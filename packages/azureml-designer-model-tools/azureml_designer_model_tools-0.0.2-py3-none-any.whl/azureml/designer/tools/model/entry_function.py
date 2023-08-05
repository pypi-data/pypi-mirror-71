import uuid
from azureml.core.authentication import InteractiveLoginAuthentication
from azureml.designer.tools.model.model_operation_processor import ModelOperationProcessor
from azureml.designer.tools.model.service_operation_processor import ServiceOperationProcessor
from azureml.designer.tools.model.workspace_client import AzuremlWorkspaceProcessor
from azureml.designer.tools.model.service_info_helper import ServiceInfoHelper
from azureml.designer.tools.model.tool_constants import ToolOperationEnum
from azureml.designer.tools.model.tool_exceptions import ToolOperationError
from azureml.studio.core.logger import get_logger

logger = get_logger(__name__)


def model_tools(workspace, pipeline_run_id, service_endpoint_name, update_description=None):
    """
    The entry function for redeploy a service by given user pipeline run.

    :param workspace: Workspace. The user given azureml.core.workspace.Workspace instance.
    :param pipeline_run_id: uuid. The user given pipeline run id to call SMT for getting Azure storage information of
            new trained model dir.
    :param service_endpoint_name: str. The given to-be-redeployed service's name.
    :param update_description: str. The description for specific service redeployment. User defined or None.
    :return: state: str. The final service redeployment status.
    """
    request_id = uuid.uuid1()
    try:
        InteractiveLoginAuthentication()
        logger.info(
            f'Redeploy service {service_endpoint_name} with pipelineRunId {pipeline_run_id} operation created.\n'
            f'Operation request tracking id: {request_id}.\nWorkspace information:\nname:{workspace.name}, '
            f'subscription_id:{workspace.subscription_id}, resource group:{workspace.resource_group}.')

        azureml_workspace_processor = AzuremlWorkspaceProcessor(workspace)

        service_operation_processor = ServiceOperationProcessor(azureml_workspace_processor, service_endpoint_name,
                                                                request_id, update_description=update_description)
        endpoint_body = service_operation_processor.get_service_endpoint_body()
        original_model_id = ServiceInfoHelper.extract_model_id(endpoint_body)
        model_operation_processor = ModelOperationProcessor(azureml_workspace_processor, request_id,
                                                            original_model_id)

        updated_model_id = model_operation_processor.update_model_by_pipelinerunid(pipeline_run_id)

        state = service_operation_processor.update_service_with_updated_model(updated_model_id, endpoint_body)

        logger.info(f'Finish redeploy service {service_endpoint_name} with pipelineRunId {pipeline_run_id} operation.\n'
                    f'Final redeployment state: {state}.\nOperation request tracking id: {request_id}.')
        return state
    except Exception as e:
        raise ToolOperationError(ToolOperationEnum.ENTIRE, request_id) from e


def model_tools_entry(subscription_id, resource_group, workspace_name,
                      pipeline_run_id, service_endpoint_name, update_description=None):
    """

    :param subscription_id: uuid. The subscription id for the target workspace.
    :param resource_group: str. The resource group name for the target workspace.
    :param workspace_name: str. The target workspace name.
    :param pipeline_run_id: uuid. The user given pipeline run id to call SMT for getting Azure storage information of
            new trained model dir.
    :param service_endpoint_name: str. The given to-be-redeployed service's name.
    :param update_description: The description for specific service redeployment. User defined or None.
    :return: state: str. The final service redeployment status.
    """
    from azureml.core import Workspace
    from azureml.core.authentication import InteractiveLoginAuthentication
    ws = Workspace(subscription_id=subscription_id,
                   resource_group=resource_group,
                   workspace_name=workspace_name,
                   auth=InteractiveLoginAuthentication())

    state = model_tools(ws, pipeline_run_id, service_endpoint_name, update_description=update_description)
    return state
