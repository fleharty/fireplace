#!/usr/bin/env python3
import csv
import pandas as pd
import argparse
import firecloud.api as fapi

parser = argparse.ArgumentParser(description='Download Terra Workspace.')
parser.add_argument('--namespace', dest='namespace', default = "broad-firecloud-dsde-methods")
parser.add_argument('--workspace', dest='workspace', default = "FireplaceSample")
args = parser.parse_args()


def get_inputs(config, input_details):
    inputs = config["inputs"]
    return [[*k.split("."), v, input_details[k]["inputType"], str(input_details[k]["optional"])]
            for k, v in sorted(inputs.items())]


def get_outputs(config, output_details):
    outputs = config["outputs"]
    return [[*k.split("."), v, output_details[k]["outputType"]]
            for k, v in sorted(outputs.items())]


def getstuff(namespace, workspace):
    workspace_configs = fapi.list_workspace_configs(namespace, workspace)

    for workspace_config in workspace_configs.json():
        workspace_config_namespace = workspace_config["namespace"]
        workspace_config_name = workspace_config["name"]

        workspace_config_details = fapi.get_workspace_config(namespace, workspace, workspace_config_namespace, workspace_config_name)
        # print(workspace_config_details.json())

        method_namespace = workspace_config["methodRepoMethod"]["methodNamespace"]
        method_name = workspace_config["methodRepoMethod"]["methodName"]
        method_version = workspace_config["methodRepoMethod"]["methodVersion"]

        inputs_outputs = fapi.get_inputs_outputs(method_namespace, method_name, method_version)
        # print(input_outputs.json())

        inputs_outputs_json = inputs_outputs.json()

        input_details = {i["name"]: i for i in inputs_outputs_json["inputs"]}
        config_inputs = get_inputs(workspace_config_details.json(), input_details)
        print(f"{config_inputs}")

        output_details = {i["name"]: i for i in inputs_outputs_json["outputs"]}
        config_outputs = get_outputs(workspace_config_details.json(), output_details)
        print(f"{config_outputs}")

        # Get WDL associated with method
        wdl_content = fapi.get_repository_method(method_namespace, method_name, method_version).json()["payload"]
        fwdl = open(f"{method_namespace}.{method_name}.{method_version}.wdl", "w")
        fwdl.write(wdl_content)
        fwdl.close()

        writeVariablesToFile(f"{method_namespace}.{method_name}.{method_version}.inputs.tsv", config_inputs)
        writeVariablesToFile(f"{method_namespace}.{method_name}.{method_version}.outputs.tsv", config_outputs)


def writeVariablesToFile(filename, content):

    with open(filename, 'w', newline='\n', encoding='utf-8') as f:

        writer = csv.writer(f, delimiter = '\t', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(["Taskname", "Variable", "Value", "Type", "Required"])
        writer.writerows(content)

getstuff(args.namespace, args.workspace)

#fapi.get_workspace_config(namespace, workspace, )

#print(workspace.json())
