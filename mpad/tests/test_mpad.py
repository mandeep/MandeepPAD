from mpad import editor
import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtWidgets import QApplication, QFileDialog, QFontDialog, QMessageBox, QInputDialog


@pytest.fixture
def window(qtbot):
    new_window = editor.TextEditor()
    qtbot.add_widget(new_window)
    new_window.show()
    return new_window


def test_window(window):
    """Tests the window title and that the window icon is visible."""
    assert window.windowTitle() == 'MandeepPAD'
    assert window.windowIcon().isNull() is False


def test_geometry(window):
    """Tests the default window geometry."""
    assert window.width() == 1024
    assert window.height() == 768


def test_text_area(qtbot, window):
    """Tests that the text is being inserted into the text area."""
    sentence = 'They gave my red hat to the donkey.'
    cursor = window.text.textCursor()
    qtbot.add_widget(cursor)
    cursor.insertText(sentence)
    cursor.select(3)
    assert cursor.selectedText() == sentence
    assert window.text.tabStopWidth() == 50


def test_bars(window):
    """Tests whether the widget contains a status bar and menu bar.
    """
    assert window.statusBar().isVisible()
    assert window.menuBar().isVisible()


def test_menu_bar(window):
    """Tests whether the menu items appear on the menu bar.
    """
    assert window.file.isEnabled()
    assert window.edit.isEnabled()
    assert window.form.isEnabled()
    assert window.tools.isEnabled()
    assert window.view.isEnabled()
    assert window.help_option.isEnabled()


def test_new_file(qtbot, window):
    """Qtbot simulates clicks inside the text editor window to ensure
    that a new window opens when New File is selected.
    """
    qtbot.mouseClick(window.file, Qt.LeftButton)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Enter)


def test_open_file(qtbot, mock, window):
    """Qtbot simulates clicks inside the text editor window to ensure
    that an open file dialog opens when Open File is selected."""
    qtbot.mouseClick(window.file, Qt.LeftButton)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    mock.patch.object(QFileDialog, 'getOpenFileName', return_value=('.travis.yml', '*.txt'))
    window.open_file()


def test_save_file(qtbot, mock, window):
    """Qtbot simulates clicks inside the text editor window to ensure
    that a save file dialog opens when Save File is selected."""
    qtbot.mouseClick(window.file, Qt.LeftButton)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    mock.patch.object(QFileDialog, 'getSaveFileName', return_value=('', ''))
    window.save_file()


def test_print_file(qtbot, mock, window):
    """Qtbot simulates clicks inside the text editor window to ensure
    that a save file dialog opens when Save File is selected."""
    qtbot.mouseClick(window.file, Qt.LeftButton)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    mock.patch.object(QPrintDialog, 'exec_', return_value='accept')
    qtbot.keyClick(window.file, Qt.Key_Enter)


def test_quit_application(qtbot, monkeypatch, window):
    """Qtbot scolls through menu items and monkeypatch intercepts the quit
    application call prior to it being called."""
    exit_calls = []
    monkeypatch.setattr(QApplication, 'quit', lambda: exit_calls.append(1))
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Enter)
    assert exit_calls == [1]


def test_undo_action(qtbot, window):
    """Inserts text into the text area then qtbot navigates to Undo
    and selects it.
    """
    sentence = "My back. There goes my back again."
    cursor = window.text.textCursor()
    qtbot.add_widget(cursor)
    cursor.insertText(sentence)
    qtbot.mouseClick(window.edit, Qt.LeftButton)
    qtbot.keyClick(window.edit, Qt.Key_Down)
    qtbot.keyClick(window.edit, Qt.Key_Enter)
    cursor.select(3)
    assert cursor.selectedText() is ''


def test_redo_action(qtbot, window):
    """Inserts text into the text area then qtbot navigates to Undo
    and selects it. Qtbot  then navigates to the redo action and
    selects it.
    """
    sentence = "Oh, hello, Principal Skinner. I'd get up, but the boy crippled me."
    cursor = window.text.textCursor()
    qtbot.add_widget(cursor)
    cursor.insertText(sentence)
    qtbot.mouseClick(window.edit, Qt.LeftButton)
    qtbot.keyClick(window.edit, Qt.Key_Down)
    qtbot.keyClick(window.edit, Qt.Key_Enter)
    qtbot.mouseClick(window.edit, Qt.LeftButton)
    qtbot.keyClick(window.edit, Qt.Key_Down)
    qtbot.keyClick(window.edit, Qt.Key_Enter)
    cursor.select(3)
    assert cursor.selectedText() == sentence


def test_delete_action(qtbot, window):
    """Inserts text into the text area then qtbot navigates to Delete
    and selects it.
    """
    sentence = "Go get help, Dog."
    cursor = window.text.textCursor()
    qtbot.add_widget(cursor)
    cursor.insertText(sentence)
    qtbot.mouseClick(window.edit, Qt.LeftButton)
    qtbot.keyClick(window.edit, Qt.Key_Down)
    qtbot.keyClick(window.edit, Qt.Key_Down)
    qtbot.keyClick(window.edit, Qt.Key_Down)
    qtbot.keyClick(window.edit, Qt.Key_Down)
    qtbot.keyClick(window.edit, Qt.Key_Down)
    qtbot.keyClick(window.edit, Qt.Key_Down)
    qtbot.keyClick(window.edit, Qt.Key_Enter)


def test_select_all(qtbot, window):
    """Inserts text into the text area then qtbot navigates to the Select
    All item and seelcts it."""
    sentence = "Oh, the boy. Bring me the boy."
    cursor = window.text.textCursor()
    qtbot.add_widget(cursor)
    cursor.insertText(sentence)
    qtbot.mouseClick(window.edit, Qt.LeftButton)
    qtbot.keyClick(window.edit, Qt.Key_Down)
    qtbot.keyClick(window.edit, Qt.Key_Down)
    qtbot.keyClick(window.edit, Qt.Key_Down)
    qtbot.keyClick(window.edit, Qt.Key_Down)
    qtbot.keyClick(window.edit, Qt.Key_Down)
    qtbot.keyClick(window.edit, Qt.Key_Down)
    qtbot.keyClick(window.edit, Qt.Key_Down)
    qtbot.keyClick(window.edit, Qt.Key_Enter)


def test_font_dialog(qtbot, mock, window):
    """Qtbot opens the format menu and selects the Change Font item."""
    qtbot.mouseClick(window.form, Qt.LeftButton)
    qtbot.keyClick(window.form, Qt.Key_Down)
    mock.patch.object(QFontDialog, 'getFont', return_value=('', ''))
    qtbot.keyClick(window.form, Qt.Key_Enter)


def test_bold_font(qtbot, window):
    """Qtbot opens the format menu and selects the Bold item."""
    qtbot.mouseClick(window.form, Qt.LeftButton)
    qtbot.keyClick(window.form, Qt.Key_Down)
    qtbot.keyClick(window.form, Qt.Key_Down)
    qtbot.keyClick(window.edit, Qt.Key_Enter)


def test_italic_font(qtbot, window):
    """Qtbot opens the format menu and selects the Italicize item."""
    qtbot.mouseClick(window.form, Qt.LeftButton)
    qtbot.keyClick(window.form, Qt.Key_Down)
    qtbot.keyClick(window.form, Qt.Key_Down)
    qtbot.keyClick(window.form, Qt.Key_Down)
    qtbot.keyClick(window.edit, Qt.Key_Enter)


def test_underline_font(qtbot, window):
    """Qtbot opens the format menu and selects the Underline item."""
    qtbot.mouseClick(window.form, Qt.LeftButton)
    qtbot.keyClick(window.form, Qt.Key_Down)
    qtbot.keyClick(window.form, Qt.Key_Down)
    qtbot.keyClick(window.form, Qt.Key_Down)
    qtbot.keyClick(window.form, Qt.Key_Down)
    qtbot.keyClick(window.edit, Qt.Key_Enter)


def test_text_search(qtbot, mock, window):
    """Qtbot opens the tools menu and selects the Find text item."""
    qtbot.mouseClick(window.tools, Qt.LeftButton)
    qtbot.keyClick(window.tools, Qt.Key_Down)
    mock.patch.object(QInputDialog, 'getText', return_value=('Hi!', True))
    qtbot.keyClick(window.tools, Qt.Key_Enter)


def test_date(qtbot, window):
    """Qtbot opens the tools menu and selects the Insert Date item."""
    cursor = window.text.textCursor()
    qtbot.add_widget(cursor)
    qtbot.mouseClick(window.tools, Qt.LeftButton)
    qtbot.keyClick(window.tools, Qt.Key_Down)
    qtbot.keyClick(window.tools, Qt.Key_Down)
    qtbot.keyClick(window.tools, Qt.Key_Down)
    qtbot.keyClick(window.tools, Qt.Key_Enter)
    cursor.select(3)
    assert '2017' in cursor.selectedText()


def test_menu_bar_visibility(qtbot, window):
    """Qtbot opens the view menu and selects the Hide Menu Bar item."""
    qtbot.mouseClick(window.view, Qt.LeftButton)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Enter)
    assert window.menu_bar.isVisible() is False


def test_tool_bar_visibility(qtbot, window):
    """Qtbot opens the view menu and selects the Hide Tool Bar item."""
    qtbot.mouseClick(window.view, Qt.LeftButton)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Enter)
    assert window.toolbar.isVisible() is False


def test_status_bar_visibility(qtbot, window):
    """Qtbot opens the view menu and selects the Hide Status Bar item."""
    qtbot.mouseClick(window.view, Qt.LeftButton)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Enter)
    assert window.status_bar.isVisible() is False


def test_about(qtbot, mock, window):
    """Qtbot opens the help menu and mock executes the about message box."""
    qtbot.mouseClick(window.help_option, Qt.LeftButton)
    qtbot.keyClick(window.help_option, Qt.Key_Down)
    mock.patch.object(QMessageBox, 'exec_', return_value='accept')
    qtbot.keyClick(window.help_option, Qt.Key_Enter)
