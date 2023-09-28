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

        self.backButton.callback = self.cancel

        self.add(textline('Account Details'))
        height, width = self.screen.getmaxyx()
        self.add(textline('\u2500'*(width-4)))
        self.add(self.backButton)
        self.add(textline("\n\n"))

        self.add(self.unameline)
        self.add(textline("\n\n"))

        self.add(self.passline0)
        self.add(self.passline1)
        self.add(self.passline2)
        self.add(self.passButton)

    def clear(self):
        self.unameline.label = 'Username: ' + self.parentApp.currentUser
        super().clear()

    def cancel(self, thing=None):
        # return to home form
        self.clear()
        self.parentApp.switchForm('Home')

    def setNewPassword(self, thing):
        pass

