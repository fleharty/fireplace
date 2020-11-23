#!/usr/bin/env python3

import argparse
import firecloud.api as fapi


# TODO: get these from command-line arguments
namespace = "broad-firecloud-dsde-methods"
workspace = "FireplaceSample"


def getstuff(namespace, workspace):
    #workspace = fapi.get_workspace(namespace, workspace)
    #print(workspace.json())
    #method_configurations = fapi.get_method_configurations(namespace, workspace)
    workspace_configs = fapi.list_workspace_configs(namespace, workspace)

    for workspace_config in workspace_configs.json():
        print(workspace_config)

    for workspace_config in workspace_configs.json():
        workspace_config_namespace = workspace_config["namespace"]
        workspace_config_name = workspace_config["name"]

        workspace_config_details = fapi.get_workspace_config(namespace, workspace, workspace_config_namespace, workspace_config_name)
        print(workspace_config_details.json())

        method_namespace = workspace_config["methodRepoMethod"]["methodNamespace"]
        method_name = workspace_config["methodRepoMethod"]["methodName"]
        method_version = workspace_config["methodRepoMethod"]["methodVersion"]

        inputs_outputs = fapi.get_inputs_outputs(method_namespace, method_name, method_version)
        # print(input_outputs.json())

        inputs_outputs_json = inputs_outputs.json()
        print(inputs_outputs_json)
        # input_types = { n:t for (n,t) in inputs_outputs_json["inputs"].items }
        input_details = {}
        for i in inputs_outputs_json["inputs"]:
            input_details[i["name"]] = i

        inputs = workspace_config_details.json()["inputs"]
        for input_name in inputs:
            [task_name, variable] = input_name.split(".")
            print(task_name + "\t" + variable + "\t" + inputs[input_name] + "\t" + input_details[input_name]["inputType"] + "\t" + str(input_details[input_name]["optional"]))


getstuff(namespace, workspace)

#fapi.get_workspace_config(namespace, workspace, )

#print(workspace.json())
