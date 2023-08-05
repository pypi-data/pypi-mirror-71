import uuid
from azureml.studio.core.logger import get_logger
from azureml.designer.tools.model.workspace_client import AzuremlWorkspaceProcessor
from azureml.designer.tools.model.http_request_helper import HttpRequestHelper
from azureml.designer.tools.model.tool_constants import RequestServiceEnum, HttpRequestMethodEnum

logger = get_logger(__name__)


class SMTOperationHelper:
    """
    SMTOperationHelper deals with obtaining the new trained model dir's Azure storage information by requesting SMT.

    1.Get the new trained model dir's Azure storage information by calling SMT rest API with given pipeline run id.
    """
    def __init__(self,
                 azureml_workspace_processor: AzuremlWorkspaceProcessor,
                 pipeline_run_id: str,
                 request_id: uuid):
        """

        :param azureml_workspace_processor: the instance for creating and refreshing the target Workspace.
        :param pipeline_run_id: the user given pipeline run id, indicate a pipeline run,
            in other words, the new trained model directory.
        :param request_id: the unique id for tracking problems during the whole package operation.
        """
        self._azureml_workspace_processor = azureml_workspace_processor
        self._pipeline_run_id = pipeline_run_id
        self._request_id = request_id
        self._base_uri = self._generate_base_uri()

    def _generate_base_uri(self):
        """
        Generate the specific SMT call url by class members in class initiation.

        :return: base_uri: str. The target url.
        """
        base_uri = f'https://{self._azureml_workspace_processor.workspace_location}.api.azureml.ms/studioservice/api' \
                   f'/subscriptions/{self._azureml_workspace_processor.subscription_id}' \
                   f'/resourceGroups/{self._azureml_workspace_processor.resource_group}' \
                   f'/workspaces/{self._azureml_workspace_processor.workspace_name}'
        return base_uri

    def get_new_trained_model_dir_blob_info(self):
        """
        When re-register a model by replacing the trained model dir locally, we should get the new trained model dir.
        Here, the new trained model is obtained by the user pipeline run, so we should call the SMT to get
        the given pipeline run id's trained model dir Azure blob storage information.
        In details are connection_string, container_name, blob_relative_path.

        :return: connection_string: str. The connection str to connect Azure storage account
            where the new trained model dir stores.
            container_name: str. The associated container for storing the new trained model dir.
            blob_relative_path: str. A prefix, which identifies all the blob files in the new trained model dir.
        """
        http_request_helper = HttpRequestHelper(self._azureml_workspace_processor, self._request_id)
        smturi = self._base_uri + f'/pipelineruns/{self._pipeline_run_id}/modeldirectory'
        response = http_request_helper.http_request_core(smturi, HttpRequestMethodEnum.GET, RequestServiceEnum.SMT)

        response_body = response.json()
        blob_relative_path = response_body.get('relativePath')
        connection_string = response_body.get('connectionString')
        container_name = response_body.get('containerName')

        if not connection_string or not container_name or not blob_relative_path:
            raise Exception("Wrong pipeline run Id, couldn't resolve blob infos from it.\n"
                            f"Connection_string: {connection_string}, container_name: {container_name}, "
                            f"blob relative path: {blob_relative_path}.\nGiven pipeline runid: {self._pipeline_run_id}")
        return connection_string, container_name, blob_relative_path
