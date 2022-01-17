# Functionalities related to writing to a file

# Import the delimiter
from __init__ import delimiter

# Import the PATH of files
from __init__ import PATH

# Import the reload_config function
from __init__ import reload_config

# Import reading functions
import modules.file.read as fr

# Import JSON module
import json

def add_entry(file_name, data):
    """Adds new entry to the specified file with certain settings
    
    Args:
        (str): the path to the file to be written to
        (ListObject): the data to be appended
        
    Returns:
        (bool): whether entry addition was successful or not"""

    # Convert the list of data into the appropriate format for storage
    data = delimiter.join(data)

    # Adding a new line charater at the end
    data += '\n'

    with open(PATH[file_name], 'a') as file:
        # Writing the line into file
        file.write(data)


def replace_content(file_name, data):
    """Overwrite the content of the specified file
    
    Args:
        (str): the path to the file to be overwritten
        (ListObject): the data to be replaced as a list of lists
        
    Returns:
        (bool): whether overwriting was successful or not"""

    try:
        # Iterating over each line in the data list
        for i, line in enumerate(data):
            # Convert the list of data into the appropriate format for storage
            line = delimiter.join(line)

            # Adding a new line charater at the end
            line += '\n'

            # Replacing the item in the orignal list
            data[i] = line

        # Using a context manager to overwrite the file
        with open(PATH[file_name], 'w') as file:
            # Writing the data into file
            file.writelines(data)

    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return False
    else:
        return True


# Function to change delimiter
# def change_delimiter(new_delimiter):
#     """Change the current file delimiter
    
#     Args:
#         (str): the new delimter to be used in the file
        
#     Returns:
#         (bool): whether the delimiter replacement was successful or not"""

#     try:

#         # Initialize content of __init__.py file
#         content = ''

#         # Using a context manager to read the file
#         with open('__init__.py', 'r') as init_file:
#             # Extract the file content
#             content = init_file.read()
#             # Change the delimiter
#             content = content.replace("delimiter = '" + delimiter + "'", "delimiter = '" + new_delimiter + "'")

#         # Using a context manager to overwrite the file
#         with open('__init__.py', 'w') as init_file:
#             # Rewrite the __init__.py file
#             init_file.write(content)

#         # Loop over the file paths
#         for key in PATH:
#             # Retrieve the file lines as a list of lists
#             lines = fr.get_lines(PATH[key], type='list')

#             # Replace the file content with the new delimiter
#             replace_content(PATH[key], lines)

#     except Exception as e:
#         print(f"{type(e).__name__}: {e}")
#         return False
#     else:
#         return True


# Function to change delimiter
def change_delimiter(new_delimiter):
    """Change the current file delimiter
    
    Args:
        (str): the new delimter to be used in the file
        
    Returns:
        (bool): whether the delimiter replacement was successful or not"""

    try:

        # Initialize content of config.json file
        conf = {}

        # Using a context manager to read the file
        with open(PATH['config']) as conf_file:
            # Read the configuration from the file
            conf = json.load(conf_file)

        # Using a context manager to overwrite the file
        with open(PATH['config'], 'w') as conf_file:
            # Change the delimiter
            conf['delimiter'] = new_delimiter
            # write the edited configuration to the file
            json.dump(conf, conf_file)

        # Reloading the current app config from the config.json file
        reload_config()

        # Loop over the file paths
        for key in ['users', 'projects']:
            # Retrieve the file lines as a list of lists
            lines = fr.get_lines(PATH[key], type='list')

            # Replace the file content with the new delimiter
            replace_content(PATH[key], lines)

    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return False
    else:
        return True

