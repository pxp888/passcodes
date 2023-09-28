import os
import curses
import npyscreen
from helpers import *
from tui import *

class viewLoginForm(npyscreen.ActionFormMinimal):
    # This form allows the user to view their logins.
    # By default all logins are shown, but the user can filter the results by name.

    def create(self):
        # create the form widgets
        self.nameFilterLine = self.add(npyscreen.TitleText, name="Name filter:", editable=True)
        self.nameFilterLine.value_changed_callback = self.fill
        self.add(npyscreen.FixedText, value="\u2500" * 40, editable=False)
        self.grid = self.add(npyscreen.GridColTitles, col_titles=["Name", "Username", "URL"], selectable=True, select_whole_line=True)
        self.grid.add_handlers({curses.ascii.NL: self.itemPicked})
        self.records = []

    def itemPicked(self, thing=None):
        # display the selected login details
        try:
            selected_row = self.grid.selected_row()
        except curses.error:
            return

        curses.def_prog_mode()
        curses.endwin()

        os.system('clear')
        print("\n {: >12} {: >12} {: >30} {: >20} \n".format(*["Name", "Username", "Password", "URL"]))
        print("\u2500" * 80)
        for record in self.records:
            if record[0] == selected_row[0]:
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


class sviewLoginForm(form):
    def __init__(self, screen):
        super().__init__(screen)

        self.nameFilterLine = lineEdit('Name filter: ')
        self.grid = filterList()
        self.okButton = button('( Back )')

        self.okButton.callback = self.on_ok

        self.nameFilterLine.pressCallback = self.grid.filter
        
        width, height = self.screen.getmaxyx()
        self.grid.maxlen = height - 7
        self.grid.callback = self.itemPicked

        self.add(textline('View Logins'))
        width, height = self.screen.getmaxyx()
        self.add(textline('\u2500'*(width-2)))
        self.add(self.okButton)
        self.add(self.nameFilterLine)
        self.add(textline('-'*40))
        self.add(self.grid)
        
        self.records = []

    def on_ok(self, thing=None):
        self.parentApp.switchForm("Home")

    def update(self):
        self.nameFilterLine.value = ""
        self.records = getUserData(self.parentApp.currentUser, self.parentApp.masterPassword)
        
        disp = {}
        for record in self.records:
            # disp[record[0]] = "{: >30} {: >30}".format(*[record[0], record[3]])
            disp[record[0]] = record[0]
        self.grid.setItems(list(disp.values()))
        self.grid.draw()

    def itemPicked(self, thing=None):
        name = thing.currentSelection()
        out = []
        for record in self.records:
            if record[0] == name:
                out.append(record)

        width, height = self.screen.getmaxyx()
        h = height - 10
        w = width - 8
        if len(out) > (h-2):
            out = out[:h-2]
        y = 2
        x = 2
        win = curses.newwin(h, w, y, x)
        win.border()

        win.addstr(1, 1, "{: >12} {: >30} {: >20}".format(*["Username", "Password", "URL"]))
        win.addstr(2, 1, "\u2500" * (w-2))
        for i in range(len(out)):
            win.addstr(i+3, 1, "{: >12} {: >30} {: >20}".format(*out[i][1:]))

        win.refresh()
        win.getch()
        del win
        self.draw()
