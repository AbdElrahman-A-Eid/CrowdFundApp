# Edit a user profile

from sys import modules
import modules.file.read as fr
import modules.file.write as fw
import modules.project.project_validators as pv
from __init__ import PATH

# Defining a function to validate all the profile details before editing


def check_profile_data(data):
    """Check the profile data against the validators

    Args:
        (list): the data and details of the profile items to be validated

    Returns:
        (list): list of booleans representing valid data items"""

    # Initializing a list with the respective validity
    result = [pv.validate_title(data[1]), pv.validate_title(data[2]), pv.validate_description(data[3]), pv.validate_title(data[4]), pv.validate_title(data[5])]

    return result


def edit_profile(id, data):
    """Edits a single user profile depending on the logged user ID
    
    Args:
        (list): The uodated data as a list
        
    Returns:
        (bool): Whether the data update was successful or not"""
    try:
        profile_lines = fr.get_lines(PATH['profiles'], 'list')

        for i, line in enumerate(profile_lines):
            if int(line[0]) == id:
                profile_lines[i] = data
                break

        fw.replace_content('profiles', profile_lines)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return False
    else:
        return True