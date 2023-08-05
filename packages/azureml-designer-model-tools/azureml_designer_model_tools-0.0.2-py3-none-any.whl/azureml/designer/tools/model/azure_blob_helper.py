import os
import shutil
import json
from azure.storage.blob import BlobServiceClient
from azureml.studio.core.logger import get_logger

logger = get_logger(__name__)


class AzureBlobServiceClient:
    """
    AzureBlobServiceClient deals with creating Azure storage account client.

    1.Create a azure storage service client based on given connection string.
    """
    def __init__(self,
                 connection_string: str):
        """

        :param connection_string: the connection str to connect Azure storage account, both ModelOperationProcessor
            and ServiceOperationProcessor need connect to Azure Storage for blob file processing.
        """
        self._connection_string = connection_string
        self.service_client = AzureBlobServiceClient._create_blob_service_client(connection_string)

    @staticmethod
    def _create_blob_service_client(connection_string):
        """
        Create Azure storage client by azure storage account connection string.

        :param connection_string: str. the connection str to connect Azure storage account, both ModelOperationProcessor
            and ServiceOperationProcessor need connect to Azure Storage for blob file processing.
        :return: blob_service_client: BlobServiceClient. The created azure storage client. Throw exception otherwise.
        """
        try:
            service_client = BlobServiceClient.from_connection_string(connection_string)
            return service_client
        except Exception as e:
            logger.error('Fail to create Azure Blob service client. '
                         f'Blob service connection string: {connection_string}.\n Error message: {e}')
            raise Exception(f'Fail to create Azure Blob service client.\n Error message: {e}') from e

    def download_single_blob_file(self, local_download_dir, blob_file_name, container_name):
        """
        Download a single blob file from current Azure Storage Account based on the given conatiner and blob file name.

        :param local_download_dir: str. The local dir path to save this download blob file.
        :param blob_file_name: str. The to be downloaded blob file's blob file name, a relative file path.
        :param container_name: str. The container's name where this blob file stores.
        :return: download_file_local_path: str. The downloaded file's local file path.
        """
        current_blob_file_client = self.service_client.get_blob_client(container=container_name,
                                                                       blob=blob_file_name)

        download_file_local_path = os.path.join(local_download_dir, blob_file_name)
        # cause blob_file_name is a relative file path,
        # so we should combine local_download_dir and blob_file_name as the local download file path.
        dir_path, file_name = os.path.split(download_file_local_path)
        # split the local download file path to dir path and file name to create the dir tree.
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        if not os.path.isfile(download_file_local_path):
            try:
                # here use the blob_client to download this blob file.
                # Noticed: the method blob_client.download_blob() returns
                # the binary stream, so the file's open() style should have 'b'
                with open(download_file_local_path, "wb") as download_file:
                    # max_concurrency: the max concurrent downloader numbers
                    current_blob_file_client.download_blob(max_concurrency=10).readinto(download_file)
                return download_file_local_path
            except Exception as e:
                raise Exception('There occurs error when downloading the target blob file: '
                                f'{blob_file_name} from container: {container_name}.\n error message: {e}') from e
        else:
            error_msg = 'There occurs a local file duplication when download the target blob file from Azure Blob!\n' \
                        f'Duplicated blob file name: {blob_file_name}, container: {container_name}, ' \
                        f'Local download path: {download_file_local_path}.'
            raise Exception(error_msg)


class AzureBlobHelper:
    """
    AzureBlobHelper deals with the Azure storage blob file process.

    1.Download a list of blob files in the specific container with a list of blob file name.

    2.Download blob file in the specific container with specific blob file name.
    Here, the blob file name param will be represented by specific blob file client.

    3.Get all the blob file names in a specific container based on a given blob file name prefix.
    """
    def __init__(self,
                 connection_string: str):
        """

        :param connection_string: the connection str to create a AzureBlobServiceClient class instance,
            with this instance, get the Azure storage account client to process blob files.
        """
        self._blob_service_client = AzureBlobServiceClient(connection_string)

    def download_blob_files(self, blob_file_name_list, container_name, local_download_dir):
        """
        Download the needed files from a given container of Azure storage account client
        based on the given blob file name list which saves these blob files.
        All the downloaded files will be saved in a given local dir path.

        :param blob_file_name_list: str list. A list of blob file names, all blob files in this list will be downloaded.
        :param container_name: str. The name of container where store these blob files.
        :param local_download_dir: str. The local dir path where these blob files are downloaded.
        :return: download_file_local_paths: str list. The local file path list of downloaded blob files.
        """
        if os.path.exists(local_download_dir):
            # clean the local download path if it exists
            shutil.rmtree(local_download_dir)
        os.makedirs(local_download_dir)

        download_file_local_paths = []
        try:
            for blob_file_name in blob_file_name_list:
                # Create a blob client to download a single blob file, here these two params are:
                # container: the container name where the blob stores;
                # blob: the to-be-downloaded blob's name
                download_file_local_paths.append(self._blob_service_client.download_single_blob_file(local_download_dir,
                                                                                                     blob_file_name,
                                                                                                     container_name))
        except Exception as e:
            raise Exception('Some errors happened when downloading the TrainModel directory which used for '
                            'model registration update from Azure Blob!\n'
                            f'Details: {e}\n'
                            f'Downloaded blob files name list: {blob_file_name_list}') from e

        logger.info('Success to download the required blob files from blob!\n'
                    f'Local save dir path: {local_download_dir}.\n'
                    f'Download azure blob container name: {container_name}, files list: {blob_file_name_list}.')
        return download_file_local_paths

    def get_blob_filenames_with_prefix(self, container_name, blob_file_relative_path):
        """
        Search in a Azure blob storage container with given container_name to
        find all the blob file names with prefix of given blob file relative path.
        blob file relative path is like this: 'azureml/0790b6b4-5f17-436c-929c-93a90a518097/Trained_model'

        :param container_name: str. The target search container's name.
        :param blob_file_relative_path: str. The given blob file name prefix for searching.
        :return: blob_filenames: str list. A list of blob file names which match given prefix.
        """
        try:
            container_client = self._blob_service_client.service_client.get_container_client(container_name)
            # add '/' to avoid situation that the blob_file_relative_path is also a blob file name.
            # if blob_file_relative_path is empty or it ends with '\', that will be an error, except it.
            if not blob_file_relative_path \
                    or blob_file_relative_path.strip() == '' \
                    or blob_file_relative_path.endswith('\\'):
                raise Exception(f'The given blob_file_relative_path: {blob_file_relative_path} is null or wrong-style.')
            if not blob_file_relative_path.endswith('/'):
                blob_file_relative_path += '/'
            blob_list = container_client.list_blobs(name_starts_with=blob_file_relative_path)
            blob_filenames = [blob_instance.name for blob_instance in blob_list]
            return blob_filenames
        except Exception as e:
            error_msg = 'There occurs error when getting the new trained model dir blob file names list ' \
                        f'from container: {container_name} ' \
                        f'with blob trained model dir relative path: {blob_file_relative_path}.\n ' \
                        f'Error message: {e}'
            raise Exception(error_msg) from e


class ConfigurationJsonUpdater:
    """
    ConfigurationJsonUpdater deals with updating the model id in 'configuration.json',
    that the blob file 'configuration.json' is a config file associated with a service endpoint.

    1.Update the 'configuration.json' file in Azure storage blob with given new model id.
    """
    def __init__(self,
                 connection_string: str):
        """

        :param connection_string: the connection str to create a AzureBlobServiceClient class instance,
            with this instance, get the Azure storage account client to process blob files.
        """
        self._blob_service_client = AzureBlobServiceClient(connection_string)

    def update_config_json(self, update_model_id, blob_file_name, container_name, request_id):
        """
        When redeploy a service endpoint, the associated config file 'configuration.json' in Azure storage blob
        should be updated. This update is to modify the service-associated model id
        with the new registered model's model id. Download this 'configuration.json' firstly, then update it locally,
        delete original file in Azure storage and then upload the new local one.

        :param update_model_id: str. The new model id which should be used for updating 'configuration.json'.
        :param blob_file_name: str. The blob file name of to-be-updated 'configuration.json' file.
        :param container_name: str. The Azure storage container of the target 'configuration.json' file.
        :param request_id: uuid. A unique id for tracking whole operation, here for log.
        :return:
        """
        if not update_model_id or not blob_file_name or not container_name:
            error_msg = "Empty params input when updating 'configuration.json' in Azure blob, can not process!\n" \
                        f"Operation request tracking id: {request_id}.\n" \
                        f"ModelId input(to be updated): {update_model_id}, blob file name input: {blob_file_name}, " \
                        f"container name input: {container_name}"
            raise Exception(error_msg)

        config_json_local_download_dir = f'./config_json_dir_{request_id}'
        if not os.path.exists(config_json_local_download_dir):
            os.makedirs(config_json_local_download_dir)
        try:
            config_json_blob_client = self._blob_service_client.service_client.get_blob_client(container=container_name,
                                                                                               blob=blob_file_name)

            config_json_local_file_path = self._blob_service_client.download_single_blob_file(
                config_json_local_download_dir,
                blob_file_name,
                container_name)

            with open(config_json_local_file_path, "r") as jsonFile:
                data = json.load(jsonFile)
                if "model" in data.keys():
                    data["model"] = update_model_id
                else:
                    raise Exception("The configuration.json file doesn't have model id info, check it. "
                                    f"Config file content: {data}")

            with open(config_json_local_file_path, "w") as jsonFile:
                json.dump(data, jsonFile)

            # TODO find a better way to update configuration.json in blob, here deletion and upload are separate.
            config_json_blob_client.delete_blob()
            # Upload the created file
            with open(config_json_local_file_path, "rb") as jsonFile:
                config_json_blob_client.upload_blob(jsonFile)
        except Exception as e:
            error_msg = "There occurs error when updating 'configuration.json' from Azure blob. " \
                        f"ModelId of the model to be updated: {update_model_id}, " \
                        f"'configuration.json' blob file name: {blob_file_name}, " \
                        f"blob container name: {container_name}\nError message: {e}"
            raise Exception(error_msg) from e
        finally:
            shutil.rmtree(config_json_local_download_dir)
