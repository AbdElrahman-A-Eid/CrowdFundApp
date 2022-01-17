# Delete a project

import modules.file.read as fr
import modules.file.write as fw
from __init__ import PATH


def delete_project(id):
    try:
        projects_lines = fr.get_lines(PATH['projects'], 'list')

        for i, line in enumerate(projects_lines):
            if int(line[0]) == id:
                del projects_lines[i]
                break

        fw.replace_content('projects', projects_lines)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return False
    else:
        return True