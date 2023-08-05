from azureml.core.workspace import Workspace
from azureml.designer.tools.model.tool_exceptions import InputDataError
from azureml.studio.core.logger import get_logger

logger = get_logger(__name__)


class AzuremlWorkspaceProcessor:
    """
    AzuremlWorkspaceProcessor deals with the azureml workspace's get and refresh.
    """
    _refresh_token_retries = 3

    def __init__(self,
                 workspace_entity: Workspace):
        """

        :param workspace_entity: Workspace. The user given azureml.core.workspace.Workspace instance.
        """
        self._workspace = workspace_entity
        self.subscription_id = workspace_entity.subscription_id
        self.resource_group = workspace_entity.resource_group
        self.workspace_name = workspace_entity.name
        self.workspace_location = workspace_entity.location

    def get_aml_workspace_entity(self):
        """
        Validate and get the given workspace entity.

        :return: self._workspace: Workspace. The validated workspace instance.
        """
        if self.subscription_id and self.resource_group and self.workspace_name:
            return self._workspace
        else:
            error_msg = f'Invalid workspace client input!\n workspace name: {self.workspace_name}, ' \
                        f'subscription_id: {self.subscription_id}, resource_group: {self.resource_group}.'
            raise InputDataError('workspace_entity', error_msg, with_traceback=False)

    def get_aml_workspace_token(self):
        """
        Get the token of given workspace, cause the token refresh every 1 hour, this method will be used very frequently
        for refreshing the workspace token.

        :return: workspace_token: HTTP authorization header.
        """
        # get the workspace token with retry
        remain_token_retries = self._refresh_token_retries
        while remain_token_retries > 0:
            try:
                workspace_token = self._workspace._auth.get_authentication_header()
                return workspace_token
            except Exception as e:
                logger.error('Failed to refresh the workspace token in the number '
                             f'{self._refresh_token_retries-remain_token_retries} retry!\n'
                             f'workspace name: {self.workspace_name}, subscription_id: {self.subscription_id}, '
                             f'resource_group: {self.resource_group}.\nError message: {e}')
            finally:
                remain_token_retries -= 1

        error_msg = f'Failed to get the workspace token!\n workspace name: {self.workspace_name}, ' \
                    f'subscription_id: {self.subscription_id}, resource_group: {self.resource_group}'
        raise InputDataError('workspace_entity', error_msg, with_traceback=False)
