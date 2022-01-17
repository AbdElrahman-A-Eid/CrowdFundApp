# Functionalities related to searching in a file

import modules.file.read as fr
from __init__ import IDENTIFIER_COL, PATH

def get_item_details(file, identifier):
    """Extract the item details from database
    
    Args:
        (str): the file to search for the item in
        (str|int): the identifier of the item being queried
        
    Returns:
        (list|None): list of the item details if exist and None otherwise"""

    # Extracting users data from database as list of lists
    items_data = fr.get_lines(PATH[file], type='list')

    # Iterating over the users data
    for item in items_data:

        # Checking the items identifiers against the queried identifier
        if item[IDENTIFIER_COL[file]] == identifier:
            # if found return the data
            return item

    # If the identifier is not found return None
    return None