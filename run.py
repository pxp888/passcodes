import sys
import npyscreen
from curses import wrapper
import curses

sys.path.append("assets/python")
from assets.python.tui import *
from assets.python.loginform import *
from assets.python.homeform import *
from assets.python.createloginform import *
from assets.python.viewloginform import *


# This is a simple password manager that uses a master password to encrypt
# and decrypt passwords
# Passwords are stored in a database and encrypted with the master password
# The master password is hashed and stored in the database


# class MyTestApp(npyscreen.NPSAppManaged):
#     # This is the main application instance.
#     def __init__(self):
#         super(MyTestApp, self).__init__()
#         # the current user and master password are stored here,
#         # to make them available to all forms.
#         self.currentUser = None
#         self.masterPassword = None

#     def onStart(self):
#         # create forms and associate them with the app
#         self.registerForm("MAIN", LoginForm())
#         self.registerForm("Home", HomeForm())
#         self.registerForm("CreateLogin", CreateLoginForm())
#         self.registerForm("ViewLogins", viewLoginForm())

# if __name__ == '__main__':
#     TA = MyTestApp()
#     TA.run()


def main(stdscr):
    stdscr.clear()
    stdscr.refresh()
    curses.curs_set(0)

    logform = sloginForm(stdscr)
    homeform = shomeForm(stdscr)

    app = stuiApp(stdscr)
    app.addform("MAIN", logform)
    app.addform("Home", homeform)

    app.switchForm("MAIN")
    app.run()
    
wrapper(main)
