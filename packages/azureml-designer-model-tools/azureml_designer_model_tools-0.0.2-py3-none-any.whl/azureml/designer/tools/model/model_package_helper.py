import os
from azureml.designer.serving.dagengine import graph_spec


class ModelPackageHelper:
    """
    ModelPackageHelper deals with finding the trained model dir relative path in a model's 'modelpackage.json' file.

    1.Find the trained model dir relative path.
    """
    @staticmethod
    def get_model_dir_relative_path(model_package_json_path):
        """
        From the extracted zip model file, there is a 'modelpackage.json' file,
        it has all the information of this model. In ModelOperationProcessor, the trained model dir should be replaced.
        Its relative dir path is like "/resource/0". So here is necessary to serialize 'modelpackage.json' file
        to find the relative dir path in extracted zip model file.
        Then this relative dir will be replaced by a user-given trained model dir.

        :param model_package_json_path: str. The local file path of 'modelpackage.json' file in the extracted model dir.
        :return: trained_model_dir_relative_path: str. The relative 'modelpackage.json' file path if no errors,
            exceptions otherwise.
        """
        if not os.path.isfile(model_package_json_path):
            raise FileNotFoundError("The current service model's model_package file is not found!"
                                    f"Not found local model_package file path: {model_package_json_path}.\n"
                                    "Check modelpackage.json file in the current model of your given service.")

        model_package = graph_spec.GraphSpec.load(model_package_json_path)

        # traverse all the staticsources in this model to search the desired replaced dir
        model_directories = [static_source for _, static_source in model_package.static_sources.items() if
                             static_source.data_type_id == 'ModelDirectory']
        # the ModelDirectory static sources count, to detect the duplication
        model_directories_count = len(model_directories)
        if model_directories_count == 1:
            trained_model_dir_relative_path = model_directories[0].file_path
        else:
            # detect the duplication
            raise Exception(f'There are {model_directories_count} model directories in current model!\n'
                            'Designer only supports service update with only 1 model inference graph in a model.')
        if trained_model_dir_relative_path == '':
            raise Exception("There is no value assigned to trained model relative file path!"
                            "The current given service's model has no model inference graph!")
        # return relative path like "/resource/0".
        return trained_model_dir_relative_path
