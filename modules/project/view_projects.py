# Retrieve data from the database

def view_project(project_line):
    print(f"Project ID: {project_line[0]}")
    print(f"\tProject Title: {project_line[1]}")
    print(f"\tProject Description: {project_line[2]}")
    print(f"\tProject Owner ID: {project_line[3]}")
    print(f"\tProject Target: {project_line[4]} EGP")
    print(f"\tProject Start Date: {project_line[5]}")
    print(f"\tProject End Date: {project_line[6]}")