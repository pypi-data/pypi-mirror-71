from enum import Enum


class RequestServiceEnum(Enum):
    """
    Enum of AML http request target services.
    """
    SMT = 'service middle tier'
    MMS = 'module management service'


class HttpRequestMethodEnum(Enum):
    """
    Enum of currently supported http request methods.
    """
    GET = 'get'
    POST = 'post'
    PATCH = 'patch'


class ToolOperationEnum(Enum):
    """
    Enum of current operation steps of this tool.
    """
    ENTIRE = 'model-tools entry function'
    RETRAIN = 'retrain and register model with given pipeline run id'
    REDEPLOY = 'redeploy retrained model to current service endpoint'
