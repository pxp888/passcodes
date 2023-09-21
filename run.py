import npyscreen
import time 
import hashlib 
import sqlite3

class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.registerForm("MAIN", LoginForm())
        self.registerForm("Home", HomeForm())

class LoginForm(npyscreen.Form):
    def __init__(self):
        super().__init__()
        self.users = self.getUserData()

    def getUserData(self):
        # this is to get the user data from the database, to be implemented later
        users = {}
        return users 
    
    def create(self):
        # This creates the form
        self.heading = self.add(npyscreen.TitleText, name = "Welcome to Passcodes", editable = False)
        self.username = self.add(npyscreen.TitleText, name = "Username:")
        self.password = self.add(npyscreen.TitlePassword, name = "Password:")
        self.add(npyscreen.ButtonPress, name = "Login", when_pressed_function = self.login)
        self.add(npyscreen.ButtonPress, name = "Create Account", when_pressed_function = self.createAccount)    

    def afterEditing(self):
        pass 

    def login(self):
        # This checks if the user exists and if the password is correct
        user = self.username.value
        password = self.password.value
        if user not in self.users:
            npyscreen.notify_confirm("User does not exist", title="Alert")
            print('user does not exist')
            return
        else:
            if self.users[user] == hashlib.sha256(password.encode()).hexdigest():
                npyscreen.notify_confirm("Login Successful", title="Alert")
                self.parentApp.switchForm("Home")
                return
            else:
                npyscreen.notify_confirm("Incorrect Password", title="Alert")
                return
        
    def createAccount(self):
        # this creates new accounts
        user = self.username.value
        password = self.password.value
        if user in self.users:
            npyscreen.notify_confirm("User Already exists", title="Alert")
            return
        else:
            self.users[user] = hashlib.sha256(password.encode()).hexdigest()
            npyscreen.notify_confirm("Added User", title="Alert")
            self.parentApp.switchForm("Home")
            return

class HomeForm(npyscreen.Form):
    def __init__(self):
        super().__init__()
    
    def create(self):
        self.heading = self.add(npyscreen.TitleText, name = "Passcodes Homeform", editable = False)
        # add a menu to create, search, and delete passcodes
        self.add(npyscreen.ButtonPress, name = "Create Passcode", when_pressed_function = self.createPasscode)
        self.add(npyscreen.ButtonPress, name = "Search Passcode", when_pressed_function = self.searchPasscode)
        self.add(npyscreen.ButtonPress, name = "Delete Passcode", when_pressed_function = self.deletePasscode)

    def createPasscode(self):
        pass

    def searchPasscode(self):
        pass

    def deletePasscode(self):
        pass
        


if __name__ == '__main__':
    TA = MyTestApp()
    TA.run()
