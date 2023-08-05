import requests
import uuid
from azureml.studio.core.logger import get_logger
from azureml.designer.tools.model.retry import retry
from azureml.designer.tools.model.workspace_client import AzuremlWorkspaceProcessor
from azureml.designer.tools.model.tool_constants import HttpRequestMethodEnum
from azureml.designer.tools.model.tool_exceptions import HttpRequestUserError, HttpRequestServerError

logger = get_logger(__name__)


class HttpRequestHelper:
    """
    HttpRequestHelper deals with the http request with retry.

    1.Process http request with selection of request methods in HttpRequestMethodEnum.
    """
    _SECURE_HTTP_STATUS = [200, 202]
    _UNAUTHORIZED_HTTP_STATUS = 401
    _FORBIDDEN_HTTP_STATUS = 403
    _max_retries = 3
    _retry_delay = 3  # unit: second

    def __init__(self,
                 azureml_workspace_processor: AzuremlWorkspaceProcessor,
                 request_id: uuid):
        """

        :param azureml_workspace_processor: the instance for creating and refreshing the target Workspace.
        :param request_id: the unique id for tracking problems during the whole package operation.
        """
        self._azureml_workspace_processor = azureml_workspace_processor
        self._request_id = request_id
        # http request hearders, currently GET or PATCH.
        self._http_headers = self._generate_headers()

    def _generate_headers(self):
        """
        Generate initially the http get header.

        :return: headers_template: dict. The http header with workspace token and tracking request id.
        """
        headers_template = {'x-ms-client-request-id': str(self._request_id)}
        workspace_token = self._azureml_workspace_processor.get_aml_workspace_token()
        headers_template.update(workspace_token)
        return headers_template

    @retry(exceptions=(HttpRequestUserError, HttpRequestServerError), tries=_max_retries, delay=_retry_delay)
    def http_request_core(self, service_uri, request_method, request_service, patch_list=None):
        """
        The http request method with retry when occur given exceptions.

        :param service_uri: str. The http request url.
        :param request_method: HttpRequestMethodEnum. The http request method to select different http request.
        :param request_service: RequestServiceEnum. The AML service where http request targets.
        :param patch_list: dict. If http request method is PATCH, pass the http request patch body to function
            by this param, if http request method is GET, keep None for this param.
        :return: response: bytes. The http request's response if status 200 or 202, exceptions otherwise.
        """
        if request_method == HttpRequestMethodEnum.GET:
            self._http_headers.update({'Content-Type': 'application/json'})
            response = requests.get(service_uri, headers=self._http_headers)
        elif request_method == HttpRequestMethodEnum.PATCH:
            self._http_headers.update({'Content-Type': 'application/json-patch+json'})
            response = requests.patch(service_uri, json=patch_list, headers=self._http_headers)
        else:
            raise Exception(f'Unsupported http request method: {request_method.value}.')

        if response.status_code in self._SECURE_HTTP_STATUS:
            return response
        elif response.status_code == self._UNAUTHORIZED_HTTP_STATUS:
            workspace_token = self._azureml_workspace_processor.get_aml_workspace_token()
            self._http_headers.update(workspace_token)
            raise HttpRequestUserError(request_service, request_method, 'HttpRequestHelper.http_request_core',
                                       response, self._request_id,
                                       f'Unauthorized request, request url: {service_uri}')
        elif response.status_code == self._FORBIDDEN_HTTP_STATUS:
            raise HttpRequestUserError(request_service, request_method, 'HttpRequestHelper.http_request_core',
                                       response, self._request_id,
                                       f'Forbidden request, request url: {service_uri}')
        elif response.status_code >= 500 or response.status_code == 0:
            raise HttpRequestServerError(request_service, request_method, 'HttpRequestHelper.http_request_core',
                                         response, self._request_id,
                                         f'Bad response after {self._max_retries} times retry, '
                                         f'request url: {service_uri}')
        else:
            error_msg = f'Received bad response from service {request_service.value}:\n' \
                        'Rest API operation: GET\n' \
                        f'Rest API url: {service_uri}\n' \
                        f'Response Code: {response.status_code}\n' \
                        f'Headers: {response.headers}\n' \
                        f'Content: {response.content}'
            raise Exception(error_msg)
