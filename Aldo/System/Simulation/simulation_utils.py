import yaml


def get_conf_from_yaml(conf_yaml_path_):
    with open(conf_yaml_path_, 'r') as conf_file_:
        conf_ = yaml.safe_load(conf_file_)
    return conf_
