# Logging a user out

import modules.file.write as fw
from __init__ import PATH

def logout_user():
    """Perform the action of logging a user out
        
    Returns:
        (bool): whether the login operation was successfull"""

    try:
        fw.replace_content('logged', [''])
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return False
    else:
        return True