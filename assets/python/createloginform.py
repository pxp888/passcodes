import time
import random

from helpers import *
from tui import *


class screateLoginForm(form):
    def __init__(self, screen):
        super().__init__(screen)

        self.name = lineEdit('Name: ')
        self.url = lineEdit('URL: ')
        self.username = lineEdit('Username: ')
        self.password = lineEdit('Password: ')
        self.generateButton = button('( Generate )')
        self.okButton = button('( Save Entry )')
        self.cancelButton = button('( Cancel )')
        self.passLength = lineEdit('Password Length: ')
        self.numbers = checkbox('Numbers')
        self.symbols = checkbox('Symbols')

        self.cancelButton.callback = self.cancel
        self.generateButton.callback = self.generate
        self.okButton.callback = self.on_ok
        
        self.numbers.callback = self.generate
        self.symbols.callback = self.generate
        
        
        self.add(textline('Create Login'))
        height, width = self.screen.getmaxyx()
        self.add(textline('\u2500'*(width-2)))
        self.add(self.name)
        self.add(self.url)
        self.add(self.username)
        self.add(self.password)
        self.add(self.generateButton)
        self.add(textline('\n'))
        self.add(self.passLength)
        self.add(self.numbers)
        self.add(self.symbols)
        self.add(textline('\n'))
        self.add(self.okButton)
        self.add(self.cancelButton)

        self.passLength.value = '12'
        self.generate()

    def cancel(self, thing=None):
        # cancel the creation of the login and return to home
        self.clear()
        self.parentApp.switchForm('Home')

    def generate(self, thing=None):
        # generate a random password
        if self.passLength.value == '':
            self.passLength.value = '12'
        try:
            n = int(self.passLength.value)
        except:
            self.alert("Password length must be a number")
            self.passLength.value = ''
        
        if int(self.passLength.value) > 40:
            self.passLength.value = '30'
        if int(self.passLength.value) < 4:
            self.passLength.value = '4'
    
        random.seed(time.time())
        code = ''
        while len(code) < int(self.passLength.value):
            n = random.randint(33, 122)
            if self.numbers.value == False and n >= 48 and n <= 57: continue
            if self.symbols.value == False:
                if n >= 33 and n <= 47: continue
                if n >= 58 and n <= 64: continue
                if n >= 91 and n <= 96: continue
                if n >= 123 and n <= 126: continue

            code += chr(n)
        self.password.value = code
        self.password.draw()

    def on_ok(self, thing=None):
        # save the login to the database
        if self.name.value == "":
            self.alert("Name field is required")
            return
        if self.passLength.value == "":
            self.alert("Password length is required")
            return
        try:
            n = int(self.passLength.value)
        except:
            self.alert("Password length must be a number")
            return
        
        currentuser = self.parentApp.currentUser
        masterPassword = self.parentApp.masterPassword
        saveUserData(currentuser, self.name.value, self.username.value, self.password.value, self.url.value, masterPassword)

        self.clear()
        self.parentApp.switchForm("Home")

