# This module contains the functions that will validate the user input of user data

# Importing Regex module
import re

# Importing reading functions
import modules.file.read as fr

# Importing the Identifier Column
from __init__ import IDENTIFIER_COL as ID, PATH

def is_available(username):
    """Validate the availability of the input username
    
    Args:
        (str): the username to be validated
        
    Returns:
        (bool): whether the username is available or not"""

    # Get the users info
    users_lines = fr.get_lines(PATH['users'], 'list')

    # Iterating over the users data
    for user_line in users_lines:
        # Checking if the user is in the data
        if username == user_line[3]:
            # Return not available
            return False
    # Else return Available
    return True


def validate_username(username):
    """Validate the input username against set of rules
    
    Args:
        (str): the username to be validated
        
    Returns:
        (bool): whether the username is valid or not"""

    # Checking that the username starts and ends with a Letter and contains only
    # uppercase letters, lowercase letters, numbers, or an underscore.
    return re.fullmatch('^[A-z]+[A-z0-9_]*[A-z0-9]+$', username) != None


def validate_name(name):
    """Validate the input name against set of rules
    
    Args:
        (str): the name to be validated
        
    Returns:
        (bool): whether the name is valid or not"""

    # Checking that the name contains uppercase and lowercase charaters only
    return re.fullmatch('^[A-z]+$', name) != None


def validate_password(password):
    """Validate the input password against set of rules
    
    Args:
        (str): the password to be validated
        
    Returns:
        (bool): whether the password is valid or not"""

    # Check that the password is longer than 7 characters and contains at least
    # an uppercase letter, a lowercase letter, and a symbol
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$"

    # Return True if the password match validation
    return re.fullmatch(reg, password) != None


def confirm_password(initial_password, password_confirmation):
    """Validate the password confirmation against the initial password input
    
    Args:
        (str): the initial password to be validated against
        (str): the password confirmation to be validated
        
    Returns:
        (bool): whether the two password match"""
    
    # Return True if Initial Password is equal to confirm Password
    return True if initial_password == password_confirmation else False


def validate_email(email):
    """Validate that the input email address is valid
    
    Args:
        (str): the email address to be validated
        
    Returns:
        (bool): whether the email address is valid or not"""
    
    # Checking if the email matches the format user@example.com
    return re.fullmatch('^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', email) != None


def validate_mobile(mobile):
    """Validate the input mobile number against set of rules
    
    Args:
        (str): the mobile number to be validated
        
    Returns:
        (bool): whether the mobile number is valid or not"""
    
    # Checking if the mobile number matches the format 01xxxxxxxxx
    return re.fullmatch("^01[015][0-9]{8}$", mobile) != None
