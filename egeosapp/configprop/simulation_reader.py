import configparser

def read_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)

    if 'DEFAULT' not in config:
        raise ValueError("Configuration file must have a [DEFAULT] section")

    return config['DEFAULT']


