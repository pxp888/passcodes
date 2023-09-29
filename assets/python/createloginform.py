import time
import random
import re

from helpers import *
from tui import *


class createLoginForm(form):
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
        self.add(textline('\u2500'*(width-4)))
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

        self.passLength.value = '16'
        self.generate()

    def clear(self):
        super().clear()
        self.generate()

    def cancel(self, thing=None):
        # cancel the creation of the login and return to home
        self.clear()
        self.parentApp.switchForm('Home')

    def generate(self, thing=None):
        # generate a random password

        if self.passLength.value == '':
            self.passLength.value = '16'
        try:
            n = int(self.passLength.value)
        except ValueError:
            self.alert("Password length must be a number")
            self.passLength.value = ''
            return

        if int(self.passLength.value) > 40:
            self.alert("Password length cannot exceed 40")
            self.passLength.value = '40'
            self.passLength.draw()
        if int(self.passLength.value) < 6:
            self.alert("Password length must be at least 6")
            self.passLength.value = '6'
            self.passLength.draw()

        random.seed(time.time())
        letterpool = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        numberpool = "0123456789"
        symbolpool = "!@#$%^&*()_+-=[];:,./<>?"
        pool = letterpool
        if self.numbers.value:
            pool += numberpool
        if self.symbols.value:
            pool += symbolpool
        while 1:
            code = ''
            while len(code) < int(self.passLength.value):
                code += random.choice(pool)
            if self.numbers.value and not re.search(r'[{}]'.format(numberpool), code):
                continue
            if self.symbols.value and not re.search(r'[{}]'.format(re.escape(symbolpool)), code):
                continue
            break

        self.password.value = code
        self.password.draw()

    def on_ok(self, thing=None):
        # save the login to the database
        if self.name.value == "":
            self.alert("Name field is required")
            return
        if len(self.password.value) < 6:
            if not self.confirm('Password is short, are you sure?'):
                return
        if len(self.password.value) > 40:
            if not self.confirm('Password is long, are you sure?'):
                return

        numberpool = "0123456789"
        symbolpool = "!@#$%^&*()_+-=[];:,./<>?"
        if self.numbers.value and not re.search(r'[{}]'.format(numberpool), self.password.value):
            if not self.confirm("Password does not contain a number, are you sure?"):
                return
        if self.symbols.value and not re.search(r'[{}]'.format(re.escape(symbolpool)), self.password.value):
            if not self.confirm("Password does not contain a symbol, are you sure?"):
                return

        currentuser = self.parentApp.currentUser
        masterPassword = self.parentApp.masterPassword
        saveUserData(currentuser, self.name.value, self.username.value, self.password.value, self.url.value, masterPassword)

        self.clear()
        self.parentApp.switchForm("Home")
