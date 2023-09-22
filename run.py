import time
import hashlib
import random 
import sqlite3
import npyscreen


# create database tables if they don't exist
db = sqlite3.connect('passcodes.db')
db.execute('''CREATE TABLE IF NOT EXISTS passcodes
    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
    OWNER TEXT,
    NAME TEXT,
    USERNAME TEXT,
    PASSWORD TEXT,
    URL TEXT);''')
db.execute('''CREATE TABLE IF NOT EXISTS users
    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
    USERNAME TEXT,
    PASSWORD TEXT);''')
db.commit()
db.close()


# define helper functions

def hash(plaintext):
    # this is a hash function
    return hashlib.sha256(plaintext.encode()).hexdigest()

def getUserData(user):
    # gets records for a user from the database
    records = []
    db = sqlite3.connect('passcodes.db')
    cursor = db.execute('''SELECT NAME, USERNAME, PASSWORD, URL FROM passcodes WHERE OWNER = ?''', (user,))
    for row in cursor:
        records.append(row)
    db.close()
    return records

def saveUserData(user, name, username, password, url):
    # saves records for a user to the database
    db = sqlite3.connect('passcodes.db')
    db.execute('''INSERT INTO passcodes (OWNER, NAME, USERNAME, PASSWORD, URL) VALUES (?, ?, ?, ?, ?)''', (user, name, username, password, url))
    db.commit()
    db.close()

class MyTestApp(npyscreen.NPSAppManaged):
    def __init__(self):
        super().__init__()

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
            PASSWORD TEXT);''')
        self.db.commit()
        self.db.close()

        self.currentUser = None
        self.masterPassword = None
        
    def onStart(self):
        # create forms and associate them with the app
        self.registerForm("MAIN", LoginForm())
        self.registerForm("Home", HomeForm())
        self.registerForm("CreateLogin", CreateLoginForm())
        self.registerForm("ViewLogins", viewLoginForm())

class LoginForm(npyscreen.Form):
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

    def getUserLoginData(self, user):
        # This gets the user data from the database
        self.db = sqlite3.connect('passcodes.db')
        cursor = self.db.execute('''SELECT USERNAME, PASSWORD FROM users WHERE USERNAME = ?''', (user,))
        for row in cursor:
            self.db.close()
            return row
        self.db.close()
        return None
    
    def saveUserLoginData(self, user, password):
        # This saves the user data to the database
        password = hash(password)
        self.db = sqlite3.connect('passcodes.db')
        self.db.execute('''INSERT INTO users (USERNAME, PASSWORD) VALUES (?, ?)''', (user, password))
        self.db.commit()
        self.db.close()
        
    def login(self):
        # This checks if the user exists and if the password is correct
        user = self.username.value
        password = self.password.value
        known = self.getUserLoginData(user)
        if known is None:
            npyscreen.notify_confirm("User not found", title="Alert")
            return
        else:
            if known[1] == hash(password):
                self.parentApp.currentUser = user
                self.parentApp.masterPassword = password
                self.parentApp.switchForm("Home")
                return
            else:
                npyscreen.notify_confirm("Incorrect Password", title="Alert")
                return
        
    def createAccount(self):
        # this creates new accounts
        user = self.username.value
        password = self.password.value
        known = self.getUserLoginData(user)
        if known is None:
            self.saveUserLoginData(user, password)
            npyscreen.notify_confirm("Account Created", title="Alert")
            self.clear()
            self.parentApp.currentUser = user
            self.parentApp.masterPassword = password
            self.parentApp.switchForm("Home")
            return
        else:
            npyscreen.notify_confirm("User already exists", title="Alert")
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
        saveUserData(currentuser, self.name.value, self.username.value, self.password.value, self.url.value)

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
        records = getUserData(currentuser)
        self.grid.values = []
        for record in records:
            if filter.lower() in record[0].lower():
                self.grid.values.append(record)
        self.grid.display()

    def on_ok(self):
        # return to home form
        self.parentApp.switchForm("Home")
    



if __name__ == '__main__':
    TA = MyTestApp()
    TA.run()


