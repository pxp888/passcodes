import os
import curses
import npyscreen

from helpers import * 


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
