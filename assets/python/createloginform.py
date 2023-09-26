import time
import random
import npyscreen
from helpers import *


class CreateLoginForm(npyscreen.ActionForm):
    # This form allows the user to create a new login record.

    def create(self):
        # create form widgets
        self.heading = self.add(npyscreen.TitleText, name="Create Login", editable=False)
        self.add(npyscreen.FixedText, value="-" * 40, rely=3, editable=False)
        self.name = self.add(npyscreen.TitleText, name="Name:")
        self.url = self.add(npyscreen.TitleText, name="URL:")
        self.username = self.add(npyscreen.TitleText, name="Username:")
        self.password = self.add(npyscreen.TitleText, name="Password:", editable=True)
        self.add(npyscreen.ButtonPress, name="generate", when_pressed_function=self.generate)
        self.add(npyscreen.TitleText, name=" ", editable=False)
        self.add(npyscreen.ButtonPress, name="OK", when_pressed_function=self.on_ok)
        self.add(npyscreen.ButtonPress, name="Cancel", when_pressed_function=self.on_cancel)
        self.add(npyscreen.TitleText, name=" ", editable=False)
        self.add(npyscreen.FixedText, value="-" * 40, editable=False)
        self.passLength = self.add(npyscreen.TitleSlider, name="Password Length:", out_of=30, step=1, value=12)
        self.passOptions = self.add(npyscreen.TitleMultiSelect, name="Password Options:", value=[0, 1], values=["Numbers", "Symbols"], scroll_exit=True)

        self.passLength.value_changed_callback = self.generate
        self.passOptions.value_changed_callback = self.generate

        self.generate()

    def clear(self):
        # clear the form
        self.name.value = ""
        self.url.value = ""
        self.username.value = ""
        self.password.value = ""
        self.passLength.value = 12
        self.passOptions.value = [0, 1]
        self.generate()

    def generate(self, widget=None):
        # generate a random password
        random.seed(time.time())
        code = ''
        while len(code) < self.passLength.value:
            n = random.randint(33, 122)
            if not 0 in self.passOptions.value and n >= 48 and n <= 57: continue
            if not 1 in self.passOptions.value and n >= 33 and n <= 47: continue
            if not 1 in self.passOptions.value and n >= 58 and n <= 64: continue
            if not 1 in self.passOptions.value and n >= 91 and n <= 96: continue
            code += chr(n)
        self.password.value = code
        self.password.display()

    def on_cancel(self):
        # cancel the creation of the login and return to home
        self.clear()
        self.parentApp.switchForm("Home")

    def on_ok(self):
        # save the login to the database
        if self.name.value == "":
            npyscreen.notify_confirm("Name field is required", title="Alert")
            return

        currentuser = self.parentApp.currentUser
        masterPassword = self.parentApp.masterPassword
        saveUserData(currentuser, self.name.value, self.username.value, self.password.value, self.url.value, masterPassword)

        self.clear()
        self.parentApp.switchForm("Home")
