# New User Registration

# Import user validators module
import modules.user.user_validators as uv

# Import file writing module
import modules.file.write as fw

# Import the files PATH
from __init__ import PATH

# Defining a function to validate all the user details before registering


def check_user_data(data):
    """Check the user data against the validators

    Args:
        (list): the data and details of the user to be validated

    Returns:
        (list): list of booleans representing valid data items"""

    # Initializing a list with the respective validity
    result = [[uv.validate_username(data[0]), uv.is_available(data[0])], uv.validate_password(data[1]), uv.confirm_password(
        data[1], data[2]), uv.validate_name(data[3]), uv.validate_name(data[4]), uv.validate_email(data[5]), uv.validate_mobile(data[6])]

    return result

# Defining the registration function


def register_user(details_list):
    """Register the user details into the database file

    Args:
        (list): the data and details of the user to be registered

    Returns:
        (bool): whether the registration operation is successful or not"""

    try:
        fw.add_entry('users', details_list)
        fw.add_entry('profiles', [details_list[0], '', '', '', '', '', 'default.jpg'])
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return False
    else:
        return True
