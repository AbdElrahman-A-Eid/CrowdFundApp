# Logging a user in

import modules.file.write as fw
import modules.file.search as fs
from __init__ import PATH
from datetime import datetime

def authenticate_user(login_details):
    """Validating the login details against the database
    
    Args:
        (list): a list containing the username and password of the user
        
    Returns:
        (bool): whether the login details are correct or not"""

    # Retrieve user details from the database
    user_data = fs.get_item_details('users', login_details[0])

    if user_data:
        return True if user_data[5] == login_details[1] else False

    return False

def login_user(username):
    """Perform the action of logging a user in
    
    Args:
        (str): the username of the user to be logged in
        
    Returns:
        (bool): whether the login operation was successfull"""

    try:
        login_details = [username, datetime.now().strftime("%d/%m/%Y %H:%M:%S")]
        fw.replace_content('logged', [login_details])
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return False
    else:
        return True