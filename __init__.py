# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import QAction

import sys
# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.


def testFunction():
    # get the number of cards in the current collection, which is stored in
    # the main window
    # show a message box
    # showInfo(repr(cardCount))
    item = mw.col.decks.deck_tree().children
    sys.stderr.write(str(dir(item)))


"""
<class 'backend_pb2.DeckNameID'>
"""


# create a new menu item, "test"
action = QAction("test", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
