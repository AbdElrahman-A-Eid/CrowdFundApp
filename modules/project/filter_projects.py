# Import datetime module
from datetime import datetime

# Defining a function to return the filtered project(s) as a list of lists


def filter_projects(data, on_date, till_date):
    """Filter projects with date and return the filtered project(s) as a list of lists

    Args:
        (list): the projects data as a list of lists
        (str): the date to search projects starting at
        (str): the enclosing end date to filter with

    Returns:
        (list): the filtered list of project data or the original data if dates are None"""

    if on_date != None:
        filtered_projects = []

        for project in data:
            on_date_condition = ((not till_date) and (datetime.strptime(
                project[5], '%d/%m/%Y') == datetime.strptime(on_date, '%d/%m/%Y')))
            if on_date_condition or (till_date and ((datetime.strptime(project[5], '%d/%m/%Y') >= datetime.strptime(on_date, '%d/%m/%Y')) and (datetime.strptime(project[5], '%d/%m/%Y') <= datetime.strptime(till_date, '%d/%m/%Y')))):
                filtered_projects.append(project)

        return filtered_projects
    else:
        return data
