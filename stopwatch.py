from PyQt5 import QtWidgets, QtCore


class StopWatch(QtWidgets.QMainWindow):
    back_to_home = QtCore.pyqtSignal()  # Signal to go back to the home screen

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cronómetro")
        self.setGeometry(500, 200, 500, 400)

        # Initialize Timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.time = QtCore.QTime(0, 0, 0, 0)
        self.timer_running = False

        # Create central widget and layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        # Display Label
        self.time_label = QtWidgets.QLabel("00:00:00")
        self.time_label.setStyleSheet("font-size: 48px; font-weight: bold;")
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.time_label)

        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        self.start_button = QtWidgets.QPushButton("Iniciar")
        self.stop_button = QtWidgets.QPushButton("Pausar")
        self.reset_button = QtWidgets.QPushButton("Resetear")

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.reset_button)
        layout.addLayout(button_layout)

        # Go Back Button
        self.back_button = QtWidgets.QPushButton("Volver al inicio")
        self.back_button.clicked.connect(self.go_back_to_home)
        layout.addWidget(self.back_button)

        # Connect Buttons
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.reset_button.clicked.connect(self.reset)

    def start(self):
        if not self.timer_running:  # Start the timer
            self.timer.start(10)  # Update every second
            self.timer_running = True
            self.start_button.setEnabled(False)  # Disable start button while running

    def stop(self):
        if self.timer_running:  # Stop the timer
            self.timer.stop()
            self.timer_running = False
            self.start_button.setEnabled(True)

    def reset(self):
        self.timer.stop()
        self.timer_running = False
        self.time = QtCore.QTime(0, 0, 0, 0)
        self.update_label()
        self.start_button.setEnabled(True)

    def update_timer(self):
        # Increment time by one second
        self.time = self.time.addSecs(1)
        self.update_label()

    def update_label(self):
        # Update the display label with the current time
        self.time_label.setText(self.time.toString("HH:hh:mm:ss"))

    def go_back_to_home(self):
        self.timer.stop()  # Stop the timer before going back
        self.back_to_home.emit()  # Emit the signal to go back to home

    def run(self):
        self.show()


