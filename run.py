import sys
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


def main(stdscr):
    stdscr.clear()
    stdscr.refresh()
    curses.curs_set(0)

    logform = sloginForm(stdscr)
    homeform = shomeForm(stdscr)
    createform = screateLoginForm(stdscr)
    viewform = sviewLoginForm(stdscr)

    app = stuiApp(stdscr)
    app.addform("MAIN", logform)
    app.addform("Home", homeform)
    app.addform("CreateLogin", createform)
    app.addform("ViewLogins", viewform)

    app.switchForm("MAIN")
    app.run()
    
wrapper(main)
