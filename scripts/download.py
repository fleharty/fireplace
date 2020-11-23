#!/usr/bin/env python3

import argparse
import firecloud.api as fapi


namespace = "broad-firecloud-dsde-methods"
workspace = "FireplaceSample"


def getstuff(namespace, workspace):
    for config in configs.json():
        config_namespace = config["namespace"]
        config_name = config["name"]

        method_config = fapi.get_workspace_config(namespace, workspace, config_namespace, config_name)

        method_namespace = config["methodRepoMethod"]["methodNamespace"]
        method_name = config["methodRepoMethod"]["methodName"]
        method_version = config["methodRepoMethod"]["methodVersion"]

        input_outputs = fapi.get_inputs_outputs(method_namespace, method_name, method_version)
        print(input_outputs.json())

#workspace = fapi.get_workspace(namespace, workspace)
#print(workspace.json())
#method_configurations = fapi.get_method_configurations(namespace, workspace)
configs = fapi.list_workspace_configs(namespace, workspace)

for config in configs:
   print(config)



#fapi.get_workspace_config(namespace, workspace, )

#print(workspace.json())