from urllib import parse
from azureml.studio.core.logger import get_logger

logger = get_logger(__name__)


class ServiceInfoHelper:
    """
    ServiceInfoHelper deals with getting the information in a service endpoint's rest API json-style return body.

    1.Get the current service-associated model's model id.

    2.Get the current service's environmentImageRequest property.

    3.Update a given environmentImageRequest property with new model id.

    4.Get the service-associated 'configuration.json' file's Azure blob information like container name, etc.

    5.Generate the patch body for service redeployment rest API patch request.
    """
    @staticmethod
    def extract_model_id(endpoint_body):
        """
        Get the current service-associated model's model id by given service endpoint return body.

        :param endpoint_body: dict. A service endpoint's rest API json-style return body.
        :return: model_ids[0]: str. The desired model id if no errors, exceptions otherwise.
        """
        try:
            environment_image_request = ServiceInfoHelper.extract_env_image(endpoint_body)
            model_ids = environment_image_request['modelIds']
            if len(model_ids) == 1:
                return model_ids[0]
            else:
                logger.error(f'Currently unhandled situation with {len(model_ids)} models '
                             'in one single service endpoint body. model amount requirement: 1.\n'
                             f'Input: {endpoint_body}')
                raise Exception(f'The given service has {len(model_ids)} models, unhandled situation!')
        except Exception as e:
            raise Exception('The given service endpoint has invalid model associated or environmentImageRequest '
                            'is invalid! Check your given real-time service endpoint.') from e

    @staticmethod
    def extract_env_image(endpoint_body):
        """
        Get the current service environmentImageRequest by given service endpoint return body.

        :param endpoint_body: dict. A service endpoint's rest API json-style return body.
        :return: original_environmentImageRequest: dict. The desired environmentImageRequest property if no errors,
            exceptions otherwise.
        """
        for endpoint_item_key, endpoint_item_value in endpoint_body.items():
            if endpoint_item_key == 'value':
                if len(endpoint_item_value) == 1:
                    for endpoint_property_key, endpoint_property_value in endpoint_item_value[0].items():
                        if endpoint_property_key == 'environmentImageRequest':
                            return ServiceInfoHelper._validate_env_image(endpoint_property_key,
                                                                         endpoint_property_value,
                                                                         endpoint_body)
                    logger.error(f'The input endpoint_body has no environmentImageRequest property!\n'
                                 f'Input: {endpoint_body}')
                elif len(endpoint_item_value) == 0:
                    logger.error(f'The input endpoint_body for extracting is empty!\n Input: {endpoint_body}')
                else:
                    logger.error(f"Currently unhandled situation with {len(endpoint_item_value)} 'value' assets "
                                 "in endpoint body input. 'value' assets amount requirement: 1.\n"
                                 f"Input: {endpoint_body}")

        raise Exception(f'There is no environmentImageRequest property in current given service!')

    @staticmethod
    def _validate_env_image(endpoint_property_key, endpoint_property_value, endpoint_body):
        """
        Validate the obtained environmentImageRequest property in endpoint return body.

        :param endpoint_property_key: str. It's just string 'environmentImageRequest',
            the key of environmentImageRequest property key-value pair in endpoint body. Here for logging only.
        :param endpoint_property_value: dict. The obtained environmentImageRequest property.
        :param endpoint_body: dict. A service endpoint's rest API json-style return body. Here for logging only.
        :return: original_environmentImageRequest: dict. The desired environmentImageRequest property if no errors,
            exceptions otherwise.
        """
        if not endpoint_property_value:
            logger.error('Extract endpoint_body failed! '
                         f'{endpoint_property_key} Message missed in endpoint body!\nEndpoint body: {endpoint_body}')
            raise Exception(f'No environmentImageRequest property in input service endpoint body.')
        else:
            original_environment_image_request = endpoint_property_value
            return original_environment_image_request

    @staticmethod
    def update_environment_image_request(update_model_id, original_environment_image_request):
        """
        In service redeployment patch request's request body, update the model id in environmentImageRequest property.

        :param update_model_id: str. The new model id should be used for updating(replacing).
        :param original_environment_image_request: dict. The given original environmentImageRequest property param.
        :return: update_environment_image_request: dict. The updated environmentImageRequest property
            after replacing the information model id.
        """
        if 'modelIds' in original_environment_image_request.keys():
            modelid_list = original_environment_image_request['modelIds']
            if len(modelid_list) == 1:
                original_environment_image_request['modelIds'] = [update_model_id]
                update_environment_image_request = original_environment_image_request
                return update_environment_image_request
            else:
                logger.error(f'Unhandled situation! there are {len(modelid_list)} models in this service endpoint!'
                             'model amount requirement: 1.\n'
                             f'Input environmentImageRequest: {original_environment_image_request}')
        else:
            logger.error("Lack of 'modelIds' property in "
                         f"input environmentImageRequest: {original_environment_image_request}")

        raise Exception(f'Update environmentImageRequest property failed when patch redeployment request!')

    @staticmethod
    def get_config_json_blob_info(config_json_file_name, original_env_image_request):
        """
        By reading the given environmentImageRequest property, get the service-associated Azure blob file
        "configuration.json" storage info: container name, blob file name.
        In 'assets' property of environmentImageRequest property,
        get the asset url value with "id"=="configuration.json".
        The target url for obtaining "configuration.json" Azure storage info is like this:
        "aml://artifact/LocalUpload/623d7344-48a5-4475-b247-cb1f10b1ea7f/configuration.json"

        :param config_json_file_name: str. The file name for searching its Azure storage info.
        :param original_env_image_request: dict. The given environmentImageRequest property param for searching.
        :return: container_name: str. The searching file's Azure storage container name.
            blob_file_name: str. The searching file's blob file name.
        """
        try:
            config_asset_blob_url = ServiceInfoHelper._get_config_json_asset_blob_url(config_json_file_name,
                                                                                      original_env_image_request)
            container_name, blob_file_name = ServiceInfoHelper._split_config_json_asset_blob_url(config_asset_blob_url)
            return container_name, blob_file_name
        except Exception as e:
            raise Exception("Error occurred when get blob file name of 'configuration.json' "
                            f"from environment image request. Details: {e}") from e

    @staticmethod
    def _get_config_json_asset_blob_url(desired_file_name, original_env_image_request):
        """
        Private method only for get_config_json_blob_info() method.
        Search in given environmentImageRequest property's 'assets' property, find the asset
        whose 'id' key has the value of desired_file_name param. Return this asset's key=='url' value.
        # e.g. "aml://artifact/LocalUpload/623d7344-48a5-4475-b247-cb1f10b1ea7f/configuration.json"

        :param desired_file_name: str. The file name for searching the Azure storage info.
        :param original_env_image_request: dict. The environmentImageRequest property
        :return: desired_file_blob_url: str. The desired file name's Azure storage info url.
        """
        desired_file_blob_url = ''
        desired_asset_count = 0
        if 'assets' in original_env_image_request.keys():
            assets = original_env_image_request['assets']
            for asset in assets:
                if 'id' in asset.keys() and 'url' in asset.keys():
                    if asset['id'] == desired_file_name:
                        desired_file_blob_url = asset['url']
                        desired_asset_count += 1
            if desired_file_blob_url == '':
                logger.error(f'Fail to find the existing blob file url of {desired_file_name} '
                             f'in environmentImageRequest input: {original_env_image_request}')
            if desired_asset_count != 1:
                logger.error(f'Duplication when finding the existing blob file url of {desired_file_name} '
                             f'in environmentImageRequest input: {original_env_image_request}')
        else:
            logger.error("Lack of 'assets' property in given environmentImageRequest input:\n"
                         f"{original_env_image_request}")

        if desired_file_blob_url != '' and desired_asset_count == 1:
            return desired_file_blob_url
        else:
            raise Exception(f"Fail to get the existing blob file url of '{desired_file_name}' "
                            "from environmentImageRequest property which is extracted from "
                            "the given service endpoint's return body!")

    @staticmethod
    def _split_config_json_asset_blob_url(config_json_asset_blob_url):
        """
        Private method only for get_config_json_blob_info() method.
        Split the given url param for obtaining the container name and blob file name information.
        e.g. "aml://artifact/LocalUpload/623d7344-48a5-4475-b247-cb1f10b1ea7f/configuration.json"
        It can be split and extracted the container name: azureml('aml')
        and blob file name: LocalUpload/623d7344-48a5-4475-b247-cb1f10b1ea7f/configuration.json

        :param config_json_asset_blob_url: str. The url contains target configuration.json's
            blob storage container name and file name. A url obtained by _get_config_json_asset_blob_url() method.
        :return: container_name: str. The Azure storage container name in the given url.
            blob_file_name: str. The blob file name in the given url.
        """
        blob_url_parsed = parse.urlparse(config_json_asset_blob_url)

        container_name = blob_url_parsed.scheme
        blob_host_name = blob_url_parsed.netloc
        blob_file_name = blob_url_parsed.path

        if container_name == 'aml':
            container_name = 'azureml'
        else:
            error_msg = "Currently unhandled container name or name abbreviation" \
                        "(the container name abbreviation in url input should be 'aml' means azureml) " \
                        f"in blob url input: {config_json_asset_blob_url}, " \
                        f"unhandled container name: {container_name}."
            raise Exception(error_msg)

        if blob_file_name.startswith('/'):
            # after urlparse, the blob file name will start with / which will trouble steps next, so remove it.
            # e.g. Before: /LocalUpload/623d7344-48a5-4475-b247-cb1f10b1ea7f/configuration.json
            # After: LocalUpload/623d7344-48a5-4475-b247-cb1f10b1ea7f/configuration.json
            blob_file_name = blob_file_name.lstrip('/')
        if not blob_file_name or not blob_file_name.startswith('LocalUpload') or blob_host_name != 'artifact':
            error_msg = "Wrong blob file url input!\n'Configuration.json' blob file name Not Found "\
                        f"in input blob file url: '{config_json_asset_blob_url}' when processing it."
            raise Exception(error_msg)

        return container_name, blob_file_name

    @staticmethod
    def generate_service_update_patchbody(update_env_image_request, update_description):
        """
        Generate the patch request body for service redeployment rest API patch request by given params.

        :param update_env_image_request: dict. The updated environmentImageRequest property.
        :param update_description: str. The description of redeployment patch request. User defined or None.
        :return: patch_list: dict. The generated patch body. Then it will be the http patch request's request body.
        """
        patch_list = [{'op': 'remove', 'path': '/imageId', 'value': 'null', 'from': 'null'}]
        if update_env_image_request is not None:
            patch_list.append({'op': 'replace', 'path': '/environmentImageRequest',
                               'value': update_env_image_request, 'from': 'null'})
        if update_description:
            patch_list.append({'op': 'replace', 'path': '/description',
                               'value': update_description, 'from': 'null'})

        return patch_list
