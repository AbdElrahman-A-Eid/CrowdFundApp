import modules.file.read as fr
import modules.file.write as fw
import modules.user.login as ul
import modules.user.logout as uo
import modules.user.register as ur
import modules.user.user_validators as uv
import modules.project.create_project as pc
import modules.project.view_projects as pvi
import modules.project.edit_project as pe
import modules.project.project_validators as pv
from __init__ import PATH
import time, os
from getpass import getpass

def logged_menu():
    logged = 1
    while logged:
        logged_user, op = get_operation()
        
        if op == '1':
            os.system('clear')
            print("######## Project Creation ########\n")

            title, description, target, start_date, end_date = project_data_input()
            
            project_data = [str(int(fr.get_lines(PATH['projects'], 'list')[-1][0])+1), title, description, logged_user[0], target, start_date, end_date]
            if pc.create_project(project_data):
                print("Project Creation was Successful!")
                print("You will be redirected to the user menu shortly.")
                time.sleep(3)
            else:
                print("An error occured! Please try again later. if error persists, call our support!")
                time.sleep(6)
            op = '0'

        if op == '2':
            print_user_projects(logged_user)

        if op == '3':
            os.system('clear')
            print("######## All Projects ########\n")
            project_lines = fr.get_lines(PATH['projects'], 'list')
            for i, project in enumerate(project_lines):
                pvi.view_project(project)
                if i + 1 < len(project_lines):
                    print("\n---------------------------\n")
            input("\nPress Return key to go back!")

        if op == '4':
            os.system('clear')
            print("######## Delete Projects ########\n")
            
            delete_user_project(logged_user)
                
        
        if op == '5':
            os.system('clear')
            print("######## Edit Projects ########\n")
            
            edit_user_project(logged_user)
            
        if op == '6':
            os.system('clear')
            print("######## Logout Screen ########\n")
            print("Logging you out...\n")
            if uo.logout_user():
                print("\nYou are logged out successfully!\nyou will be redirected to main menu shortly!")
                logged = 0
                time.sleep(4)
            else:
                print("We have encountered a problem. Please try again later!")

def edit_user_project(logged_user):
    project_lines = fr.get_lines(PATH['projects'], 'list')
    user_projects = [project for project in project_lines if project[3] == logged_user[0]]

    if len(user_projects) > 0:
        ids = []
        print("---- My Projects ----\n")
        for i, project in enumerate(user_projects):
            ids.append(project[0])
            pvi.view_project(project)
            if i + 1 < len(user_projects):
                print("\n---------------------------\n")
        p_id = input("\nChoose the project ID to edit: ")
        while p_id not in ids:
            p_id = input("\nChoose the project ID to edit: ")
                
        for i, project in enumerate(project_lines):
            if project[0] == p_id:
                get_updated_project_values(project)
                pe.edit_project(p_id, project)
                break

        fw.replace_content('projects', project_lines)
    else:
        input("\nYou don't have projects yet!\nPress Return key to go back!")

def get_updated_project_values(project):
    print("You can either update the values or press Enter to keep the old value:\n")

    while True:
        title = input(f"\tProject Title [{project[1]}]: ")
        if pv.validate_title(title) or title == '':
            break
        else:
            print("Please enter a title containing only lowercase or uppercase latin letters!")
                        
    while True:
        description = input(f"\tProject Description [{project[2][:10]}...]: ")
        if pv.validate_description(description) or description == '':
            break
        else:
            print("Descriptions allow latin letters, digits, and the following\nspecial characters (),.-_@*?! only!")

    while True:
        target = input(f"\tProject Target [{project[4]}]: ")
        if pv.validate_target(target) or target == '':
            break
        else:
            print("Total target must be a positive integer!")

    while True:
        start_date = input(f"\tProject Start Date [{project[5]}]: ")
        if (pv.validate_date(start_date) and pv.validate_start_date(start_date)) or start_date == '':
            break
        elif pv.validate_date(start_date):
            print("Start date must not be older than today's date")
        else:
            print("Please enter a valid date with the format dd/mm/YYYY!")

    while True:
        end_date = input(f"\tProject End Date [{project[6]}]: ")
        if (pv.validate_date(end_date) and pv.validate_end_date(end_date, (start_date or project[5]))) or end_date == '':
            break
        elif pv.validate_date(end_date):
            print("End date must not be older than tomorrow's date and at newer or equal to start date")
        else:
            print("Please enter a valid date with the format dd/mm/YYYY!")
                        
    new_data = ['', title, description, '', target, start_date, end_date]

    for i, item in enumerate(new_data):
        if item != '':
            project[i] = item

def delete_user_project(logged_user):
    project_lines = fr.get_lines(PATH['projects'], 'list')
    user_projects = [project for project in project_lines if project[3] == logged_user[0]]

    if len(user_projects) > 0:
        ids = []
        print("---- My Projects ----\n")
        for i, project in enumerate(user_projects):
            ids.append(project[0])
            pvi.view_project(project)
            if i + 1 < len(user_projects):
                print("\n---------------------------\n")
        p_id = input("\nChoose the project ID to delete: ")
        while p_id not in ids:
            p_id = input("\nChoose the project ID to delete: ")
                
        for i, project in enumerate(project_lines):
            if project[0] == p_id:
                del project_lines[i]

        fw.replace_content('projects', project_lines)
    else:
        input("\nYou don't have projects yet!\nPress Return key to go back!")

def print_user_projects(logged_user):
    os.system('clear')
    print("######## My Projects ########\n")
    project_lines = fr.get_lines(PATH['projects'], 'list')
    user_projects = [project for project in project_lines if project[3] == logged_user[0]]
    if len(user_projects) > 0:
        for i, project in enumerate(user_projects):
            pvi.view_project(project)
            if i + 1 < len(user_projects):
                print("\n---------------------------\n")
        input("\nPress Return key to go back!")
    else:
        input("\nYou don't have projects yet!\nPress Return key to go back!")

def project_data_input():
    while True:
        title = input("\tProject Title: ")
        if pv.validate_title(title):
            break
        else:
            print("Please enter a title containing only lowercase and uppercase latin letters with digits!")
            
    while True:
        description = input("\tProject Description: ")
        if pv.validate_description(description):
            break
        else:
            print("Descriptions allow latin letters, digits, and the following\nspecial characters (),.-_@*?! only!")

    while True:
        target = input("\tProject Target: ")
        if pv.validate_target(target):
            break
        else:
            print("Total target must be a positive integer!")

    while True:
        start_date = input("\tProject Start Date: ")
        if pv.validate_date(start_date) and pv.validate_start_date(start_date):
            break
        elif pv.validate_date(start_date):
            print("Start date must not be older than today's date")
        else:
            print("Please enter a valid date with the format dd/mm/YYYY!")

    while True:
        end_date = input("\tProject End Date: ")
        if pv.validate_date(end_date) and pv.validate_end_date(end_date, start_date):
            break
        elif pv.validate_date(end_date):
            print("End date must not be older than tomorrow's date and at newer or equal to start date")
        else:
            print("Please enter a valid date with the format dd/mm/YYYY!")
    return title,description,target,start_date,end_date

def get_operation():
    os.system('clear')
    logged_user = fr.get_logged_user()
    print("######## Yinshe's CrowdFund App ########\n")
    print(f"---- Logged in as: {logged_user[3]} ----\n")
    op = '0'
    while int(op) not in (1, 2, 3, 4, 5, 6):
        op = input("\nYou can choose any of the following operations:\n\t1. Create Project\n\t2. View My Projects\n\t3. View All Projects\n\t4. Delete Project\n\t5. Edit Projects\n\t6. Logout\n\nPlease choose the operation you want (number of the item): ")
        if not op.isnumeric():
            op = '0'
    return logged_user,op
    


def main():
    os.system('clear')
    op = '0'
    while op != '3':
        print("Welcome to Yinshe's CrowdFund App\n")
        while int(op) not in (1, 2, 3):
            op = input("\nYou can choose any of the following operations:\n\t1. Login with existing account\n\t2. Register a new account\n\t3. Exit the app\n\nPlease choose the operation you want (number of the item): ")
            if not op.isnumeric():
                op = '0'

        if op == '1':
            authenticated = 0
            while not authenticated:
                os.system('clear')
                print("######## Yinshe's CrowdFund App ########\n")
                print("---- Login Page ----\n")

                print("Please enter your credentials:\n")
                username = input("\tUsername: ")
                password = getpass("\tPassword: ")

                print("\nAuthenticating...")

                if not ul.authenticate_user([username, password]):
                    print("\nWrong Username or Password! Please try again!")
                    time.sleep(3)
                else:
                    authenticated = 1
                    ul.login_user(username)
                    logged_menu()
                    op = '0'
                    os.system('clear')

        elif op == '2':
            os.system('clear')
            print("######## Yinshe's CrowdFund App ########\n")
            print("---- Registration Page ----\n")
            print("Please enter your the required details below:\n")

            while True:
                username = input("\tUsername: ")
                if uv.validate_username(username) and uv.is_available(username):
                    break
                elif uv.is_available(username):
                    print("Username can only start with a latin letter, end with latin letter or digit, and may contain underscore only!")
                else:
                    print("Username is already taken!")
            
            while True:
                password = getpass("\tPassword: ")
                if uv.validate_password(password):
                    break
                else:
                    print("Password must be longer than 7 characters and contains at least\nan uppercase letter, a lowercase letter, and a symbol!")
            
            while True:
                password_confirm = getpass("\tPassword Confirmation: ")
                if uv.confirm_password(password, password_confirm):
                    break
                else:
                    print("Password confirmation doesnt't match!")

            while True:
                first_name = input("\tFirst Name: ")
                if uv.validate_name(first_name):
                    break
                else:
                    print("Please enter a name containing only lowercase or uppercase latin letters!")
            
            while True:
                last_name = input("\tLast Name: ")
                if uv.validate_name(last_name):
                    break
                else:
                    print("Please enter a name containing only lowercase or uppercase latin letters!")

            while True:
                email = input("\tEmail Address: ")
                if uv.validate_email(email):
                    break
                else:
                    print("Please enter a valid email address!")

            while True:
                mobile = input("\tMobile Number: ")
                if uv.validate_mobile(mobile):
                    break
                else:
                    print("Please enter a valid Egyptian mobile number!")
            
            user_data = [str(int(fr.get_lines(PATH['users'], 'list')[-1][0])+1), first_name, last_name, username, email, password, mobile, str(1)]
            if ur.register_user(user_data):
                print("Registration was successful!")
                print("You will be redirected to the main menu to login shortly.")
                time.sleep(3)
            else:
                print("An error occured! Please try again later. if error persists, call our support!")
            op = '0'

        elif op == '3':
            os.system('clear')
            print("######## Yinshe's CrowdFund App ########\n")
            print("\nThank you for using my CrowdFund App")
            print("The app will exit shortly...")
            time.sleep(3)

main()
