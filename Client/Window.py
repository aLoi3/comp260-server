from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from queue import *
import sys
import os

qtCreatorFile = os.path.dirname(os.path.abspath(__file__))

Ui_MainWindow, QtBaseClass = uic.loadUiType(os.path.join(qtCreatorFile, "PyqtWindow.ui"))


class Window(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.input_manager = ''
        self.message_queue = Queue()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(100)
        self.client = ''

    def window_draw(self):
        app = QApplication(sys.argv)
        window = Window()
        window.show()
        sys.exit(app.exec_())

    def timerEvent(self):
        while self.message_queue.qsize() > 0:
            self.textEdit.append(self.message_queue.get())

    def text_enter(self):
        if self.lineEdit.text() is not '':
            self.input_manager.player_input(self.lineEdit.text())
        self.lineEdit.clear()

    def keyPressEvent(self, event):
        key = event.key()
        if key is Qt.Key_Return:
            self.text_enter()

    def closeEvent(self, event):
        self.client.is_running = False
        self.client.is_connected = False

        self.client.my_socket.close()
        self.client.my_socket = None

        if self.client.my_receive_thread is not None:
            self.client.my_receive_thread.join
        if self.client.my_connection_thread is not None:
            self.client.my_connection_thread.join

    def set_client(self, new_client):
        self.client = new_client
