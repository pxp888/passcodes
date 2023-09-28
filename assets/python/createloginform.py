import time
import random
# import npyscreen

from helpers import *
from tui import *


# class CreateLoginForm(npyscreen.ActionForm):
#     # This form allows the user to create a new login record.

#     def create(self):
#         # create form widgets
#         self.heading = self.add(npyscreen.TitleText, name="Create Login", editable=False)
#         self.add(npyscreen.FixedText, value="-" * 40, rely=3, editable=False)
#         self.name = self.add(npyscreen.TitleText, name="Name:")
#         self.url = self.add(npyscreen.TitleText, name="URL:")
#         self.username = self.add(npyscreen.TitleText, name="Username:")
#         self.password = self.add(npyscreen.TitleText, name="Password:", editable=True)
#         self.add(npyscreen.ButtonPress, name="generate", when_pressed_function=self.generate)
#         self.add(npyscreen.TitleText, name=" ", editable=False)
#         self.add(npyscreen.ButtonPress, name="OK", when_pressed_function=self.on_ok)
#         self.add(npyscreen.ButtonPress, name="Cancel", when_pressed_function=self.on_cancel)
#         self.add(npyscreen.TitleText, name=" ", editable=False)
#         self.add(npyscreen.FixedText, value="-" * 40, editable=False)
#         self.passLength = self.add(npyscreen.TitleSlider, name="Password Length:", out_of=30, step=1, value=12)
#         self.passOptions = self.add(npyscreen.TitleMultiSelect, name="Password Options:", value=[0, 1], values=["Numbers", "Symbols"], scroll_exit=True)

#         self.passLength.value_changed_callback = self.generate
#         self.passOptions.value_changed_callback = self.generate

#         self.generate()

#     def clear(self):
#         # clear the form
#         self.name.value = ""
#         self.url.value = ""
#         self.username.value = ""
#         self.password.value = ""
#         self.passLength.value = 12
#         self.passOptions.value = [0, 1]
#         self.generate()

#     def generate(self, widget=None):
#         # generate a random password
#         random.seed(time.time())
#         code = ''
#         while len(code) < self.passLength.value:
#             n = random.randint(33, 122)
#             if not 0 in self.passOptions.value and n >= 48 and n <= 57: continue
#             if not 1 in self.passOptions.value and n >= 33 and n <= 47: continue
#             if not 1 in self.passOptions.value and n >= 58 and n <= 64: continue
#             if not 1 in self.passOptions.value and n >= 91 and n <= 96: continue
#             code += chr(n)
#         self.password.value = code
#         self.password.display()

#     def on_cancel(self):
#         # cancel the creation of the login and return to home
#         self.clear()
#         self.parentApp.switchForm("Home")

#     def on_ok(self):
#         # save the login to the database
#         if self.name.value == "":
#             npyscreen.notify_confirm("Name field is required", title="Alert")
#             return

#         currentuser = self.parentApp.currentUser
#         masterPassword = self.parentApp.masterPassword
#         saveUserData(currentuser, self.name.value, self.username.value, self.password.value, self.url.value, masterPassword)

#         self.clear()
#         self.parentApp.switchForm("Home")


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
        self.passLength.callback = self.generate
        
        self.numbers.callback = self.generate
        self.symbols.callback = self.generate
        
        
        self.add(textline('Create Login'))
        width, height = self.screen.getmaxyx()
        self.add(textline('\u2500'*(width-2)))
        self.add(self.name)
        self.add(self.url)
        self.add(self.username)
        self.add(self.password)
        self.add(self.generateButton)
        self.add(textline('\n'))
        self.add(self.okButton)
        self.add(self.cancelButton)
        self.add(textline('\n'))
        self.add(self.passLength)
        self.add(self.numbers)
        self.add(self.symbols)

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

    def numberCheck(self, thing=None):
        if self.passLength.value == '':
            return 
        try:
            n = int(self.passLength.value)
            self.generate()
        except:
            self.alert("Password length must be a number")
            self.passLength.value = self.passLength.value[:-1]
