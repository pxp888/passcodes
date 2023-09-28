import os
import curses
from helpers import *
from tui import *


class viewLoginForm(form):
    def __init__(self, screen):
        super().__init__(screen)

        self.nameFilterLine = lineEdit('Name filter: ')
        self.grid = filterList()
        self.okButton = button('( Back )')

        self.okButton.callback = self.on_ok
        self.nameFilterLine.pressCallback = self.grid.filter
        
        height, width = self.screen.getmaxyx()
        # self.grid.maxlen = height - 10
        self.grid.callback = self.itemPicked

        self.add(textline('View Logins'))
        
        self.add(textline('\u2500'*(width-4)))
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
        disp = list(disp.values())
        self.grid.setItems(disp)
        self.grid.draw()

    def itemPicked(self, thing=None):
        name = thing.currentSelection()
        out = []
        for record in self.records:
            if record[0] == name:
                out.append(record)

        height, width = self.screen.getmaxyx()
        h = height - 10
        w = width - 8
        if len(out) > (h-2):
            out = out[:h-2]
        y = 2
        x = 2
        win = curses.newwin(h, w, y, x)
        win.border()

        win.addstr(1, 1, "{: >18} {: >18} {: >32}".format(*["Username", "URL", "Password"]))
        win.addstr(2, 1, "\u2500" * (w-2))
        for i in range(len(out)):
            # win.addstr(i+3, 1, "{: >12} {: >40} {: >20}".format(*out[i][1:]))
            win.addstr(i+3, 1, "{: >18} {: >18} {: >32}".format(*[out[i][1], out[i][3], out[i][2]]))
        win.refresh()
        win.getch()
        del win
        self.draw()
