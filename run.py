import npyscreen
import time 
import hashlib 
import sqlite3

class MyTestApp(npyscreen.NPSAppManaged):
    def __init__(self):
        super().__init__()
        self.db = sqlite3.connect('passcodes.db')
        self.db.execute('''CREATE TABLE IF NOT EXISTS passcodes
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT NOT NULL,
            USERNAME TEXT NOT NULL,
            PASSWORD TEXT NOT NULL,
            URL TEXT NOT NULL,
            NOTES TEXT NOT NULL);''')
        self.db.execute('''CREATE TABLE IF NOT EXISTS users
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            USERNAME TEXT NOT NULL,
            PASSWORD TEXT NOT NULL);''')
        self.db.commit()
        self.db.close()

        self.currentUser = None

    def onStart(self):
        self.registerForm("MAIN", LoginForm())
        self.registerForm("Home", HomeForm())
        self.registerForm("CreateLogin", CreateLoginForm())

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
                self.parentApp.currentUser = user
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
            self.parentApp.currentUser = user
            self.parentApp.switchForm("Home")
            return

class HomeForm(npyscreen.Form):
    def __init__(self):
        super().__init__()
    
    def create(self):
        self.heading = self.add(npyscreen.TitleText, name = "Passcodes Homeform", editable = False)
        # add a menu to create, search, and delete passcodes
        self.add(npyscreen.FixedText, value="-" * 40, rely=3, editable=False)
        self.add(npyscreen.ButtonPress, name = "Search Logins", when_pressed_function = self.searchPasscode)
        self.add(npyscreen.ButtonPress, name = "Create Login", when_pressed_function = self.createPasscode)
        self.add(npyscreen.ButtonPress, name = "Delete Login", when_pressed_function = self.deletePasscode)

    def createPasscode(self):
        self.parentApp.switchForm("CreateLogin")

    def searchPasscode(self):
        pass

    def deletePasscode(self):
        pass



class CreateLoginForm(npyscreen.FormWithMenus):
    def __init__(self):
        super().__init__()
    
    def create(self):
        self.heading = self.add(npyscreen.TitleText, name = "Create Login", editable = False)
        self.add(npyscreen.FixedText, value="-" * 40, rely=3, editable=False)

        self.name = self.add(npyscreen.TitleText, name = "Name:")
        self.url = self.add(npyscreen.TitleText, name = "URL:")
        self.username = self.add(npyscreen.TitleText, name = "Username:")
        self.password = self.add(npyscreen.TitleText, name = "Password:", editable = True)
        
        self.add(npyscreen.ButtonPress, name = "generate", when_pressed_function = self.generate)
        
        self.add(npyscreen.ButtonPress, name = "Save", when_pressed_function = self.createPasscode)
        self.add(npyscreen.ButtonPress, name = "Cancel", when_pressed_function = self.cancel)

        self.add(npyscreen.FixedText, value="-" * 40, rely=12, editable=False)
        self.length = self.add(npyscreen.TitleSlider, name = "Password Length:", out_of=30, step=1, value=12)
        self.numbers = self.add(npyscreen.TitleMultiSelect, name = "Password Options:", value = [0,1,2,3] ,values = ["Numbers", "Symbols", "Uppercase"], scroll_exit=True)
        
    def generate(self):
        pass

    def cancel(self):
        self.parentApp.switchForm("Home")


if __name__ == '__main__':
    TA = MyTestApp()
    TA.run()
