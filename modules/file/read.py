# Functionalities related to reading from a file

# Import the delimiter
from __init__ import PATH, delimiter

# Import searching
import modules.file.search as fs

# Define a function to read file lines
def get_lines(path, type='str'):
    """Extract the file lines either as list of strings or list of lists
    
    Args:
        (str): path to the file to be read
        (str): [optional] the type of return ('str' or 'list') (by default return will be list of strings
        
    Return:
        (list): a list of lines either as strings or lists"""

    # Creating a context manager to handle the file
    with open(path) as file_obj:
        
        # Read the file lines as strings
        file_lines = file_obj.readlines()

        if (type == 'list'):
            # Loop over the file lines extracted as string
            for i, line in enumerate(file_lines):
                # Removing the new line charater at the end of the file
                line = line.replace('\n', "")
                # Using delimiter to split over the line into a list 
                # and reassigning the list to the original lines list
                file_lines[i] = line.split(delimiter)

        return file_lines


def get_logged_user():
    
    with open(PATH['logged']) as logged_file:
        username = logged_file.read().split(delimiter)[0]
        user_data = fs.get_item_details('users', username)

        return user_data
        