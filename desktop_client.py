import sys
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

class CameraControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.capture_btn = QPushButton('Capture', self)
        self.capture_btn.clicked.connect(self.send_capture_command)
        self.capture_btn.resize(self.capture_btn.sizeHint())
        self.capture_btn.move(50, 50)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Camera Control')
        self.show()

    def send_capture_command(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('YOURIP', 12345))
        client_socket.send("capture".encode('utf-8'))
        client_socket.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CameraControlApp()
    sys.exit(app.exec_())

