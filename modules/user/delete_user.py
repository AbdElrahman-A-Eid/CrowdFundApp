# Delete a user account

import modules.file.read as fr
import modules.file.write as fw
from __init__ import PATH
import os


def delete_account(id):
    try:
        users_lines = fr.get_lines(PATH['users'], 'list')
        profiles_lines = fr.get_lines(PATH['profiles'], 'list')

        for i, line in enumerate(users_lines):
            if int(line[0]) == id:
                del users_lines[i]
                break

        for i, line in enumerate(profiles_lines):
            if int(line[0]) == id:
                del profiles_lines[i]
                try:
                    os.remove(PATH['imgs'] + line[-1])
                except Exception as e:
                    print(f"{type(e).__name__}: {e}")
                break

        fw.replace_content('users', users_lines)
        fw.replace_content('profiles', profiles_lines)

    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return False
    else:
        return True