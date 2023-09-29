import os
import curses

"""
This file describes interface classes used to quickly
build a text-based user interface.
"""


class textline():
    """This is the base widget class.  By itself it only shows text."""
    def __init__(self, label=''):
        self.screen = None  # to be set during form.add()
        self.parent = None  # to be set during form.add()
        self.callback = None

        self.label = label
        self.y = 0
        self.x = 0
        self.focus = 0

    def draw(self):
        self.screen.addstr(self.y, self.x, self.label, curses.color_pair(2))

    def clear(self):
        self.draw()

    def remove(self, thing):
        self.screen.addstr(self.y, self.x, ' '*50)
        self.parent.stuff.remove(self)
        self.parent.active.remove(self)

    def keypress(self, key):
        if key == 'KEY_DOWN':
            if self.parent is not None:
                self.parent.focusNext()
        elif key == 'KEY_UP':
            if self.parent is not None:
                self.parent.focusPrev()


class lineEdit(textline):
    """This is a lineEdit with a label and an editable field.  To respond
    to the user pressing enter or return, set the callback function.
    To respond to individual keypresses, set the pressCallback function."""

    def __init__(self, label=''):
        super().__init__(label)
        self.value = ''
        self.focus = 1
        self.pressCallback = None

    def draw(self):
        if self.focus == 2:
            self.screen.addstr(self.y, self.x, ' '*50)
            self.screen.addstr(self.y, self.x, self.label, curses.A_REVERSE)
            self.screen.addstr(self.y, self.x + len(self.label), self.value, curses.A_REVERSE)
        else:
            self.screen.addstr(self.y, self.x, ' '*50)
            self.screen.addstr(self.y, self.x, self.label)
            self.screen.addstr(self.y, self.x + len(self.label), self.value)

    def keypress(self, key):
        if key == 'KEY_BACKSPACE':
            if len(self.value) > 0:
                self.value = self.value[:-1] + ' '
                self.draw()
                self.value = self.value[:-1]
                self.draw()
        elif key == '\n':
            if self.callback is not None:
                self.callback(self)
        elif key == 'KEY_DOWN':
            if self.parent is not None:
                self.parent.focusNext()
        elif key == 'KEY_UP':
            if self.parent is not None:
                self.parent.focusPrev()
        elif key == 'KEY_LEFT' or key == 'KEY_RIGHT' or key == 'KEY_NPAGE' or key == 'KEY_PPAGE':
            pass
        else:
            self.value += key
            self.draw()

        if self.pressCallback is not None:
            self.pressCallback(self)

    def clear(self):
        self.value = ''
        self.draw()


class button(textline):
    """This is effectively a button.  It is actually a selectable piece of
    text. To respond to the user pressing enter or return, set the callback
    function."""

    def __init__(self, label=''):
        super().__init__(label)
        self.focus = 1

    def draw(self):
        if self.focus == 2:
            self.screen.addstr(self.y, self.x, self.label, curses.A_REVERSE)
        else:
            self.screen.addstr(self.y, self.x, self.label, curses.color_pair(1))

    def keypress(self, key):
        super().keypress(key)
        if key == '\n' or key == ' ':
            if self.callback is not None:
                self.callback(self)


class checkbox(textline):
    """This is a basic checkbox, toggled with either space or enter."""
    def __init__(self, label='', value=True):
        super().__init__(label)
        self.focus = 1
        self.value = value

    def draw(self):
        msg = self.label + ' [ ]'
        if self.value:
            msg = self.label + ' [X]'
        if self.focus == 2:
            self.screen.addstr(self.y, self.x, msg, curses.A_REVERSE)
        else:
            self.screen.addstr(self.y, self.x, msg, curses.color_pair(1))

    def keypress(self, key):
        super().keypress(key)
        if key == '\n' or key == ' ':
            self.value = not self.value
            self.draw()
            if self.callback is not None:
                self.callback(self)


class filterList(textline):
    """This is a list of items that can be filtered by typing in a lineEdit.
    To respond to the user pressing enter or return, set the callback function.
    """

    def __init__(self, label=''):
        super().__init__(label)
        self.names = []
        self.items = []
        self.focus = 1
        self.selected = -1
        self.maxlen = 5
        self.fterm = ''

    def setItems(self, names):
        self.names = names[:self.maxlen]
        self.items = names
        self.fterm = ''
        self.selected = -1

    def draw(self):
        height, width = self.screen.getmaxyx()
        for i in range(self.maxlen):
            self.screen.addstr(self.y + i, self.x, ' '*(width-self.x))

        if self.fterm == '':
            self.names = self.items
        else:
            self.names = []
            for i in self.items:
                if self.fterm.lower() in i.lower():
                    self.names.append(i)

        if not self.names:
            self.screen.addstr(self.y, self.x, 'No entries found.')
            return

        if self.selected > -1:
            page = self.selected // self.maxlen
        else:
            page = 0

        start = page * self.maxlen
        end = start + self.maxlen

        for i in range(start, end):
            if i >= len(self.names):
                break
            if self.focus == 2 and i == self.selected:
                self.screen.addstr(self.y + i - start, self.x, self.names[i], curses.A_REVERSE)
            else:
                self.screen.addstr(self.y + i - start, self.x, self.names[i])
        self.screen.move(height-1, 0)

    def clear(self):
        height, width = self.screen.getmaxyx()
        for i in range(self.maxlen):
            self.screen.addstr(self.y + i, self.x, ' '*(width-self.x))

    def filter(self, thing):
        self.fterm = thing.value.lower()
        self.selected = -1
        self.draw()

    def keypress(self, key):
        if key == 'KEY_DOWN':
            if not self.names:
                pass
            elif self.selected == -1:
                self.selected = 0
            else:
                if self.names:
                    self.selected = (self.selected + 1) % len(self.names)
            self.draw()
        elif key == 'KEY_UP':
            if self.selected == 0:
                self.selected = -1
                self.parent.focusPrev()
            elif self.selected == -1:
                self.parent.focusPrev()
            else:
                if self.names:
                    self.selected = (self.selected - 1) % len(self.names)
                self.draw()
        elif key == '\n':
            if self.callback is not None:
                self.callback(self)
        elif key == 'KEY_NPAGE':
            if self.selected == -1:
                self.selected = 0
            else:
                self.selected = (self.selected + self.maxlen)
                if self.selected >= len(self.names):
                    self.selected = len(self.names) - 1
            self.draw()
        elif key == 'KEY_PPAGE':
            if self.selected == -1:
                self.selected = 0
            else:
                self.selected = (self.selected - self.maxlen)
                if self.selected < 0:
                    self.selected = 0
            self.draw()
        else:
            pass

    def currentSelection(self):
        if self.selected >= 0 and self.selected < len(self.names):
            return self.names[self.selected]
        else:
            return None


class form():
    """This is a container for widgets.  This manages the widgets.
    Which widget has focus, and directs keypresses to the correct widget.
    """

    def __init__(self, screen):
        self.screen = screen
        self.stuff = []
        self.focus = None
        self.active = []
        self.parentApp = None

    def add(self, thing, x=3, y=-1):
        """Add a widget to the form.  The x and y coordinates are relative
        to the form. If y is -1, the widget is added to the end of the list."""
        thing.screen = self.screen
        thing.parent = self
        if y == -1:
            y = len(self.stuff)
        thing.x = x
        thing.y = y

        self.stuff.append(thing)
        if thing.focus > 0:
            self.active.append(thing)

    def draw(self):
        self.screen.clear()
        if self.focus is None:
            if len(self.active) > 0:
                self.focus = self.active[0]
                self.active[0].focus = 2

        for n in self.stuff:
            n.draw()
        self.focus.draw()

    def focusNext(self):
        if self.focus is None:
            return
        self.focus.focus = 1
        self.focus.draw()
        idx = self.active.index(self.focus)
        idx += 1
        if idx >= len(self.active):
            idx = 0
        self.focus = self.active[idx]
        self.focus.focus = 2
        self.focus.draw()

    def focusPrev(self):
        if self.focus is None:
            return
        self.focus.focus = 1
        self.focus.draw()
        idx = self.active.index(self.focus)
        idx -= 1
        if idx < 0:
            idx = len(self.active) - 1
        self.focus = self.active[idx]
        self.focus.focus = 2
        self.focus.draw()

    def values(self):
        """This returns a dict with the values of widgets that have a label."""
        out = {}
        for i in self.active:
            if type(i) == lineEdit:
                out[i.label] = i.value
            elif type(i) == checkbox:
                out[i.label] = i.value
            elif type(i) == filterList:
                out[i.label] = i.currentSelection()
        return out

    def keypress(self, key):
        if self.focus is None:
            return
        if key == '\t':
            self.focusNext()
        elif key == 'KEY_BTAB':
            self.focusPrev()
        # elif key == 'KEY_DOWN':
        #     self.focusNext()
        # elif key == 'KEY_UP':
        #     self.focusPrev()
        else:
            self.focus.keypress(key)

    def alert(self, msg):
        """This displays a message to the user."""
        h = 5
        w = len(msg) + 6
        y = 5
        x = 10
        win = curses.newwin(h, w, y, x)
        win.border()
        win.addstr(2, 3, msg)
        win.refresh()
        win.getch()
        del win
        self.draw()

    def confirm(self, msg):
        """This displays a message and returns True if
        the user presses 'y' or 'Y'."""

        h = 7
        w = len(msg) + 6
        y = 5
        x = 10
        win = curses.newwin(h, w, y, x)
        win.border()
        win.addstr(2, 3, msg)
        win.addstr(4, 3, "Press 'Y' to accept")
        win.refresh()
        n = win.getch()
        del win
        self.draw()
        if n == ord('y') or n == ord('Y'):
            return True
        else:
            return False

    def clear(self):
        """This clears all widgets."""
        for i in self.stuff:
            i.clear()
        for i in self.active:
            i.focus = 1
        self.focus = self.active[0]
        self.focus.focus = 2
        self.draw()


class simpleTuiApp():
    """This is the main application class.
    It manages forms and keyboard presses."""

    def __init__(self, screen):
        self.screen = screen
        self.forms = {}
        self.currentForm = None

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

    def addform(self, name, nform):
        self.forms[name] = nform
        nform.parentApp = self

    def switchForm(self, name):
        self.currentForm = self.forms[name]
        self.currentForm.draw()

    def getForm(self, name):
        return self.forms[name]

    def run(self):
        while 1:
            n = self.screen.getkey()
            if n == '\x1b':  # escape
                pass
            else:
                self.currentForm.keypress(n)
