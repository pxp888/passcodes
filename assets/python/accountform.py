from helpers import *
from tui import *


class accountForm(form):
    def __init__(self, screen):
        super().__init__(screen)

        self.backButton = button('( Back )')

        self.unameline = textline('Username: ')
        
        self.passline0 = lineEdit('Current Password: ')
        self.passline1 = lineEdit('    New Password: ')
        self.passline2 = lineEdit('Confirm Password: ')
        self.passButton = button('( Set New Password )')

        self.passline3 = lineEdit('Current Password: ')
        self.passline4 = lineEdit('Confirm Password: ')
        self.killButton = button('( Delete Account )')

        self.backButton.callback = self.cancel
        self.passButton.callback = self.setNewPassword
        self.killButton.callback = self.removeUser

        self.add(textline('Account Details'))
        height, width = self.screen.getmaxyx()
        self.add(textline('\u2500'*(width-4)))
        self.add(self.backButton)
        self.add(textline("\n"))

        self.add(self.unameline)
        self.add(textline("\n"))

        self.add(textline("To change master password, fill in the fields below"))
        self.add(textline("then press the 'Set New Password' button.  This cannot be undone."))
        self.add(self.passline0)
        self.add(self.passline1)
        self.add(self.passline2)
        self.add(self.passButton)

        self.add(textline("\n"))
        self.add(textline("To delete account and all data, fill in the fields below"))
        self.add(textline("then press the 'Delete Account' button.  This cannot be undone."))
        self.add(self.passline3)
        self.add(self.passline4)
        self.add(self.killButton)

    def clear(self):
        self.unameline.label = 'Username: ' + self.parentApp.currentUser
        super().clear()

    def cancel(self, thing=None):
        # return to home form
        self.clear()
        self.parentApp.switchForm('Home')

    def setNewPassword(self, thing):
        """set a new password for the account"""
        
        # check that the current password is correct
        known = getUserLoginData(self.parentApp.currentUser)
        password = self.passline0.value
        user, salt, passwordHash = known
        if not passwordHash == str(hash(password+salt)):
            self.alert("Incorrect Current Password")
            return
        
        # check that the new password is valid
        if not self.passline1.value == self.passline2.value:
            self.alert("New Passwords do not match")
            return
        if self.passline1.value == "":
            self.alert("New Password cannot be blank")
            return
        if len(self.passline1.value) < 6:
            self.alert("New Password must be at least 6 characters")
            return
        
        npass = self.passline1.value
        records = getUserData(user, password)

        # remove current data from database
        removeUserData(self.parentApp.currentUser)

        # re-add data to database with new password
        for name, username, password, url in records:
            saveUserData(user, name, username, password, url, npass)

        # update the master password
        saveUserLoginData(user, npass)

        # return to home form
        self.alert("Password Changed")
        self.clear()
        self.parentApp.masterPassword = npass
        self.parentApp.switchForm('Home')

    def removeUser(self, thing):
        """remove the user from the database"""
        # check that the current password is correct
        known = getUserLoginData(self.parentApp.currentUser)

        password = self.passline3.value
        user, salt, passwordHash = known
        if not passwordHash == str(hash(password+salt)):
            self.alert("Incorrect Current Password")
            return
        
        # check that the new password is valid
        if not self.passline4.value == self.passline3.value:
            self.alert("Passwords do not match")
            return
        if self.passline4.value == "":
            self.alert("Password cannot be blank")
            return
        
        # remove user from database
        removeUserData(self.parentApp.currentUser)

        # return to home form
        self.alert("Account Deleted")
        self.clear()
        self.parentApp.currentUser = None
        self.parentApp.masterPassword = None
        self.parentApp.getForm("MAIN").clear()
        self.parentApp.switchForm('MAIN')


