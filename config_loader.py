import yaml

def read(query):
    with open("config.yaml") as config_file:
        data = yaml.safe_load(config_file)
    return eval(query)