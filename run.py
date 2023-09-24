import os 
import time
import hashlib
import random 
import base64
import psycopg2
import curses
import npyscreen
from cryptography.fernet import Fernet

# This is a simple password manager that uses a master password to encrypt and decrypt passwords
# Passwords are stored in a database and encrypted with the master password
# The master password is hashed and stored in the database


# CRYPTOGRAPHY FUNCTIONS

# These are defined here to make it easier to change the encryption method later

def hash(plaintext):
    # this is a hash function
    return hashlib.sha256(plaintext.encode()).digest()

def encrypt(plaintext, key):
    # this is an encryption function
    key = base64.b64encode(hash(key))
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(plaintext.encode())
    return cipher_text.decode()

def decrypt(ciphertext, key):
    # this is a decryption function
    key = base64.b64encode(hash(key))
    cipher_suite = Fernet(key)
    plain_text = cipher_suite.decrypt(ciphertext.encode())
    return plain_text.decode()


# DATABASE FUNCTIONS

# These are defined here to make it easier to change the database later.  
# These functions are the only ones that interact with the database.  
# There is one global variable to store the database connection, and make it available to all functions.

db_connection = None

def getDBConnection():
    # This is a helper function used by the database calls below to get a database connection.  
    # This enables the same connection to be used for multiple calls, and re-establishes the connection if it is lost.
    # The database connection details are stored in environment variables.

    db_pw = os.environ.get('DB_PW')
    db_ip = os.environ.get('DB_IP')
    if db_ip is None: db_ip = "localhost"
    
    global db_connection
    if db_connection is None or db_connection.closed != 0:
        try:
            db_connection = psycopg2.connect(
                host=db_ip,
                database="postgres",
                user="postgres",
                password=db_pw
            )
        except psycopg2.OperationalError:
            # if the connection times out, re-establish it
            db_connection = psycopg2.connect(
                host=db_ip,
                database="postgres",
                user="postgres",
                password=db_pw
            )
    return db_connection

def setupStorage():
    # create database tables if they don't exist.  This should only be called once at the start of the application.  
    conn = getDBConnection()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS passcodes
        (ID SERIAL PRIMARY KEY,
        OWNER TEXT,
        NAME TEXT,
        USERNAME TEXT,
        PASSWORD TEXT,
        URL TEXT);''')
    cur.execute('''CREATE TABLE IF NOT EXISTS users
        (ID SERIAL PRIMARY KEY,
        USERNAME TEXT,
        SALT TEXT,
        PASSWORD TEXT);''')
    conn.commit()
    cur.close()
    
def getUserLoginData(username):
    # gets login data from the database for a given username.  
    conn = getDBConnection()
    cur = conn.cursor()
    cur.execute("SELECT USERNAME, SALT, PASSWORD FROM users WHERE USERNAME = %s", (username,))
    result = cur.fetchone()
    cur.close()

    if result is None:
        return None
    else:
        return result 

def saveUserLoginData(username, password):
    # saves login data to the database
    salt = str(random.randint(1000000000000000, 9999999999999999))
    passwordHash = str(hash(password + salt))
    
    conn = getDBConnection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (USERNAME, SALT, PASSWORD) VALUES (%s, %s, %s)", (username, salt, passwordHash))
    conn.commit()
    cur.close()

def getUserData(owner, masterPassword):
    # gets records for a user from the database
    conn = getDBConnection()
    cur = conn.cursor()
    cur.execute("SELECT NAME, USERNAME, PASSWORD, URL FROM passcodes WHERE OWNER = %s", (owner,))
    records = cur.fetchall()
    cur.close()

    for i in range(len(records)):
        name, username, password, url = records[i]
        records[i] = (name, username, decrypt(password, masterPassword), url)
    return records

def saveUserData(owner, name, username, password, url, masterPassword):
    # saves records for a user to the database
    password = encrypt(password, masterPassword)

    conn = getDBConnection()
    cur = conn.cursor()
    cur.execute("INSERT INTO passcodes (OWNER, NAME, USERNAME, PASSWORD, URL) VALUES (%s, %s, %s, %s, %s)", (owner, name, username, password, url))
    conn.commit()
    cur.close()


# MAIN APPLICATION

class MyTestApp(npyscreen.NPSAppManaged):
    # This is the main application instance.  
    def __init__(self):
        super(MyTestApp, self).__init__()
        # the current user and master password are stored here, to make them available to all forms.  
        self.currentUser = None
        self.masterPassword = None
        
    def onStart(self):
        # create forms and associate them with the app
        self.registerForm("MAIN", LoginForm())
        self.registerForm("Home", HomeForm())
        self.registerForm("CreateLogin", CreateLoginForm())
        self.registerForm("ViewLogins", viewLoginForm())

class LoginForm(npyscreen.Form):
    # This is the login screen form that handles logging in and creating new accounts.  
    # There are two buttons, one to login and one to create a new account.
    # There are also text fields for username and password entry.  

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
        known = getUserLoginData(user)
        if known is None:
            npyscreen.notify_confirm("User not found", title="Alert")
            return
        try:
            user, salt, passwordHash = known
            if passwordHash == str(hash(password+salt)):
                self.parentApp.currentUser = user
                self.parentApp.masterPassword = password
                self.parentApp.switchForm("Home")
                return
            else:
                npyscreen.notify_confirm("Incorrect Password", title="Alert")
                return
        except:
            npyscreen.notify_confirm("Incorrect Password", title="Alert")
            return
        
    def createAccount(self):
        # this creates new accounts
        user = self.username.value
        password = self.password.value
        if user == "":
            npyscreen.notify_confirm("Username is required", title="Alert")
            return
        if password == "":
            npyscreen.notify_confirm("Password is required", title="Alert")
            return

        known = getUserLoginData(user)
        if known is None:
            saveUserLoginData(user, password)
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
    # this is a simple form that acts as the main menu for the application.  
    # it allows the user to create new logins, view existing logins, or logout and return to the login screen. 

    def create(self):
        # create the main menu
        self.heading = self.add(npyscreen.TitleText, name = "Passcodes Homeform", editable = False)
        self.add(npyscreen.FixedText, value="-" * 40, rely=3, editable=False)
        self.add(npyscreen.ButtonPress, name = "View Logins", when_pressed_function = self.searchPasscodes)
        self.add(npyscreen.ButtonPress, name = "Create Login", when_pressed_function = self.createPasscode)
        self.add(npyscreen.ButtonPress, name = "Logout", when_pressed_function = self.logout)
        # self.add(npyscreen.ButtonPress, name = "Exit", when_pressed_function = self.exit)   # This is commented out for heroku deployment, uncomment to run locally. 

    def exit(self):
        self.parentApp.switchForm(None)

    def createPasscode(self):
        # switch to the create login form
        self.parentApp.switchForm("CreateLogin")

    def searchPasscodes(self):
        # switch to the view logins form
        self.parentApp.setNextForm("Home")
        self.parentApp.getForm("ViewLogins").update()
        self.parentApp.switchForm("ViewLogins")

    def logout(self):
        # log user out and return to login form
        self.parentApp.currentUser = None
        self.parentApp.masterPassword = None
        self.parentApp.getForm("MAIN").clear()
        self.parentApp.switchForm("MAIN")

class CreateLoginForm(npyscreen.ActionForm):
    # This form allows the user to create a new login record.  

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
        self.add(npyscreen.ButtonPress, name = "OK", when_pressed_function = self.on_ok)
        self.add(npyscreen.ButtonPress, name = "Cancel", when_pressed_function = self.on_cancel)
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

        if self.name.value == "":
            npyscreen.notify_confirm("Name field is required", title="Alert")
            return

        currentuser = self.parentApp.currentUser
        masterPassword = self.parentApp.masterPassword
        saveUserData(currentuser, self.name.value, self.username.value, self.password.value, self.url.value, masterPassword)

        self.clear()
        self.parentApp.switchForm("Home")

class viewLoginForm(npyscreen.ActionFormMinimal):
    # This form allows the user to view their logins.
    # By default all logins are shown, but the user can filter the results by name. 

    def create(self):
        # create the form widgets
        self.nameFilterLine = self.add(npyscreen.TitleText, name = "Name filter:", editable = True)
        self.add(npyscreen.FixedText, value="\u2500" * 40, editable=False)
        self.nameFilterLine.value_changed_callback = self.fill
        self.grid = self.add(npyscreen.GridColTitles, col_titles = ["Name", "Username", "URL"], selectable = True, select_whole_line = True)
        self.grid.add_handlers({curses.ascii.NL: self.itemPicked})
        self.records = []

    def itemPicked(self, thing=None):
        # display the selected login details
        try:
            selected_row = self.grid.selected_row()
        except:
            return 

        curses.def_prog_mode()
        curses.endwin()

        os.system('clear')
        print("\n {: >12} {: >12} {: >30} {: >20} \n".format(*["Name", "Username", "Password", "URL"]))
        print("\u2500" * 80)
        for record in self.records:
            if record[0]==selected_row[0]:        
                print("{: >12} {: >12} {: >30} {: >20}".format(*record))

        input('\n\nPress enter to continue...')
        curses.reset_prog_mode()

    def update(self):
        # get the records from the database and fill the grid
        self.nameFilterLine.value = ""
        self.records = getUserData(self.parentApp.currentUser, self.parentApp.masterPassword)
        self.fill()

    def fill(self, widget=None):
        # fill the grid with the login details, filtered by name
        if self.records == []: 
            self.grid.values = []
            return 
        shownRecords = {}
        for record in self.records:
            shownRecords[record[0]] = [record[0], record[1], record[3]]

        filter = str(self.nameFilterLine.value)
        self.grid.values = []
        for record in shownRecords.values():
            if filter.lower() in record[0].lower():
                self.grid.values.append(record)
        self.grid.display()
    
    def on_ok(self):
        # return to home form
        self.nameFilterLine.value = ""
        self.parentApp.switchForm("Home")
    



if __name__ == '__main__':
    # setup the database 
    setupStorage()

    #run the app     
    TA = MyTestApp()
    TA.run()

