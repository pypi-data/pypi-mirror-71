import argparse
from azureml.designer.tools.model.entry_function import model_tools_entry


def main():
    """
    Tool entry function which allows the cmd-line parameter passing.

    :return:
    """
    # test the pkg tool by enter param in cmd
    parser = argparse.ArgumentParser()
    # connect to the desired workspace
    parser.add_argument("-sub", "--subscription_id", type=str, required=True,
                        help="the subscription id for connecting the target workspace")
    parser.add_argument("-r", "--resource_group", type=str, required=True,
                        help="the resource group for connecting the target workspace")
    parser.add_argument("-w", "--workspace_name", type=str, required=True,
                        help="the workspace name for connecting the target workspace")
    # get the to be redeployed endpoint's name
    parser.add_argument("-s", "--service_endpoint_name", type=str, required=True,
                        help="the name of your current service endpoint")

    parser.add_argument("-p", "--pipeline_run_id", type=str, required=True,
                        help="the id for your new pipeline run")

    parser.add_argument("-d", "--update_description", type=str,
                        help="the description for your this time's redeployment")

    args = parser.parse_args()

    state = model_tools_entry(args.subscription_id,
                              args.resource_group,
                              args.workspace_name,
                              args.pipeline_run_id,
                              args.service_endpoint_name,
                              update_description=args.update_description)
    return state


if __name__ == '__main__':
    main()
