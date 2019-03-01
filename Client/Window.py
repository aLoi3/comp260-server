from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import Qt
from queue import *


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('pyqt/PyqtWindow.ui', self)
        self.input_manager = ''
        self.message_queue = Queue()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timer_event)
        self.timer.start(100)

    def window_draw(self):
        self.ui.show()

    def timer_event(self):
        while self.message_queue.qsize() > 0:
            self.plainTextEdit.appendPlainText(self.message_queue.get())

    def text_enter(self):
        if self.line_edit.text() is not '':
            self.input_manager.player_input(self.line_edit.text())
        self.line_edit.clear()

    def key_press_event(self, event):
        key = event.key()
        if key is Qt.Key_Return:
            self.text_enter()
