import copy
import os
import os.path
# noinspection PyPackageRequirements
import yaml

default_config = {
    "credentials": {
        "path": "/home/parndt/Vault/creds.yaml"
    },
    "emr": {
        "name": "demo-cluster",
        "worker-count": 2,
        "region": "us-west-2",
        "instance-type": "r4.2xlarge",
        "spot-price": 1.0,
        "open-firewall": "false"
    },
    "jupyter": {
        "password": "ChangeMe321"
    }
}


class Config:

    def __init__(self, file_path="./config.yaml"):
        self.config = dict()
        self.file_path = file_path
        self.load()

    def load(self):
        self.config = copy.deepcopy(default_config)

        if os.path.isfile(self.file_path):
            with open(self.file_path, 'r') as stream:
                file_yaml = yaml.load(stream)
                self.config["credentials"].update(file_yaml["credentials"])
                self.config["emr"].update(file_yaml["emr"])
                self.config["jupyter"].update(file_yaml["jupyter"])

    def save(self):
        with open(self.file_path, 'w') as stream:
            stream.write(yaml.safe_dump(self.config, default_flow_style=False))
