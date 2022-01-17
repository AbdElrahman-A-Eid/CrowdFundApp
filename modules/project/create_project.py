# Create new project

# Import user validators module
import modules.project.project_validators as pv

# Import file writing module
import modules.file.write as fw

# Import the files PATH
from __init__ import PATH

# Defining a function to validate all the project details before creation


def check_project_data(data):
    """Check the project data against the validators

    Args:
        (list): the data and details of the project to be validated

    Returns:
        (list): list of booleans representing valid data items"""

    # Initializing a list with the respective validity
    result = [pv.validate_title(data[0]), pv.validate_description(data[1]), pv.validate_target(data[2]), pv.validate_date(
        data[3]) and pv.validate_start_date(data[3]), pv.validate_date(data[4]) and pv.validate_end_date(data[4], data[3])]

    return result

# Defining the registration function


def create_project(details_list):
    """Register the project details into the database file

    Args:
        (list): the data and details of the project to be registered

    Returns:
        (bool): whether the registration operation is successful or not"""

    try:
        fw.add_entry('projects', details_list)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return False
    else:
        return True
