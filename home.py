from PyQt5 import QtWidgets, QtGui, QtCore
import datetime
from countdown import CountDown
from stopwatch import StopWatch


class HomeView(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home")
        self.setGeometry(500, 200, 500, 500)

        # Set central widget
        self.central_widget = BackgroundWidget("background.jpg")  # Pass image path
        self.setCentralWidget(self.central_widget)

        # Layout
        layout = QtWidgets.QVBoxLayout(self.central_widget)

        # Timer to update Chile time
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_chile_time)
        self.timer.start(1000)  # Update every second

        # Time label
        self.time_label = QtWidgets.QLabel()
        self.time_label.setStyleSheet("font-size: 36px; font-weight: bold; color: white;")
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.time_label)
        self.update_chile_time()  # Set initial time

        # Countdown button
        self.countdown_button = QtWidgets.QPushButton("Temporizador")
        self.countdown_button.setStyleSheet("font-size: 20px; background-color: rgba(0,0,0,0.3); color: white; border-radius: 5px; padding: 10px;")
        self.countdown_button.clicked.connect(self.show_countdown)
        layout.addWidget(self.countdown_button)

        # Stopwatch button
        self.stopwatch_button = QtWidgets.QPushButton("Cronometro")
        self.stopwatch_button.setStyleSheet("font-size: 20px; background-color: rgba(0,0,0,0.3); color: white; border-radius: 5px; padding: 10px;")
        self.stopwatch_button.clicked.connect(self.show_stopwatch)
        layout.addWidget(self.stopwatch_button)

    def update_chile_time(self):
        chile_tz = datetime.timezone(datetime.timedelta(hours=-3))  # Chile timezone (CLT)
        current_chile_time = datetime.datetime.now(chile_tz).strftime("%H:%M:%S")
        self.time_label.setText(f"{current_chile_time}")
    
    def show_countdown(self):
        self.hide()  # Hide the home screen
        self.countdown_window = CountDown()
        self.countdown_window.back_to_home.connect(self.show_home)  # Connect the signal
        self.countdown_window.show()  # Show the countdown window

    def show_stopwatch(self):
        self.hide()
        self.stopwatch_window = StopWatch()
        self.stopwatch_window.back_to_home.connect(self.show_home)
        self.stopwatch_window.show()


    def show_home(self):
        try:
            self.countdown_window.close()
        except: 
            self.stopwatch_window.close()
        finally:   
            self.show()  

    

    def run(self):
        self.show()

    


class BackgroundWidget(QtWidgets.QWidget):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.image_path = image_path

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pixmap = QtGui.QPixmap(self.image_path)
        painter.drawPixmap(self.rect(), pixmap)



