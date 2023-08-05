import os
import re
import shutil
import zipfile
import uuid
from azureml.core.model import Model
from azureml.studio.core.logger import get_logger
from azureml.designer.tools.model.workspace_client import AzuremlWorkspaceProcessor
from azureml.designer.tools.model.smt_operation_helper import SMTOperationHelper
from azureml.designer.tools.model.model_package_helper import ModelPackageHelper
from azureml.designer.tools.model.azure_blob_helper import AzureBlobHelper
from azureml.designer.tools.model.tool_constants import ToolOperationEnum
from azureml.designer.tools.model.tool_exceptions import ToolOperationError

logger = get_logger(__name__)


class ModelOperationProcessor:
    """
    ModelOperationProcessor deals with updating a registered model.

    1.Download the original model based on the given model id.

    2.Extract(Unzip) the download model to a local directory.

    3.Get the original trained model dir's relative path in the extracted model.

    4.Download the new trained model dir based on the given pipeline run id.

    5.Replace the trained model dir in extracted model with the downloaded new trained model dir.

    6.Re-zip the model with replacement.

    7.Register the new locally changed model to the given workspace.

    8.Combine these steps above, get the new registered model's model id.
    """
    def __init__(self,
                 azureml_workspace_processor: AzuremlWorkspaceProcessor,
                 request_id: uuid,
                 original_model_id: str):
        """

        :param azureml_workspace_processor: the instance for creating and refreshing the target Workspace.
        :param request_id: the unique id for tracking problems during the whole package operation.
        :param original_model_id: the original model's model id.
        """
        self._azureml_workspace_processor = azureml_workspace_processor
        self._request_id = request_id
        self._base_uri = self._generate_base_uri()
        model_info = original_model_id.split(':')
        self._model_name, self._original_model_version = model_info[0], model_info[1]
        # temporary process dirs
        self._temp_root = f'./{self._request_id}'
        self._model_download_root = os.path.join(self._temp_root, 'ModelsRepo')  # private
        self._model_extract_root = os.path.join(self._temp_root, 'ModelsRepoExtracted')  # private
        self._blob_trained_model_download_root = os.path.join(self._temp_root, 'BlobDownload')  # private
        self._model_rezip_root = os.path.join(self._temp_root, 'ModelsReZip')  # private

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

    # the ModelOperationProcessor entry
    def update_model_by_pipelinerunid(self, pipeline_run_id):
        """
        The method for integrate all the ModelOperationProcessor steps in one.

        :param pipeline_run_id: uuid. The user given pipeline run id to call SMT for getting Azure storage information
            of new trained model dir.
        :return: updated_model_id: str. The new registered model's model id.
        """
        self._init_sub_dirs()
        # initiate local process dirs
        try:
            self._download_original_model()

            model_unzip_dir_path = self._unzip_downloaded_model()

            original_model_dir_relative_path = self._get_original_trained_model_relative_path(model_unzip_dir_path)

            downloaded_trained_model_file_paths = self._download_blob_trained_model_dir(pipeline_run_id)

            self._process_model_dir_replacement(downloaded_trained_model_file_paths, original_model_dir_relative_path)

            updated_model_file_path = self._zip_updated_model()

            updated_model_id = self._register_updated_model(updated_model_file_path)

            logger.info(f'Succeed to register the locally updated model by given pipeline run id: {pipeline_run_id}.\n'
                        f'Operation request tracking id: {self._request_id}.')
            return updated_model_id
        except Exception as e:
            raise ToolOperationError(ToolOperationEnum.RETRAIN, self._request_id) from e
        finally:
            self._destroy_sub_dir(self._temp_root)

    # the ModelOperationProcessor step by step methods
    def _download_original_model(self):
        """
        With the given original model id, download this original model from workspace.

        :return:
        """
        model_management_helper = ModelManagementServiceHelper(self._azureml_workspace_processor)
        model_management_helper.download_model_by_id(self._model_download_root, self._model_name,
                                                     self._original_model_version)
        logger.info(f'Succeed to download the original model: {self._model_name}:{self._original_model_version}.'
                    f'local download dir: {self._model_download_root}.\n'
                    f'Operation request tracking id: {self._request_id}.')

    def _unzip_downloaded_model(self):
        """
        Extract downloaded original model, return the extracted local dir path
        Besides, the downloaded model is a file without postfix, add 'zip' postfix for it firstly.

        :return: unzip_model_dir_path: str. The model's local extracted dir path.
        """
        if not os.path.exists(self._model_extract_root):
            os.makedirs(self._model_extract_root)

        zip_model_file_path = os.path.join(self._model_download_root, f'{self._model_name}.zip')
        if not os.path.isfile(zip_model_file_path):
            logger.error('When processing the downloaded model, in the step of extracting the download zip model from '
                         f'{zip_model_file_path} to {self._model_extract_root}(relative path), '
                         f'there is no downloaded model in target dir: {zip_model_file_path}')
            raise FileNotFoundError('Try again!\nInner error when processing original to-be-updated model: '
                                    f'{self._model_name}.')

        # the extracted dir root
        unzip_model_dir_path = os.path.join(self._model_extract_root, self._model_name)
        if not os.path.exists(unzip_model_dir_path):
            os.makedirs(unzip_model_dir_path)
        with zipfile.ZipFile(zip_model_file_path) as zf:
            zf.extractall(unzip_model_dir_path)

        logger.info('Succeed to extract the downloaded model zip file. '
                    f'Local downloaded zip model dir: {self._model_download_root}, '
                    f'local extracted model file dir: {unzip_model_dir_path}.\n'
                    f'Operation request tracking id: {self._request_id}.')
        return unzip_model_dir_path

    def _get_original_trained_model_relative_path(self, extract_dir_path):
        """
        Get the original trained model dir's relative path of the extracted original model.

        :param extract_dir_path: str. The local dir path where the extracted original model stores.
        :return: original_model_dir_relative_path: str. The original trained model dir relative path.
        """
        # the model package file name where the json-style model loads
        model_package_file_name = 'modelpackage.json'
        model_package_file_path = os.path.join(extract_dir_path, model_package_file_name)
        original_model_dir_relative_path = ModelPackageHelper.get_model_dir_relative_path(model_package_file_path)
        logger.info("Succeed to get the original model's trained model dir relative path: "
                    f"{original_model_dir_relative_path}.\n"
                    f"Operation request tracking id: {self._request_id}.")
        return original_model_dir_relative_path

    def _download_blob_trained_model_dir(self, pipeline_run_id):
        """
        Based on the given pipeline run id, download the new trained model dir from Azure Storage.

        :param pipeline_run_id: The user given pipeline run id to call SMT for getting Azure storage information of
            new trained model dir.
        :return: downloaded_trained_model_file_paths: str list. A list of local file path for all the files
            in the downloaded new trained model dir.
        """
        smt_operation_helper = SMTOperationHelper(self._azureml_workspace_processor, pipeline_run_id, self._request_id)
        connection_str, container_name, blob_relative_path = smt_operation_helper.get_new_trained_model_dir_blob_info()
        azure_blob_helper = AzureBlobHelper(connection_str)
        blob_file_name_list = azure_blob_helper.get_blob_filenames_with_prefix(container_name,
                                                                               blob_relative_path)
        # the dir path to save the downloaded blob files
        blob_trained_model_download_dir = os.path.join(self._blob_trained_model_download_root, self._model_name)
        # the local file path list of the downloaded trained model dir blob file paths.
        downloaded_trained_model_file_paths = azure_blob_helper.download_blob_files(blob_file_name_list, container_name,
                                                                                    blob_trained_model_download_dir)
        logger.info(f'Succeed to download the new trained model dir from azure blob, container name: {container_name},'
                    f'blob file name list: {blob_file_name_list}.\n'
                    f'Local download path list: {downloaded_trained_model_file_paths}.\n'
                    f'Operation request tracking id: {self._request_id}.')
        return downloaded_trained_model_file_paths

    @staticmethod
    def _process_model_dir_file_replacement(original_model_dir_absolute_path, downloaded_trained_model_file_path):
        """
        Replace a single file with file of the downloaded new trained model dir.

        :param original_model_dir_absolute_path: str. The original trained model dir local path, like '.../Resources/0'.
        :param downloaded_trained_model_file_path: str. one of the downloaded new trained model dir file's local path.
        :return: new_model_dir_absolute_file_path: str. The local file path of new trained model dir file
            after replacement, actually it should be the same as param 'downloaded_trained_model_file_path'.
        """
        path_list = re.split(r'[/|\\]', downloaded_trained_model_file_path)
        append = ''
        # here, we should copy files of the path downloaded_trained_model_file_path to
        # the dir original_model_dir_absolute_path.
        # But for keep the dir structure as the blob files in Azure blob, we should get the path 'append',
        # it the rest path of blob file after prefix 'Trained_model/.....'.
        start_index = path_list.index('Trained_model')
        if start_index >= len(path_list):
            logger.error('The current downloaded blob file(new Trained model for updating) is not found, '
                         f'blob file download path: {downloaded_trained_model_file_path}.')
            raise FileNotFoundError('Try again!\n Inner error when processing the original to-be-replaced model.')
        for i in range(start_index + 1, len(path_list)):
            append = os.path.join(append, path_list[i])

        new_model_dir_absolute_file_path = os.path.join(original_model_dir_absolute_path, append)
        # split the downloaded blob file path with the dir path and the file name
        dir_path, file_name = os.path.split(new_model_dir_absolute_file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        # only can copy file to a destination, if copy dir, do it yourself
        shutil.copy(downloaded_trained_model_file_path, new_model_dir_absolute_file_path)

        return new_model_dir_absolute_file_path

    def _process_model_dir_replacement(self, downloaded_trained_model_file_paths, original_model_dir_relative_path):
        """
        Replace all the files in origianl trained model dir with the downloaded new trained model dir's file.

        :param downloaded_trained_model_file_paths: str list. A list of local file path for all the files
            in the downloaded new trained model dir.
        :param original_model_dir_relative_path: str. The original trained model dir relative path.
        :return: new_model_dir_file_paths: str list. The local file path list of new trained model dir files
            after replacement.
        """
        blob_trained_model_download_dir = os.path.join(self._blob_trained_model_download_root, self._model_name)
        # the dir path to store the downloaded blob files
        if not os.path.exists(blob_trained_model_download_dir):
            logger.error('The current downloaded blob directory(new Trained model dir for updating) is NOT found, '
                         f'relative downloaded trained model dir path: {blob_trained_model_download_dir}.')
            raise NotADirectoryError('Try again!\n Inner error when processing the original to-be-replaced model.')

        # the path of unzip model dir
        unzip_model_dir_path = os.path.join(self._model_extract_root, self._model_name)

        # the absolute local model dir path for being replaced.
        original_model_dir_absolute_path = os.path.join(unzip_model_dir_path, original_model_dir_relative_path)
        if os.path.exists(original_model_dir_absolute_path):
            shutil.rmtree(original_model_dir_absolute_path)
        os.makedirs(original_model_dir_absolute_path)

        new_model_dir_file_paths = []
        for downloaded_trained_model_file_path in downloaded_trained_model_file_paths:
            new_model_dir_file_paths.append(ModelOperationProcessor._process_model_dir_file_replacement(
                original_model_dir_absolute_path, downloaded_trained_model_file_path))

        logger.info('Success to replace the trained model dir by the downloaded model dir from Azure blob.\n'
                    f'Operation request tracking id: {self._request_id}.')
        return new_model_dir_file_paths

    def _zip_updated_model(self):
        """
        Re-zip the model after finishing the trained model dir replacement.

        :return: updated_model_file_path: str. The re-zip model's local file path.
        """
        if not os.path.exists(self._model_rezip_root):
            os.makedirs(self._model_rezip_root)

        # the local file path for the to-be-zipped updated model.
        updated_model_file_path_zip = os.path.join(self._model_rezip_root, f'{self._model_name}.zip')

        # here, the extra '/' is necessary,
        # if not, the re-zip zip file will contain the current dir 'zip_origin_dir_path'
        updated_model_source_dir_path = os.path.join(self._model_extract_root, f'{self._model_name}/')

        with zipfile.ZipFile(updated_model_file_path_zip, 'w') as rezip_file:
            pre_len = len(os.path.dirname(updated_model_source_dir_path))
            for parent, dir_names, file_names in os.walk(updated_model_source_dir_path):
                for file_name in file_names:
                    path_file = os.path.join(parent, file_name)
                    arcname = path_file[pre_len:].strip(os.path.sep)
                    rezip_file.write(path_file, arcname, zipfile.ZIP_DEFLATED)

        updated_model_file_path = os.path.join(self._model_rezip_root, self._model_name)
        if os.path.isfile(updated_model_file_path_zip):
            if os.path.isfile(updated_model_file_path):
                os.remove(updated_model_file_path)
            os.renames(updated_model_file_path_zip, updated_model_file_path)
        else:
            logger.error('Error occurred when re-zip the already-update model dir, '
                         f'the re-zip source dir: {updated_model_source_dir_path}, model name: {self._model_name}.')
            raise FileNotFoundError('Try again!\n Inner error when processing the original to-be-replaced model.')

        logger.info('Success to zip the local updated model! '
                    f'Updated model local path: {updated_model_file_path}.\n'
                    f'Operation request tracking id: {self._request_id}.')
        return updated_model_file_path

    def _register_updated_model(self, updated_model_file_path):
        """
        Register the locally updated model(replace the trained model dir locally) to workspace.

        :param updated_model_file_path: str. The to-be-registered model's local file path.
        :return: updated_model_id: str. The new registered model's model id if no errors, exceptions otherwise.
        """
        model_management_helper = ModelManagementServiceHelper(self._azureml_workspace_processor)
        updated_model_id = model_management_helper.register_updated_model(self._model_name,
                                                                          updated_model_file_path,
                                                                          self._original_model_version)
        logger.info(f'Succeed to register the local updated model, updated model id: {updated_model_id}.\n'
                    f'Operation request tracking id: {self._request_id}.')
        return updated_model_id

    # init and destroy the temporary directories
    def _init_sub_dirs(self):
        """
        Create the temporary directories for ModelOperationProcessor.

        :return:
        """
        ModelOperationProcessor._init_sub_dir(self._blob_trained_model_download_root)
        ModelOperationProcessor._init_sub_dir(self._model_download_root)
        ModelOperationProcessor._init_sub_dir(self._model_extract_root)
        ModelOperationProcessor._init_sub_dir(self._model_rezip_root)

    @staticmethod
    def _init_sub_dir(dir_path):
        """
        Create a temporary directory by the given local dir path.

        :param dir_path: str. The local dir path which should be created.
        :return:
        """
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(dir_path)

    @staticmethod
    def _destroy_sub_dir(dir_path):
        """
        Delete a directory and all the files inside by the given local dir path.

        :param dir_path: str. The local dir path which should be deleted.
        :return: not os.path.exists(dir_path): Bool. The flag whether the given dir has deleted.
        """
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        return not os.path.exists(dir_path)


class ModelManagementServiceHelper:
    """
    ModelManagementServiceHelper deals with the interaction with workspace.

    1.Download a model based on given model id from the workspace.

    2.Register a model from a local file to the workspace.
    """
    def __init__(self,
                 azureml_workspace_processor: AzuremlWorkspaceProcessor):
        """

        :param azureml_workspace_processor: the instance for creating and refreshing the target Workspace.
        """
        self._target_workspace = azureml_workspace_processor.get_aml_workspace_entity()

    def download_model_by_id(self, download_root, model_name, model_version):
        """
        Download model by given model id(combine model name and model version) to the given local dir path.

        :param download_root: str. The local dir path to save the downloaded model.
        :param model_name: str.
        :param model_version: int.
        :return: path: str. The local file path to save the downloaded model.
        """
        path = os.path.join(download_root, f'{model_name}.zip')
        try:
            model = Model(self._target_workspace, id=f'{model_name}:{model_version}')
            oldpath = model.download(download_root, exist_ok=True)
            # the target_dir="." param in model.download() should be exactly a dir path not a file path,
            # so the download model rename operation is necessary.
            if os.path.isfile(path):
                # to make sure when rename the download model xxx to xxx.zip, there is no xxx.zip exist before.
                os.remove(path)
            # rename the file with appending the postfix '.zip'
            os.rename(oldpath, path)
            logger.info(f'Success to download the desired Model! Local download path: {path}.\n'
                        f'Downloaded model id: {model_name}:{model_version}.')
            return path
        except Exception as e:
            error_msg = 'Fail to download original model from workspace.\n' \
                        f'workspace name: {self._target_workspace.name}, ' \
                        f'workspace resource group: {self._target_workspace.resource_group}, ' \
                        f'modelId: {model_name}:{model_version}.\n Error message: {e}'
            raise Exception(error_msg) from e

    def register_updated_model(self, model_name, updated_model_file_path, original_model_version):
        """
        Register a model from a local file to the workspace.

        :param model_name: str. The desired model name for the to-be-registered model.
        :param updated_model_file_path: str. The local file path where the to-be-registered model stores.
        :param original_model_version: int. Original model's model version, here only for logging.
        :return: model_registered.id: str. The registered model's id if no errors, exceptions otherwise.
        """
        if os.path.isfile(updated_model_file_path):
            pass
        else:
            logger.error('Error occurred when get the already-update model zip, '
                         f'the re-zip file temp path: {updated_model_file_path}, model name: {model_name}.')
            raise Exception('Try again! There occurs some file processing problems when updating the trained model.')

        try:
            model_registered = Model.register(workspace=self._target_workspace,
                                              model_path=updated_model_file_path,
                                              model_name=model_name,
                                              tags={'CreatedByAMLStudio': 'true',
                                                    model_name: 'Locally updated, original version: '
                                                                f'{original_model_version}'},
                                              description="Update model locally with pipeline run trained model.")
            logger.info('Success to register the local updated model!\n'
                        f'Original model id: {model_name}:{original_model_version}.\n'
                        f'Re-register model id: {model_registered.id}, local file path: {updated_model_file_path}.')
            return model_registered.id
        except Exception as e:
            error_msg = 'Fail to register new model to workspace.\n' \
                        f'workspace name: {self._target_workspace.name}, ' \
                        f'workspace resource group: {self._target_workspace.resource_group}, ' \
                        f'original model\'s modelId: {model_name}:{original_model_version}.\n Error message: {e}'
            raise Exception(error_msg) from e
