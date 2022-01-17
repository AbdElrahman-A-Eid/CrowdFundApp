# Edit a project

import modules.file.read as fr
import modules.file.write as fw
from __init__ import PATH

def edit_project(id, data):
    """Edits a single project data depending on the id provided
    
    Args:
        (str): The id of the project to be edited
        (list): The uodated data as a list
        
    Returns:
        (bool): Whether the data update was successful or not"""
    try:
        projects_lines = fr.get_lines(PATH['projects'], 'list')

        for i, line in enumerate(projects_lines):
            if int(line[0]) == id:
                projects_lines[i] = data
                break

        fw.replace_content('projects', projects_lines)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return False
    else:
        return True