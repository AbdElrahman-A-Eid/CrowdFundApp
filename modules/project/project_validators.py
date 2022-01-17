# This module contains the functions that will validate the user input of project data

# Importing Regex module
import re

# Import datetime
from datetime import datetime

def validate_title(title):
    """Validate the input title against set of rules
    
    Args:
        (str): the title to be validated
        
    Returns:
        (bool): whether the title is valid or not"""
    # Checking that the title contains uppercase and lowercase charaters and digits only
    return re.fullmatch("^[A-z\s'\d-]+$", title) != None

def validate_description(description):
    """Validate the input description against set of rules
    
    Args:
        (str): the description to be validated
        
    Returns:
        (bool): whether the description is valid or not"""

    return re.fullmatch("^[A-z0-9\.,-_\?\!@\*\s\(\)'\"]+$", description) != None

def validate_target(target):
    """Validate the input fund target against set of rules
    
    Args:
        (int): the fund target to be validated
        
    Returns:
        (bool): whether the fund target is valid or not"""
    # Checking that the target is a positive integer
    return True if target.isnumeric() and int(target) > 0 else False


def validate_date(date):
    """Validate the input project date against set of rules
    
    Args:
        (str): the project date to be validated
        
    Returns:
        (bool): whether the date is valid or not"""
    
    return True if re.fullmatch("^([1-9]|1[0-9]|2[0-9]|3[0-1])\/(0?[1-9]|1[0-2])\/\d{4}$", date) != None else False


def validate_start_date(start_date):
    """Validate the input project start date/time against set of rules
    
    Args:
        (datetime): the project start date/time to be validated
        
    Returns:
        (bool): whether the date/time is valid or not"""
    
    # Check that the start date is not before today's date
    return True if datetime.now() <= datetime.strptime(start_date, '%d/%m/%Y') else False


def validate_end_date(end_date, start_date):
    """Validate the input project end date/time against set of rules
    
    Args:
        (str): the project end date/time to be validated
        
    Returns:
        (bool): whether the date/time is valid or not"""

    # Check that the end date is not before today's date
    return True if (datetime.now() < datetime.strptime(end_date, '%d/%m/%Y') and datetime.strptime(end_date, '%d/%m/%Y') >= datetime.strptime(start_date, '%d/%m/%Y')) else False