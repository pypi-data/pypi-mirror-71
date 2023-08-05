import uuid
import requests
import traceback
from azureml.studio.core.error import UserError
from azureml.designer.tools.model.tool_constants import RequestServiceEnum, HttpRequestMethodEnum, ToolOperationEnum


class ToolOperationError(Exception):
    """
    ToolOperationError defines the errors raised in this tool's operation steps.
    """
    def __init__(self,
                 fail_step: ToolOperationEnum,
                 request_id: uuid,
                 extra_error_msg=None,
                 with_traceback=True):
        """

        :param fail_step: The operation step where failed, currently register and redeploy step.
        :param request_id: The unique id for tracking problems during the whole package operation.
        :param extra_error_msg: The passing extra error message.
        :param with_traceback: Flag to indicating the error has traceback or not. Generally flag is True.
        """
        if fail_step == ToolOperationEnum.ENTIRE:
            errmsg = f"Some errors occurred in this pkg tool's entry function, current request id: {request_id}.\n" \
                     f"Details: {None if extra_error_msg is None else extra_error_msg}."
        elif fail_step == ToolOperationEnum.RETRAIN:
            errmsg = f"The model operation step '{fail_step.value}' failed, check it with request id: {request_id}.\n" \
                     f"Details: {None if extra_error_msg is None else extra_error_msg}."
        elif fail_step == ToolOperationEnum.REDEPLOY:
            errmsg = f"The service operation step '{fail_step.value}' failed, check it with request id: {request_id}." \
                     f"\nDetails: {None if extra_error_msg is None else extra_error_msg}."
        else:
            errmsg = f"Unknown step '{fail_step.value}' failed, contact support with request id: {request_id}.\n" \
                     f"Details: {None if extra_error_msg is None else extra_error_msg}."
        if with_traceback:
            errmsg += '\n'
            errmsg += traceback.format_exc()
        super().__init__(errmsg)


class HttpRequestUserError(UserError):
    """
    HttpRequestUserError defines the Http 400 user errors in azureml-designer-model-tools.
    """
    def __init__(self,
                 request_service: RequestServiceEnum,
                 http_request_type: HttpRequestMethodEnum,
                 api_name: str,
                 response: requests.Response,
                 request_id: uuid,
                 exception_details,
                 with_traceback=True):
        """

        :param request_service: The AML service where http request targets.
        :param http_request_type: The http request method to select different http request.
        :param api_name: The api name where the error occurs.
        :param response: Current http response.
        :param request_id: The unique id for tracking problems during the whole package operation.
        :param exception_details: Optional param for passing extra error message.
        :param with_traceback: Flag to indicating the error has traceback or not. Generally flag is True.
        """
        errmsg = f'{response.status_code} {response.reason}!\n' \
                 f'When processing the http {http_request_type.value} request to {request_service.value} ' \
                 f'by the internal method {api_name}, there occurs some user errors.\n' \
                 f'Http response content: {response.content}\n' \
                 f'Tracking request id: {request_id}, exception details: {exception_details}.'
        if with_traceback:
            errmsg += '\n'
            errmsg += traceback.format_exc()
        super().__init__(errmsg)


class HttpRequestServerError(Exception):
    """
    HttpRequestServerError defines the Http 500 server errors in azureml-designer-model-tools.
    """
    def __init__(self,
                 request_service: RequestServiceEnum,
                 http_request_type: HttpRequestMethodEnum,
                 api_name: str,
                 response: requests.Response,
                 request_id: uuid,
                 exception_details,
                 with_traceback=True):
        """

        :param request_service: The AML service where http request targets.
        :param http_request_type: The http request method to select different http request.
        :param api_name: The api name where the error occurs.
        :param response: Current http response.
        :param request_id: The unique id for tracking problems during the whole package operation.
        :param exception_details: Optional param for passing extra error message.
        :param with_traceback: Flag to indicating the error has traceback or not. Generally flag is True.
        """
        errmsg = f'{response.status_code} {response.reason}!\n' \
                 f'When processing the http {http_request_type.value} request to {request_service.value} ' \
                 f'by the internal method {api_name}, there occurs some server errors.\n' \
                 f'Http response content: {response.content}\n' \
                 f'Tracking request id: {request_id}, exception details: {exception_details}.'
        if with_traceback:
            errmsg += '\n'
            errmsg += traceback.format_exc()
        super().__init__(errmsg)


class InputDataError(UserError):
    """
    InputDataError defines the errors raised by wrong or inappropriate input.
    """
    def __init__(self,
                 input_name: str,
                 error_msg: str,
                 with_traceback=True):
        """

        :param input_name: The wrong or inappropriate input's name.
        :param error_msg: The passing detailed error message.
        :param with_traceback: Flag to indicating the error has traceback or not. Generally flag is True.
        """
        errmsg = f'Invalid input for processing.\nInput: {input_name}\nData: {str(error_msg)}'
        if with_traceback:
            errmsg += '\n'
            errmsg += traceback.format_exc()
        super().__init__(errmsg)
