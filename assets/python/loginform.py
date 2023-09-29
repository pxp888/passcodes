from helpers import *
from tui import *


class loginForm(form):
    """ This is the login screen form that handles logging in
    and creating new accounts."""

    def __init__(self, screen):
        super().__init__(screen)

        self.username = lineEdit("Username: ")
        self.password = lineEdit("Password: ")

        self.loginButton = button("( Login )")
        self.createButton = button("( Create Account )")

        self.loginButton.callback = self.login
        self.createButton.callback = self.createAccount

        self.add(textline("\n"))
        self.add(textline("Welcome to Passcodes"))
        height, width = self.screen.getmaxyx()
        self.add(textline('\u2500'*(width-4)))
        self.add(textline("\n\n"))
        self.add(self.username)
        self.add(self.password)
        self.add(textline("\n"))
        self.add(self.loginButton)
        self.add(self.createButton)

        self.add(textline("Hint - You can navigate with arrows keys or Tab"),y=10)


    def login(self, thing=None):
        user = self.username.value
        password = self.password.value
        if user == "":
            self.alert("Username is required")
            return
        if password == "":
            self.alert("Password is required")
            return

        known = getUserLoginData(user)
        if known is None:
            self.alert("User not found")
            return

        user, salt, passwordHash = known
        if passwordHash == str(hash(password+salt)):
            self.parentApp.currentUser = user
            self.parentApp.masterPassword = password
            self.parentApp.getForm("Home").clear()
            self.parentApp.switchForm("Home")
            return
        else:
            self.alert("Incorrect Password")
            return

    def createAccount(self, thing=None):
        # this creates new accounts
        user = self.username.value
        password = self.password.value
        if user == "":
            self.alert("Username is required")
            return
        if password == "":
            self.alert("Password is required")
            return
        if len(password) < 6:
            self.alert("Password must be at least 6 characters")
            return

        known = getUserLoginData(user)
        if known is None:
            saveUserLoginData(user, password)
            self.alert("Account Created")
            self.clear()
            self.parentApp.currentUser = user
            self.parentApp.masterPassword = password
            self.parentApp.switchForm("Home")
            return
        else:
            self.alert("User already exists")
            return
