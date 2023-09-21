import npyscreen
import time 
import hashlib
import random 
import sqlite3

class MyTestApp(npyscreen.NPSAppManaged):
    def __init__(self):
        super().__init__()
        self.db = sqlite3.connect('passcodes.db')
        self.db.execute('''CREATE TABLE IF NOT EXISTS passcodes
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            OWNER TEXT NOT NULL,
            NAME TEXT NOT NULL,
            USERNAME TEXT NOT NULL,
            PASSWORD TEXT NOT NULL,
            URL TEXT NOT NULL);''')
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
            self.saveUserData()
            npyscreen.notify_confirm("Added User", title="Alert")
            self.parentApp.currentUser = user
            self.parentApp.switchForm("Home")
            return

class HomeForm(npyscreen.Form):    
    def create(self):
        self.heading = self.add(npyscreen.TitleText, name = "Passcodes Homeform", editable = False)
        # add a menu to create, search, and delete passcodes
        self.add(npyscreen.FixedText, value="-" * 40, rely=3, editable=False)
        self.add(npyscreen.ButtonPress, name = "View Logins", when_pressed_function = self.searchPasscode)
        self.add(npyscreen.ButtonPress, name = "Create Login", when_pressed_function = self.createPasscode)
        # self.add(npyscreen.ButtonPress, name = "Delete Login", when_pressed_function = self.deletePasscode)
        self.add(npyscreen.ButtonPress, name = "Logout", when_pressed_function = self.logout)

    def createPasscode(self):
        self.parentApp.switchForm("CreateLogin")

    def searchPasscode(self):
        self.parentApp.setNextForm("Home")
        self.parentApp.switchForm("ViewLogins")

    def deletePasscode(self):
        pass

    def logout(self):
        self.parentApp.currentUser = None
        self.parentApp.getForm("MAIN").clear()
        self.parentApp.switchForm("MAIN")
        
class CreateLoginForm(npyscreen.Form):
    def create(self):
        self.heading = self.add(npyscreen.TitleText, name = "Create Login", editable = False)
        self.add(npyscreen.FixedText, value="-" * 40, rely=3, editable=False)

        self.name = self.add(npyscreen.TitleText, name = "Name:")
        self.url = self.add(npyscreen.TitleText, name = "URL:")
        self.username = self.add(npyscreen.TitleText, name = "Username:")
        self.password = self.add(npyscreen.TitleText, name = "Password:", editable = True)
        
        self.add(npyscreen.ButtonPress, name = "generate", when_pressed_function = self.generate)
        self.add(npyscreen.TitleText, name = " ", editable = False)
        self.add(npyscreen.ButtonPress, name = "Save", when_pressed_function = self.save)
        self.add(npyscreen.ButtonPress, name = "Cancel", when_pressed_function = self.cancel)

        self.add(npyscreen.FixedText, value="-" * 40, editable=False)
        self.passLength = self.add(npyscreen.TitleSlider, name = "Password Length:", out_of=30, step=1, value=12, when_value_edited_function = self.generate)
        self.passOptions = self.add(npyscreen.TitleMultiSelect, name = "Password Options:", value = [0,1] ,values = ["Numbers", "Symbols"], scroll_exit=True, when_value_edited_function = self.generate)

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
    
    def generate(self):
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

    def cancel(self):
        # cancel the creation of the login and return to home
        self.clear()
        self.parentApp.switchForm("Home")

    def save(self):
        # save the login to the database
        currentuser = self.parentApp.currentUser
        self.db = sqlite3.connect('passcodes.db')
        self.db.execute('''INSERT INTO passcodes (OWNER, NAME, USERNAME, PASSWORD, URL) VALUES (?, ?, ?, ?, ?)''', (currentuser, self.name.value, self.username.value, self.password.value, self.url.value))
        self.db.commit()
        self.db.close()
        self.clear()
        self.parentApp.switchForm("Home")

class viewLoginForm(npyscreen.Form):
    

    def create(self):
        self.name = self.add(npyscreen.TitleText, name = "Name:", editable = True)
        self.add(npyscreen.ButtonPress, name = "Done", when_pressed_function = self.on_ok)
        self.grid = self.add(npyscreen.GridColTitles, col_titles = ["Name", "Username", "Password", "URL"], editable = False)
        self.fill()

    def fill(self):
        currentuser = self.parentApp.currentUser

        self.db = sqlite3.connect('passcodes.db')
        cursor = self.db.execute('''SELECT NAME, USERNAME, PASSWORD, URL FROM passcodes where OWNER = ?''', (currentuser,))
        self.grid.values = []
        for row in cursor:
            self.grid.values.append(row)
            print(row)
        self.db.close()
        self.grid.display()

    def on_ok(self):
        self.parentApp.switchForm("Home")



if __name__ == '__main__':
    TA = MyTestApp()
    TA.run()


