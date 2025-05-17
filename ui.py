from aqt.qt import *
from aqt.utils import showInfo

def show_pgn_dialog():
    dialog = QDialog()
    dialog.setWindowTitle("Enter PGN")
    
    layout = QVBoxLayout()
    
    pgn_text = QPlainTextEdit()
    pgn_text.setPlaceholderText("Paste your PGN here...")
    layout.addWidget(pgn_text)
    
    # Add checkbox
    black_perspective = QCheckBox("View from Black's perspective")
    layout.addWidget(black_perspective)
    
    buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)
    layout.addWidget(buttons)
    
    dialog.setLayout(layout)
    
    result = dialog.exec()
    if result:
        return (pgn_text.toPlainText(), black_perspective.isChecked())
    return (None, False)  # Return a tuple with default values

def show_title_dialog():
    title, ok = QInputDialog.getText(None, "Enter Title", "Enter a title for this chess game:")
    if ok and title:
        return title
    return None

def get_pgn_and_title():
    pgn_result = show_pgn_dialog()
    if pgn_result[0]:  # If pgn_text is not None
        pgn_text, is_black = pgn_result
        title = show_title_dialog()
        if title:
            return pgn_text, title, is_black
    return None, None, False