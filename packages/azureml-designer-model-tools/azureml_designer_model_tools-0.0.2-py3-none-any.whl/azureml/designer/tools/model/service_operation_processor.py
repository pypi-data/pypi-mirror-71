import json
import time
import uuid
from azureml.studio.core.logger import get_logger
from azureml.designer.tools.model.retry import retry
from azureml.designer.tools.model.service_info_helper import ServiceInfoHelper
from azureml.designer.tools.model.azure_blob_helper import ConfigurationJsonUpdater
from azureml.designer.tools.model.workspace_client import AzuremlWorkspaceProcessor
from azureml.designer.tools.model.tool_constants import HttpRequestMethodEnum, RequestServiceEnum, ToolOperationEnum
from azureml.designer.tools.model.http_request_helper import HttpRequestHelper
from azureml.designer.tools.model.tool_exceptions import ToolOperationError

logger = get_logger(__name__)


class ServiceOperationProcessor:
    """
    ServiceOperationProcessor deals with redeploying a real-time service endpoint with a model existing in workspace.

    1.Call MMS to get this service endpoint's current information.

    2.Generate a new environmentImageRequest property for redeployment and update configuration.json of this service.

    3.Use MMS rest API for service redeployment.

    4.Wait for the final redeployment status based on the given operation id.

    5.Combine these steps above, get the new final service redeployment status.
    """
    _max_retries = 3
    _retry_delay = 1  # unit: second
    _redeployment_state_polling_interval = 15  # unit: second
    _redeployment_state_polling_timeout = 600  # unit: second

    def __init__(self,
                 azureml_workspace_processor: AzuremlWorkspaceProcessor,
                 update_service_name: str,
                 request_id: uuid,
                 update_description=None):
        """

        :param azureml_workspace_processor: the instance for creating and refreshing the target Workspace.
        :param update_service_name: the name of the to-be-redeployed service.
        :param request_id: the unique id for tracking problems during the whole package operation.
        :param update_description: the description for specific service redeployment. User defined or None.
        """
        self._azureml_workspace_processor = azureml_workspace_processor
        self._base_uri = self._generate_base_uri()
        self._update_service_name = update_service_name
        self._request_id = request_id
        self._update_description = update_description
        self._connection_string = self._get_connection_string()

    def _generate_base_uri(self):
        """
        Generate the specific MMS call url by class members in class initiation.

        :return: base_uri: str. The target url.
        """
        base_uri = f'https://{self._azureml_workspace_processor.workspace_location}.api.azureml.ms' \
                   f'/modelmanagement/v1.0/subscriptions/{self._azureml_workspace_processor.subscription_id}' \
                   f'/resourceGroups/{self._azureml_workspace_processor.resource_group}' \
                   f'/providers/Microsoft.MachineLearningServices' \
                   f'/workspaces/{self._azureml_workspace_processor.workspace_name}'
        return base_uri

    def _get_connection_string(self):
        """
        Get the workapce-associated Azure storage account's connntion sting.

        :return: connection_string: str.
        """
        data_store = self._azureml_workspace_processor.get_aml_workspace_entity().get_default_datastore()
        connection_string = f'DefaultEndpointsProtocol={data_store.protocol};AccountName={data_store.account_name};' \
                            f'AccountKey={data_store.account_key};EndpointSuffix={data_store.endpoint}'
        return connection_string

    # service operation processor entry
    def update_service_with_updated_model(self, updated_model_id, endpoint_body):
        """
        The method for integrate all the ServiceOperationProcessor steps in one.

        :param updated_model_id: str. The model id of new model for service redeployment.
        :param endpoint_body: dict. The service endpoint original return body, for getting properties.
        :return: state: str. The final service redeployment status.
        """
        try:
            update_environment_image_request = self.update_redeployment_configuration(updated_model_id, endpoint_body)

            update_operation_id = self.redeploy_service_with_patch_request(update_environment_image_request)

            state, return_content = self.wait_for_redeployment(update_operation_id)

            logger.info(f'Finish the service update operation, final operation state: {state}.\n'
                        f'Operation request tracking id: {self._request_id}.\n'
                        f'Return info: {return_content}.')
            return state
        except Exception as e:
            raise ToolOperationError(ToolOperationEnum.REDEPLOY, self._request_id) from e

    # service update operation step by step methods
    def get_service_endpoint_body(self):
        """
        Call MMS to get this service endpoint's current return body,
        with who can get properties like environmentImageRequest.

        :return: response.json(): dict.
        """
        try:
            http_request_helper = HttpRequestHelper(self._azureml_workspace_processor, self._request_id)

            service_uri = self._base_uri + f'/services?name={self._update_service_name}'

            response = http_request_helper.http_request_core(service_uri,
                                                             HttpRequestMethodEnum.GET,
                                                             RequestServiceEnum.MMS)

            logger.info("Succeed to get the given service's return body json.\n"
                        f"Operation request tracking id: {self._request_id}.\n"
                        f"Return service endpoint body: {response.content}.")
            return response.json()
        except Exception as e:
            raise Exception('Error occurred when calling backend for getting service endpoint returnbody!') from e

    def update_redeployment_configuration(self, updated_model_id, endpoint_body):
        """
        Generate new environmentImageRequest property for service redeployment by getting original one
        from endpoint return body. And update configuration.json of this service in Azure storage.

        :param updated_model_id: str. The model id of new model for service redeployment.
        :param endpoint_body: dict. The service endpoint original return body, for getting properties.
        :return: update_environment_image_request: dict. The new environmentImageRequest property.
        """
        original_environment_image_request = ServiceInfoHelper.extract_env_image(endpoint_body)

        config_json_file_name = 'configuration.json'
        container_name, blob_file_name = ServiceInfoHelper.get_config_json_blob_info(
            config_json_file_name, original_environment_image_request)

        update_environment_image_request = ServiceInfoHelper.update_environment_image_request(
            updated_model_id, original_environment_image_request)

        configuration_json_updater = ConfigurationJsonUpdater(self._connection_string)
        configuration_json_updater.update_config_json(updated_model_id, blob_file_name,
                                                      container_name, self._request_id)
        return update_environment_image_request

    def redeploy_service_with_patch_request(self, update_environment_image_request):
        """
        Use MMS rest API and http patch request for service redeployment.

        :param update_environment_image_request: dict. The new environmentImageRequest property generated by
            update_redeployment_configuration() method.
        :return: update_operation_id: uuid. The service redeployment operation id, for tracking the status of
            current service redeployment request.
        """
        http_request_helper = HttpRequestHelper(self._azureml_workspace_processor, self._request_id)

        service_uri = self._base_uri + f'/services/{self._update_service_name}'

        patch_list = ServiceInfoHelper.generate_service_update_patchbody(update_environment_image_request,
                                                                         self._update_description)

        update_operation_id = ''
        response = http_request_helper.http_request_core(service_uri,
                                                         HttpRequestMethodEnum.PATCH,
                                                         RequestServiceEnum.MMS,
                                                         patch_list=patch_list)
        if response.status_code == 200:
            content = response.content
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            service_payload = json.loads(content)
            if 'operationId' in service_payload:
                update_operation_id = service_payload['operationId']
        elif response.status_code == 202:
            if 'Operation-Location' in response.headers:
                operation_location = response.headers['Operation-Location']
            else:
                error_msg = 'Missing response header key: Operation-Location in redeployment response headers ' \
                            f'when calling {service_uri} with method {HttpRequestMethodEnum.PATCH}.\n' \
                            f'Return response header: {response.headers}'
                raise Exception(error_msg)
            update_operation_id = operation_location.split('/')[-1]

        if update_operation_id == '':
            raise Exception(f'Unknown service redeployment error: no operation id returned, service url: {service_uri}'
                            f'\nResponse content: {response.content}')

        logger.info('Succeed to patch the service update request to the backend, '
                    f'patch request return operation id: {update_operation_id}.\n'
                    f'Operation request tracking id: {self._request_id}.')
        return update_operation_id

    @retry(exceptions=KeyError, tries=_max_retries, delay=_retry_delay)
    def _get_redeploy_operation_status(self, update_operation_id, request_id):
        """
        Call MMS rest API and http get request by using given operation id to get the latest redeployment status.

        :param update_operation_id: uuid. The service redeployment operation id, for tracking the status of
            current service redeployment request.
        :param request_id: uuid. The unique id for tracking problems during the whole package operation.
        :return: state: str. The latest redeployment status.
            content: dict. The response content of MMS api call.
        """
        http_request_helper = HttpRequestHelper(self._azureml_workspace_processor, request_id)
        service_uri = self._base_uri + f'/operations/{update_operation_id}'
        response = http_request_helper.http_request_core(service_uri, HttpRequestMethodEnum.GET, RequestServiceEnum.MMS)

        content = response.content
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        service_payload = json.loads(content)
        if 'state' in service_payload.keys() and service_payload['state'] != '':
            state = service_payload['state']
            return state, content
        else:
            raise KeyError('The service operation state request return no valid state or empty state, '
                           f'GET request url: {service_uri}\nResponse: {content}')

    def wait_for_redeployment(self, update_operation_id):
        """
        Continuous MMS rest API Http Get call for getting the latest service redeployment state.
        Existing status: Cancelled  Failed  NotStarted  Running  Succeeded  TimedOut

        :param update_operation_id: uuid. The service redeployment operation id, for tracking the status of
            current service redeployment request.
        :return: current_state: str. The final redeployment status.
            current_content: dict. The final response content of MMS api call.
        """
        current_state, current_content = self._get_redeploy_operation_status(update_operation_id, self._request_id)
        tick_now = time.time()
        tick_tolerance = tick_now + self._redeployment_state_polling_timeout
        while (time.time() < tick_tolerance) and (current_state == 'Running' or current_state == 'NotStarted'):
            time.sleep(self._redeployment_state_polling_interval)
            current_state, current_content = self._get_redeploy_operation_status(update_operation_id, self._request_id)

        logger.info(f'Finish the service redeployment operation, return redeployment state: {current_state}.\n'
                    f'Return redeployment message: {current_content}.\n'
                    f'Operation request tracking id: {self._request_id}.')
        if current_state == 'Succeeded':
            return current_state, current_content
        elif current_state == 'Running' or current_state == 'NotStarted':
            raise TimeoutError("Service redeployment didn't finish after "
                               f"{self._redeployment_state_polling_timeout/60} minutes, "
                               f"current state: {current_state}, operation id: {update_operation_id}\n"
                               f"Response content: {current_content}")
        elif current_state == 'Failed' or current_state == 'TimedOut' or current_state == 'Cancelled':
            raise Exception(f'The service redeployment operation {current_state}, operation id: {update_operation_id}'
                            f'\nResponse content: {current_content}')
        else:
            raise Exception('Current service operation has occurred unknown error.\n'
                            f'Current operation state: {current_state}, operation id: {update_operation_id}'
                            f'\nResponse content: {current_content}')
