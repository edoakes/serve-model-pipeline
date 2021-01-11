import argparse
import json
import yaml

import ray
from ray import serve
from ray.serve.backends import ImportedBackend

ray.init(address="auto")
client = serve.connect()

parser = argparse.ArgumentParser()
parser.add_argument("config_file")

def main(config_file):
    with open(config_file) as f:
        config = json.load(f)

    names = []
    for model in config["models"]:
        client.create_backend(model["name"], ImportedBackend(model["class"]), *model.get("args", []), config=serve.BackendConfig(**model.get("config", {})))
        client.create_endpoint(model["name"], backend=model["name"])
        names.append(model["name"])
    
    client.create_backend(config["name"], ImportedBackend("serve_pipeline.ModelPipeline"), names)
    client.create_endpoint(config["name"], backend=config["name"], route=config.get("route", None))

if __name__ == "__main__":
    main(parser.parse_args().config_file)
