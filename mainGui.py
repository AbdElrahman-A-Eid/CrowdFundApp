import sys, time, os, shutil
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDesktopWidget
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QPixmap
from __init__ import PATH, dirname
import modules.file.read as fr
import modules.file.search as fs
import modules.user.login as ul
import modules.user.logout as uo
import modules.user.register as ur
import modules.user.delete_user as ud
import modules.user.edit_profile as up
import modules.project.create_project as pc
import modules.project.edit_project as pe
import modules.project.delete_project as pdel
import modules.project.filter_projects as pfil
import modules.project.project_validators as pv


# Height, Width pairs of all the ui elements
DIMENSIONS = {'welcome': (395, 610), 'login': (336, 600), 'register': (696, 630), 'dashboard': (546, 1034),
             'create_project': (487, 984), 'select_project': (320, 600), 'edit_project': (487, 984), 
             'profile_view': (590, 984), 'profile_edit': (570, 984)}

# Project Validaion Warnings
project_warnings = ["Must start with Latin letter. Can contain latin letters, numeric digits, and hyphen (-)",
                    "The only symbols allowed are: .,-_?!@*()'\"",
                    "Target must be a positive integer!",
                    "Can't be older than today's date!",
                    "Can't be older than start date!"
                    ]


def set_dimensions(window_name):
    widget.setFixedHeight(DIMENSIONS[window_name][0])
    widget.setFixedWidth(DIMENSIONS[window_name][1])


class WelcomeWindow(QMainWindow):
    def __init__(self):
        super(WelcomeWindow, self).__init__()
        loadUi(dirname + "/ui_templates/welcome_window.ui", self)
        self.get_started_button.clicked.connect(self.get_started)

    def get_started(self):
        login_window = LoginWindow()
        widget.addWidget(login_window)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        set_dimensions('login')


class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        loadUi(dirname + "/ui_templates/login_screen.ui", self)
        self.register_button.clicked.connect(self.go_to_registration)
        self.login_button.clicked.connect(self.login)
        self.password_input.returnPressed.connect(self.login)
        self.username_input.returnPressed.connect(self.login)

    def login(self):
        login_details = [
            self.username_input.text(), self.password_input.text()]
        if ul.authenticate_user(login_details):
            self.password_input.setText('')
            self.username_input.setText('')
            ul.login_user(login_details[0])
            self.go_to_dashboard()
        else:
            self.warning_label.setText('Incorrect username or password!')
            self.warning_label.repaint()
            self.password_input.setText('')
            time.sleep(1)
            self.warning_label.setText('')
            self.warning_label.repaint()

    def go_to_registration(self):
        register_window = RegisterWindow()
        widget.addWidget(register_window)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        set_dimensions('register')

    def go_to_dashboard(self):
        dashboard_window = DashboardWindow()
        widget.addWidget(dashboard_window)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        set_dimensions('dashboard')


class RegisterWindow(QMainWindow):
    def __init__(self):
        super(RegisterWindow, self).__init__()
        loadUi(dirname + "/ui_templates/register_screen.ui", self)
        self.login_button.clicked.connect(self.go_to_login)
        self.register_button.clicked.connect(self.register)

    def go_to_login(self):
        login_window = LoginWindow()
        widget.addWidget(login_window)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        set_dimensions('login')

    def register(self):

        valid = 1
        warning_labels = [self.warning1, self.warning2, self.warning3,
                          self.warning4, self.warning5, self.warning6, self.warning7]
        user_input = [self.username_input.text(), self.password_input.text(), self.confirm_password_input.text(
        ), self.first_name_input.text(), self.last_name_input.text(), self.email_input.text(), self.mobile_input.text()]

        invalid_warnings = [("Must start with Latin letter. Only underscore allowed!",
                             "Username is already taken!"),
                            "8 characters long, Uppercase letter, digit, symbol required!",
                            "Password confirmation doesnt't match!",
                            "Lowercase or uppercase latin letters only!",
                            "Lowercase or uppercase latin letters only!",
                            "Not a valid email address!",
                            "Not a valid Egyptian mobile number!"
                            ]

        for i, response in enumerate(ur.check_user_data(user_input)):
            if type(response) != type(True):
                # This is the username validation result
                if not response[0]:
                    # invalid username
                    self.launch_warning(
                        warning_labels[i], invalid_warnings[i][0])
                    valid = 0

                elif not response[1]:
                    # username taken
                    self.launch_warning(
                        warning_labels[i], invalid_warnings[i][1])
                    valid = 0

            elif not response:
                self.launch_warning(warning_labels[i], invalid_warnings[i])
                valid = 0

        if valid and ur.register_user([str(int(fr.get_lines(PATH['users'], 'list')[-1][0])+1), user_input[3], user_input[4], user_input[0], user_input[5], user_input[1], user_input[6], str(1)]):
            print("New User Registered!")
            self.go_to_login()
        elif not valid:
            time.sleep(2)
            for label in warning_labels:
                self.remove_warning(label)

    def launch_warning(self, label, message):
        label.setText(message)
        label.repaint()

    def remove_warning(self, label):
        label.setText('')
        label.repaint()


#            #################### Dashboard Section #####################             #

class DashboardWindow(QMainWindow):
    def __init__(self):
        super(DashboardWindow, self).__init__()
        loadUi(dirname + "/ui_templates/dashboard_screen.ui", self)

        self.filtered = 0
        self.logged_user = fr.get_logged_user()
        self.username_output.setText(self.logged_user[3])
        self.username_output_2.setText(self.logged_user[3])
        self.actionEdit_Profile.triggered.connect(self.edit_profile)
        self.actionView_Profile.triggered.connect(self.view_profile)
        self.actionDelete_Account.triggered.connect(self.delete_user)
        self.actionLogout.triggered.connect(self.logout)
        self.actionExit.triggered.connect(self.exit)
        self.create_button.clicked.connect(self.create_project)
        self.edit_button.clicked.connect(self.edit_project)
        self.delete_button.clicked.connect(self.delete_project)
        self.filter_button.clicked.connect(self.filter_projects)
        self.reset_button.clicked.connect(self.reset_filter)

        # Set Tables Columns Width
        my_projects_widths = [100, 210, 380, 100, 112, 112]
        all_projects_widths = [80, 190, 325, 100, 108, 108, 80]
        for col, width in enumerate(my_projects_widths):
            self.my_projects_table.setColumnWidth(col, width)
        for col, width in enumerate(all_projects_widths):
            self.all_projects_table.setColumnWidth(col, width)

        # Loading data to the tables
        self.update_tables()

    def logout(self):
        uo.logout_user()
        self.go_to_welcome()

    def go_to_welcome(self):
        welcome_window = WelcomeWindow()
        widget.addWidget(welcome_window)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        set_dimensions('welcome')

    def create_project(self):
        project_creation = ProjectCreation()
        widget.addWidget(project_creation)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        set_dimensions('create_project')

    def select_project(self):
        # Launch the dialog
        pass

    def edit_project(self):
        rows = sorted(self.my_projects_table.selectionModel().selectedRows())
        if not bool(rows):
            self.launch_warning(
                self.warning, 'You must select a project from the table first!')
            time.sleep(1)
            self.remove_warning(self.warning)
        else:
            project_edit = ProjectEdit(self.user_projects[rows[0].row()])
            widget.addWidget(project_edit)
            widget.setCurrentIndex(widget.currentIndex() + 1)
            set_dimensions('edit_project')

    def delete_project(self):
        rows = sorted(self.my_projects_table.selectionModel().selectedRows())
        if not bool(rows):
            self.launch_warning(
                self.warning, 'You must select a project/projects from the table first!')
            time.sleep(1)
            self.remove_warning(self.warning)
        else:
            for row in rows:
                pdel.delete_project(int(self.user_projects[row.row()][0]))
            self.update_tables()

    def filter_projects(self):
        if self.on_date_radio.isChecked():
            self.filtered = 1
        elif self.till_date_radio.isChecked():
            self.filtered = 2
        self.update_tables()

    def reset_filter(self):
        self.filtered = 0
        self.update_tables()

    def edit_profile(self):
        profile_edit_window = ProfileEdit()
        widget.addWidget(profile_edit_window)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        set_dimensions('profile_edit')

    def view_profile(self):
        profile_view_window = ProfileView()
        widget.addWidget(profile_view_window)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        set_dimensions('profile_view')

    def delete_user(self):
        if bool(self.user_projects):
            for project in self.user_projects:
                project[0]
                pdel.delete_project(int(project[0]))
        ud.delete_account(int(self.logged_user[0]))
        uo.logout_user()
        self.go_to_welcome()

    def exit(self):
        uo.logout_user()
        sys.exit()

    def launch_warning(self, label, message):
        label.setText(message)
        label.repaint()

    def remove_warning(self, label):
        label.setText('')
        label.repaint()

    def update_data(self):
        all_projects = fr.get_lines(PATH['projects'], 'list')
        self.user_projects = [
            project for project in all_projects if project[3] == self.logged_user[0]]
        self.project_lines = pfil.filter_projects(all_projects, self.on_date.text(
        ) if self.filtered else None, self.till_date.text() if (self.filtered - 1) == 1 else None)
        self.my_projects_table.setRowCount(len(self.user_projects))
        self.all_projects_table.setRowCount(len(self.project_lines))

    def update_tables(self):

        self.update_data()

        row = 0
        for project in self.user_projects:
            self.my_projects_table.setItem(
                row, 0, QtWidgets.QTableWidgetItem(project[0]))
            self.my_projects_table.setItem(
                row, 1, QtWidgets.QTableWidgetItem(project[1]))
            self.my_projects_table.setItem(
                row, 2, QtWidgets.QTableWidgetItem(project[2]))
            self.my_projects_table.setItem(
                row, 3, QtWidgets.QTableWidgetItem(project[4]))
            self.my_projects_table.setItem(
                row, 4, QtWidgets.QTableWidgetItem(project[5]))
            self.my_projects_table.setItem(
                row, 5, QtWidgets.QTableWidgetItem(project[6]))
            row += 1

        # Resize Rows for content
        self.my_projects_table.resizeRowsToContents()

        row = 0
        for project in self.project_lines:
            self.all_projects_table.setItem(
                row, 0, QtWidgets.QTableWidgetItem(project[0]))
            self.all_projects_table.setItem(
                row, 1, QtWidgets.QTableWidgetItem(project[1]))
            self.all_projects_table.setItem(
                row, 2, QtWidgets.QTableWidgetItem(project[2]))
            self.all_projects_table.setItem(
                row, 3, QtWidgets.QTableWidgetItem(project[4]))
            self.all_projects_table.setItem(
                row, 4, QtWidgets.QTableWidgetItem(project[5]))
            self.all_projects_table.setItem(
                row, 5, QtWidgets.QTableWidgetItem(project[6]))
            self.all_projects_table.setItem(
                row, 6, QtWidgets.QTableWidgetItem(project[3]))
            row += 1

        # Resize Rows for content
        self.all_projects_table.resizeRowsToContents()


#            #################### Projects Section #####################             #

class ProjectCreation(QMainWindow):
    def __init__(self):
        super(ProjectCreation, self).__init__()
        loadUi(dirname + "/ui_templates/project_creation.ui", self)
        self.logged_user = fr.get_logged_user()
        self.start_date_input.setDate(QDate.currentDate())
        self.end_date_input.setDate(QDate.currentDate())
        self.cancel_button.clicked.connect(self.back_to_dashboard)
        self.create_button.clicked.connect(self.create)

    def create(self):
        valid = 1
        warning_labels = [self.warning1, self.warning2,
                          self.warning3, self.warning4, self.warning5]
        project_input = [self.title_input.text(), self.desc_input.toPlainText().replace('\n', " "), self.target_input.text(
        ), self.start_date_input.text(), self.end_date_input.text()]

        for i, response in enumerate(pc.check_project_data(project_input)):
            if not response:
                self.launch_warning(warning_labels[i], project_warnings[i])
                valid = 0

        if valid and pc.create_project([str(int(fr.get_lines(PATH['projects'], 'list')[-1][0])+1), project_input[0], project_input[1], self.logged_user[0], project_input[2], project_input[3], project_input[4]]):
            print("New Project Created!")
            self.back_to_dashboard()
        elif not valid:
            time.sleep(2)
            for label in warning_labels:
                self.remove_warning(label)

    def launch_warning(self, label, message):
        label.setText(message)
        label.repaint()

    def remove_warning(self, label):
        label.setText('')
        label.repaint()

    def back_to_dashboard(self):
        dashboard_window = DashboardWindow()
        widget.addWidget(dashboard_window)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        set_dimensions('dashboard')


class ProjectEdit(QMainWindow):
    def __init__(self, project_data):
        super(ProjectEdit, self).__init__()
        loadUi(dirname + "/ui_templates/project_edit.ui", self)
        self.logged_user = fr.get_logged_user()
        self.edited_project_id = project_data[0]
        self.title_input.setText(project_data[1])
        self.desc_input.setPlainText(project_data[2])
        self.target_input.setText(project_data[4])
        start_date_comp = project_data[5].split('/')
        end_date_comp = project_data[6].split('/')
        self.start_date_input.setDate(QDate(int(start_date_comp[2]), int(
            start_date_comp[1]), int(start_date_comp[0])))
        self.end_date_input.setDate(
            QDate(int(end_date_comp[2]), int(end_date_comp[1]), int(end_date_comp[0])))

        self.cancel_button.clicked.connect(self.back_to_dashboard)
        self.edit_button.clicked.connect(self.edit)

    def edit(self):
        valid = 1
        warning_labels = [self.warning1, self.warning2,
                          self.warning3, self.warning4, self.warning5]
        project_input = [self.title_input.text(), self.desc_input.toPlainText().replace('\n', " "), self.target_input.text(
        ), self.start_date_input.text(), self.end_date_input.text()]

        for i, response in enumerate(pc.check_project_data(project_input)):
            if not response:
                self.launch_warning(warning_labels[i], project_warnings[i])
                valid = 0

        if valid and pe.edit_project(int(self.edited_project_id), [self.edited_project_id, project_input[0], project_input[1], self.logged_user[0], project_input[2], project_input[3], project_input[4]]):
            print("Project Edited!")
            self.back_to_dashboard()
        elif not valid:
            time.sleep(2)
            for label in warning_labels:
                self.remove_warning(label)

    def launch_warning(self, label, message):
        label.setText(message)
        label.repaint()

    def remove_warning(self, label):
        label.setText('')
        label.repaint()

    def back_to_dashboard(self):
        dashboard_window = DashboardWindow()
        widget.addWidget(dashboard_window)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        set_dimensions('dashboard')


#            #################### Profile Section #####################             #

class ProfileView(QMainWindow):
    def __init__(self):
        super(ProfileView, self).__init__()
        loadUi(dirname + "/ui_templates/profile_view.ui", self)
        self.logged_user = fr.get_logged_user()
        
        self.profile_data = fs.get_item_details("profiles", self.logged_user[0])

        self.full_name.setText(self.logged_user[1] + ' ' + self.logged_user[2])
        self.email.setText(self.logged_user[4])
        self.mobile.setText(self.logged_user[6])
        self.country.setText(self.profile_data[1])
        self.city.setText(self.profile_data[2])
        self.bio.setPlainText(self.profile_data[3])
        self.university.setText(self.profile_data[4])
        self.degree.setText(self.profile_data[5])

        self.dashboard_button.clicked.connect(self.back_to_dashboard)
        self.edit_button.clicked.connect(self.edit_profile)

        self.update_image()

    def update_image(self):
        qpixmap = QPixmap(PATH['imgs'] + self.profile_data[6])
        self.image_view.setPixmap(qpixmap.scaled(220, 220, Qt.KeepAspectRatio, Qt.FastTransformation))
        self.image_view.repaint()

    def edit_profile(self):
        profile_edit_window = ProfileEdit()
        widget.addWidget(profile_edit_window)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        set_dimensions('profile_edit')
    
    def back_to_dashboard(self):
        dashboard_window = DashboardWindow()
        widget.addWidget(dashboard_window)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        set_dimensions('dashboard')


class ProfileEdit(QMainWindow):
    def __init__(self):
        super(ProfileEdit, self).__init__()
        loadUi(dirname + "/ui_templates/profile_edit.ui", self)
        self.logged_user = fr.get_logged_user()
        
        self.profile_data = fs.get_item_details("profiles", self.logged_user[0])

        self.full_name.setText(self.logged_user[1] + ' ' + self.logged_user[2])
        self.email.setText(self.logged_user[4])
        self.country.setText(self.profile_data[1])
        self.city.setText(self.profile_data[2])
        self.bio_input.setPlainText(self.profile_data[3])
        self.university.setText(self.profile_data[4])
        self.degree.setText(self.profile_data[5])
        self.image_name.setText(self.profile_data[6])

        self.update_image()

        self.cancel_button.clicked.connect(self.back_to_dashboard)
        self.edit_button.clicked.connect(self.edit)
        self.image_button.clicked.connect(self.change_image)

    def edit(self):
        valid = 1
        warning_labels = [self.warning1, self.warning2,
                          self.warning3, self.warning4, self.warning5]
        profile_input = [self.logged_user[0], self.country.text(), self.city.text(), self.bio_input.toPlainText().replace('\n', " "), self.university.text(
        ), self.degree.text(), self.image_name.text()]

        for i, response in enumerate(up.check_profile_data(profile_input)):
            if not response:
                self.launch_warning(warning_labels[i], "Invalid input!")
                valid = 0

        if valid and up.edit_profile(int(self.logged_user[0]), profile_input):
            print("Profile Edited!")
            self.back_to_dashboard()
        elif not valid:
            time.sleep(2)
            for label in warning_labels:
                self.remove_warning(label)

    def launch_warning(self, label, message):
        label.setText(message)
        label.repaint()

    def remove_warning(self, label):
        label.setText('')
        label.repaint()

    def update_image(self):
        qpixmap = QPixmap(PATH['imgs'] + self.profile_data[6])
        self.image_view.setPixmap(qpixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.FastTransformation))
        self.image_view.repaint()

    def change_image(self):
        try:
            file_filter = 'JPEG (*.jpeg);;PNG (*.png);;JPG (*.jpg)'
            response = QFileDialog.getOpenFileName(
                parent=self,
                caption='Select a data file',
                directory=os.getcwd(),
                filter=file_filter,
                initialFilter='JPG (*.jpg)'
            )
            shutil.copyfile(response[0], PATH['imgs'] + self.logged_user[0] + '.' + response[0].split('.')[-1])
            self.image_name.setText(self.logged_user[0] + '.' + response[0].split('.')[-1])
            self.image_name.repaint()
            self.profile_data[6] = self.logged_user[0] + '.' + response[0].split('.')[-1]

            # Updating the image
            self.update_image()
        except Exception as e:
            print(f"{type(e).__name__}: {e}")
        
    def back_to_dashboard(self):
        dashboard_window = DashboardWindow()
        widget.addWidget(dashboard_window)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        set_dimensions('dashboard')

def center_window(widget):
		qr = widget.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		widget.move(qr.topLeft())

# main
app = QApplication(sys.argv)
welcome_window = WelcomeWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome_window)
widget.setWindowTitle('Yinshe CrowdFund App')
center_window(widget)
set_dimensions('welcome')
widget.show()
try:
    sys.exit(app.exec_())
finally:
    uo.logout_user()
    print("Exiting...")
