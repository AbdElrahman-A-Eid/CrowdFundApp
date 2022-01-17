import json, os

dirname = os.path.dirname(__file__)

config = {}

# Defining a function that reloads the configurations
def reload_config():
    """Reloads configuration variables from the config.json file
    
    Returns:
        (bool): whether reload was successful or not"""

    with open(dirname + '/' + 'database/config.json', 'r') as file:
        global config
        config = json.load(file)
        for key, value in config['path'].items():
            config['path'][key] = dirname + '/' + value



reload_config()

    
# Delimiter Initialization
delimiter = config['delimiter']

# Initializing file paths/names
PATH = config['path']

# Initializing the identifier col that the item can be searched with in the file
IDENTIFIER_COL = config['identifierCol']