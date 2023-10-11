import time
from datetime import datetime
import socket
import threading
import curses
from picamera2 import Picamera2, Preview
from libcamera import controls

class CameraApp:
    def __init__(self):
        # Initialize the camera and configure it
        self.picam2 = Picamera2()
        self._configure_camera()

    def _configure_camera(self):
        """Set up the camera with the desired configuration."""
        still_config = self.picam2.create_still_configuration(
            main={"size": (4000, 4000)},
            lores={"size": (640, 480)},
            display="lores"
        )
        self.picam2.configure(still_config)

    def capture(self):
        """Capture an image with the camera."""
        self.picam2.start_preview(Preview.QTGL)
        timestamp = datetime.now().isoformat()
        self.picam2.start()
        time.sleep(1)
        self.picam2.capture_file(f'/home/pi/Desktop/shared/{timestamp}.jpg')
        self.picam2.stop_preview()
        self.picam2.stop()

    def main(self, stdscr):
        """Main loop to listen for key presses."""
        stdscr.nodelay(1)  # Do not wait for input when calling getch
        while True:
            c = stdscr.getch()
            if c == ord('f'):
                stdscr.addstr(0, 0, "F key pressed!")
                print("F key pressed!")
                self.picam2.set_controls({
                    "AwbMode": 4,
                    "AfMode": controls.AfModeEnum.Manual,
                    "LensPosition": 6.0,
                    "ExposureTime": 500000,
                    "AnalogueGain": 8.0
                })
                time.sleep(1)
                self.capture()
            elif c == ord('q'):
                break  # Exit the loop if 'q' is pressed

    def remote_control(self):
        """Method to handle remote commands."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', 12345))
        server_socket.listen(5)

        while True:
            client, addr = server_socket.accept()
            command = client.recv(1024).decode('utf-8')
            if command == "capture":
                self.capture()
            elif command == "quit":
                break
            client.close()
        server_socket.close()


if __name__ == "__main__":
    app = CameraApp()

    mode = input("Choose mode (local/remote): ").strip().lower()
    if mode == "local":
        curses.wrapper(app.main)
    elif mode == "remote":
        app.remote_control()
