import npyscreen

from helpers import *


class LoginForm(npyscreen.Form):
    # This is the login screen form that handles logging in and creating new accounts.
    # There are two buttons, one to login and one to create a new account.
    # There are also text fields for username and password entry.

    def create(self):
        # This creates the form
        self.heading = self.add(npyscreen.TitleText, name = "Welcome to Passcodes", editable = False)
        self.username = self.add(npyscreen.TitleText, name = "Username:")
        self.password = self.add(npyscreen.TitlePassword, name = "Password:")
        self.add(npyscreen.ButtonPress, name = "Login", when_pressed_function = self.login)
        self.add(npyscreen.ButtonPress, name = "Create Account", when_pressed_function = self.createAccount)

    def clear(self):
        # This clears the form
        self.username.value = ""
        self.password.value = ""

    def login(self):
        # This checks if the user exists and if the password is correct
        user = self.username.value
        password = self.password.value
        if user == "":
            npyscreen.notify_confirm("Username is required", title="Alert")
            return
        if password == "":
            npyscreen.notify_confirm("Password is required", title="Alert")
            return

        known = getUserLoginData(user)
        if known is None:
            npyscreen.notify_confirm("User not found", title="Alert")
            return

        user, salt, passwordHash = known
        if passwordHash == str(hash(password+salt)):
            self.parentApp.currentUser = user
            self.parentApp.masterPassword = password
            self.parentApp.switchForm("Home")
            return
        else:
            npyscreen.notify_confirm("Incorrect Password", title="Alert")
            return

    def createAccount(self):
        # this creates new accounts
        user = self.username.value
        password = self.password.value
        if user == "":
            npyscreen.notify_confirm("Username is required", title="Alert")
            return
        if password == "":
            npyscreen.notify_confirm("Password is required", title="Alert")
            return

        known = getUserLoginData(user)
        if known is None:
            saveUserLoginData(user, password)
            npyscreen.notify_confirm("Account Created", title="Alert")
            self.clear()
            self.parentApp.currentUser = user
            self.parentApp.masterPassword = password
            self.parentApp.switchForm("Home")
            return
        else:
            npyscreen.notify_confirm("User already exists", title="Alert")
            return

