import npyscreen
import time
import hashlib
import random 
import sqlite3

class MyTestApp(npyscreen.NPSAppManaged):
    def __init__(self):
        super().__init__()

        # create the database if it doesn't exist
        self.db = sqlite3.connect('passcodes.db')
        self.db.execute('''CREATE TABLE IF NOT EXISTS passcodes
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            OWNER TEXT,
            NAME TEXT,
            USERNAME TEXT,
            PASSWORD TEXT,
            URL TEXT);''')
        self.db.execute('''CREATE TABLE IF NOT EXISTS users
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            USERNAME TEXT,
            SALT TEXT,                                                                                                                                      
            PASSWORD TEXT);''')
        self.db.commit()
        self.db.close()

        # create variables to store the current user and master password
        self.currentUser = None
        self.masterPassword = None

    def onStart(self):
        # create forms and associate them with the app
        self.registerForm("MAIN", LoginForm())
        self.registerForm("Home", HomeForm())
        self.registerForm("CreateLogin", CreateLoginForm())
        self.registerForm("ViewLogins", viewLoginForm())

class LoginForm(npyscreen.Form):
    def __init__(self):
        super().__init__()
        self.users = self.getUserData()

    def getUserData(self):
        # this is to get the user data from the database, and return it as a dictionary
        users = {}
        self.db = sqlite3.connect('passcodes.db')
        cursor = self.db.execute('''SELECT USERNAME, PASSWORD FROM users''')
        for row in cursor:
            users[row[0]] = row[1]
        self.db.close()
        return users
    
    def saveUserData(self):
        # write user data to the database
        self.db = sqlite3.connect('passcodes.db')
        self.db.execute('''INSERT INTO users (USERNAME, PASSWORD) VALUES (?, ?)''', (self.username.value, self.users[self.username.value]))
        self.db.commit()
        self.db.close()
        
    def create(self):
        # This creates the form
        self.heading = self.add(npyscreen.TitleText, name = "Welcome to Passcodes", editable = False)
        self.username = self.add(npyscreen.TitleText, name = "Username:")
        self.password = self.add(npyscreen.TitlePassword, name = "Password:")
        self.add(npyscreen.ButtonPress, name = "Login", when_pressed_function = self.login)
        self.add(npyscreen.ButtonPress, name = "Create Account", when_pressed_function = self.createAccount)    

    def clear(self):
        # This clears the form
        self.username.value = ""
        self.password.value = ""    

    def login(self):
        # This checks if the user exists and if the password is correct
        user = self.username.value
        password = self.password.value
        if user not in self.users:
            npyscreen.notify_confirm("User does not exist", title="Alert")
            return
        else:
            if self.users[user] == hashlib.sha256(password.encode()).hexdigest():
                self.parentApp.switchForm("Home")
                self.parentApp.currentUser = user
                self.parentApp.masterPassword = password
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
            self.saveUserData()
            npyscreen.notify_confirm("Added User", title="Alert")
            self.parentApp.currentUser = user
            self.parentApp.switchForm("Home")
            return

class HomeForm(npyscreen.Form):    
    def create(self):
        # create the main menu
        self.heading = self.add(npyscreen.TitleText, name = "Passcodes Homeform", editable = False)
        self.add(npyscreen.FixedText, value="-" * 40, rely=3, editable=False)
        self.add(npyscreen.ButtonPress, name = "View Logins", when_pressed_function = self.searchPasscode)
        self.add(npyscreen.ButtonPress, name = "Create Login", when_pressed_function = self.createPasscode)
        self.add(npyscreen.ButtonPress, name = "Logout", when_pressed_function = self.logout)

    def createPasscode(self):
        # switch to the create login form
        self.parentApp.switchForm("CreateLogin")

    def searchPasscode(self):
        # switch to the view logins form
        self.parentApp.setNextForm("Home")
        self.parentApp.getForm("ViewLogins").fill()
        self.parentApp.switchForm("ViewLogins")

    def logout(self):
        # log user out and return to login form
        self.parentApp.currentUser = None
        self.parentApp.masterPassword = None
        self.parentApp.getForm("MAIN").clear()
        self.parentApp.switchForm("MAIN")
        
class CreateLoginForm(npyscreen.ActionForm):
    def create(self):
        # create form widgets
        self.heading = self.add(npyscreen.TitleText, name = "Create Login", editable = False)
        self.add(npyscreen.FixedText, value="-" * 40, rely=3, editable=False)
        self.name = self.add(npyscreen.TitleText, name = "Name:")
        self.url = self.add(npyscreen.TitleText, name = "URL:")
        self.username = self.add(npyscreen.TitleText, name = "Username:")
        self.password = self.add(npyscreen.TitleText, name = "Password:", editable = True)
        self.add(npyscreen.ButtonPress, name = "generate", when_pressed_function = self.generate)
        self.add(npyscreen.TitleText, name = " ", editable = False)
        self.add(npyscreen.FixedText, value="-" * 40, editable=False)
        self.passLength = self.add(npyscreen.TitleSlider, name = "Password Length:", out_of=30, step=1, value=12)
        self.passOptions = self.add(npyscreen.TitleMultiSelect, name = "Password Options:", value = [0,1] ,values = ["Numbers", "Symbols"], scroll_exit=True)

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
        self.passOptions.value = [0,1]
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
        currentuser = self.parentApp.currentUser
        self.db = sqlite3.connect('passcodes.db')
        self.db.execute('''INSERT INTO passcodes (OWNER, NAME, USERNAME, PASSWORD, URL) VALUES (?, ?, ?, ?, ?)''', (currentuser, self.name.value, self.username.value, self.password.value, self.url.value))
        self.db.commit()
        self.db.close()
        self.clear()
        self.parentApp.switchForm("Home")

class viewLoginForm(npyscreen.ActionFormMinimal):
    def create(self):
        # create the form widgets
        self.nameline = self.add(npyscreen.TitleText, name = "Name has:", editable = True)
        self.add(npyscreen.FixedText, value="-" * 40, editable=False)
        self.nameline.value_changed_callback = self.fill
        self.grid = self.add(npyscreen.GridColTitles, col_titles = ["Name", "Username", "Password", "URL"], editable = False)
        
    def fill(self, widget=None):
        # fill the grid with the login details
        currentuser = self.parentApp.currentUser
        filter = self.nameline.value
        self.db = sqlite3.connect('passcodes.db')
        cursor = self.db.execute('''SELECT NAME, USERNAME, PASSWORD, URL FROM passcodes where OWNER = ? ORDER BY NAME ASC''', (currentuser,))
        self.grid.values = []
        for row in cursor:
            if not filter is None and len(filter) > 0:
                if filter not in row[0]: continue
            self.grid.values.append(row)
        self.db.close()
        self.grid.display()

    def on_ok(self):
        # return to home form
        self.parentApp.switchForm("Home")
    



if __name__ == '__main__':
    TA = MyTestApp()
    TA.run()


