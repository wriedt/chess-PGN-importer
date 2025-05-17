import os
import sys

# Add the 'lib' directory to the Python path
addon_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(addon_dir, 'lib')
if lib_dir not in sys.path:
    sys.path.append(lib_dir)

from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo, qconnect

from .ui import get_pgn_and_title
from .note_creator import create_notes_from_pgn

def on_pgn_add():
    pgn_text, title, is_black = get_pgn_and_title()
    if pgn_text and title is not None:
        create_notes_from_pgn(pgn_text, title, is_black)
        showInfo("Notes created successfully!")
    else:
        showInfo("PGN import cancelled.")

# Create a new menu item
action = QAction("Add Chess PGN", mw)
qconnect(action.triggered, on_pgn_add)
mw.form.menuTools.addAction(action)