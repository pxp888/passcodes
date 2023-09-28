import npyscreen
from helpers import *
from tui import *


class HomeForm(npyscreen.Form):
    """ this is a simple form that acts as the main menu for the application.
    It allows the user to create new logins, view existing logins, or logout 
    and return to the login screen."""

    def create(self):
        # create the main menu
        self.heading = self.add(npyscreen.TitleText, name="Passcodes Homeform", editable=False)
        self.add(npyscreen.FixedText, value="-" * 40, rely=3, editable=False)
        self.add(npyscreen.ButtonPress, name="View Logins", when_pressed_function=self.searchPasscodes)
        self.add(npyscreen.ButtonPress, name="Create Login", when_pressed_function=self.createPasscode)
        self.add(npyscreen.ButtonPress, name="Logout", when_pressed_function=self.logout)
        # self.add(npyscreen.ButtonPress, name="Exit", when_pressed_function=self.exit)   # This is commented out for heroku deployment, uncomment to run locally.

    def exit(self):
        # exit the application
        self.parentApp.switchForm(None)

    def createPasscode(self):
        # switch to the create login form
        self.parentApp.switchForm("CreateLogin")

    def searchPasscodes(self):
        # switch to the view logins form
        self.parentApp.setNextForm("Home")
        self.parentApp.getForm("ViewLogins").update()
        self.parentApp.switchForm("ViewLogins")

    def logout(self):
        # log user out and return to login form
        self.parentApp.currentUser = None
        self.parentApp.masterPassword = None
        self.parentApp.getForm("MAIN").clear()
        self.parentApp.switchForm("MAIN")


class shomeForm(form):
    def __init__(self, screen):
        super().__init__(screen)

        self.viewButton = button('View Logins')
        self.createButton = button('Create Login')
        self.logoutButton = button('Logout')

        self.logoutButton.callback = self.logout

        self.add(self.viewButton)
        self.add(self.createButton)
        self.add(self.logoutButton)

    def logout(self, thing=None):
        self.parentApp.currentUser = None
        self.parentApp.masterPassword = None
        self.parentApp.getForm("MAIN").clear()
        self.parentApp.switchForm("MAIN")



