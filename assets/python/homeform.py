from helpers import *
from tui import *


class homeForm(form):
    def __init__(self, screen):
        super().__init__(screen)

        self.viewButton = button('( View Logins )')
        self.createButton = button('( Create Login )')
        self.accountButton = button('( Account Details )')
        self.logoutButton = button('( Logout )')

        self.logoutButton.callback = self.logout
        self.createButton.callback = self.createPasscode
        self.viewButton.callback = self.viewPasscodes
        self.accountButton.callback = self.viewAccount

        self.add(textline('Passcodes Home'))
        height, width = self.screen.getmaxyx()
        self.add(textline('\u2500'*(width-4)))
        self.add(textline("\n\n"))
        self.add(self.viewButton)
        self.add(self.createButton)
        self.add(self.accountButton)
        self.add(self.logoutButton)

    def logout(self, thing=None):
        self.parentApp.currentUser = None
        self.parentApp.masterPassword = None
        self.parentApp.getForm("MAIN").clear()
        self.parentApp.switchForm("MAIN")

    def createPasscode(self, thing=None):
        self.parentApp.getForm("CreateLogin").clear()
        self.parentApp.switchForm("CreateLogin")

    def viewPasscodes(self, thing=None):
        self.parentApp.getForm("ViewLogins").update()
        self.parentApp.switchForm("ViewLogins")

    def viewAccount(self, thing=None):
        self.parentApp.getForm("Account").clear()
        self.parentApp.switchForm("Account")
