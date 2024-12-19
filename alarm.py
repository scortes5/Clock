from PyQt5 import QtWidgets, QtCore, QtMultimedia
from PyQt5.QtMultimedia import QSoundEffect
import os
import datetime
from customize import CircularSpinBox


class Alarm(QtWidgets.QMainWindow):
    back_to_home = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alarma")
        self.setGeometry(500, 200, 500, 400)
        
        # Initialize Alarm Variables
        self.alarm_active = False
        self.alarm_time = None

        # Central widget and layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        # Timer to update Chile time
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_chile_time)
        self.timer.start(1000)  # Update every second

        # Time label
        self.time_label = QtWidgets.QLabel()
        self.time_label.setStyleSheet("font-size: 36px; font-weight: bold")
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.time_label)
        self.update_chile_time()  # Set initial time

        # Input Fields for Alarm Time
        input_layout = QtWidgets.QHBoxLayout()

        # Get the current time
        current_time = datetime.datetime.now()

        self.hours_input = CircularSpinBox()
        self.hours_input.setRange(0, 23)
        self.hours_input.setValue(current_time.hour)  # Set to current hour

        self.minutes_input = CircularSpinBox()
        self.minutes_input.setRange(0, 59)
        self.minutes_input.setValue(current_time.minute)  # Set to current minute

        self.seconds_input = CircularSpinBox()
        self.seconds_input.setRange(0, 59)
        self.seconds_input.setValue(current_time.second)

        input_layout.addWidget(QtWidgets.QLabel("Horas:"))
        input_layout.addWidget(self.hours_input)
        input_layout.addWidget(QtWidgets.QLabel("Minutos:"))
        input_layout.addWidget(self.minutes_input)
        input_layout.addWidget(QtWidgets.QLabel("Segundos:"))
        input_layout.addWidget(self.seconds_input)
        layout.addLayout(input_layout)

        # Buttons to Set and Cancel Alarm
        button_layout = QtWidgets.QHBoxLayout()
        self.set_alarm_button = QtWidgets.QPushButton("Establecer Alarma")
        self.cancel_alarm_button = QtWidgets.QPushButton("Cancelar Alarma")
        button_layout.addWidget(self.set_alarm_button)
        button_layout.addWidget(self.cancel_alarm_button)
        layout.addLayout(button_layout)

        # Connect Buttons
        self.set_alarm_button.clicked.connect(self.set_alarm)
        self.cancel_alarm_button.clicked.connect(self.cancel_alarm)

        # Sound Selection
        self.sound_combo = QtWidgets.QComboBox()
        self.load_sounds()
        layout.addWidget(QtWidgets.QLabel("Selecciona un sonido:"))
        layout.addWidget(self.sound_combo)

        # Back Button
        self.back_button = QtWidgets.QPushButton("Volver al inicio")
        self.back_button.clicked.connect(self.go_back_to_home)
        layout.addWidget(self.back_button)



    def load_sounds(self):
        """Load sound files into the ComboBox without file extensions."""
        self.sound_folder = "sounds"  # Folder containing sound files
        if not os.path.exists(self.sound_folder):
            os.makedirs(self.sound_folder)  # Create folder if it doesn't exist
        
        self.sound_mapping = {}  # Dictionary to map display names to full file paths
        
        # List only .wav files for compatibility with QSoundEffect
        sound_files = [f for f in os.listdir(self.sound_folder) if f.endswith('.wav')]
        for sound in sound_files:
            name_without_extension = os.path.splitext(sound)[0]  # Remove the file extension
            self.sound_combo.addItem(name_without_extension)  # Add name to dropdown
            self.sound_mapping[name_without_extension] = os.path.join(self.sound_folder, sound)  # Map name to file path

    def update_chile_time(self):
        chile_tz = datetime.timezone(datetime.timedelta(hours=-3))  # Chile timezone (CLT)
        current_chile_time = datetime.datetime.now(chile_tz)
        self.time_label.setText(current_chile_time.strftime("%H:%M:%S"))

        # Check Alarm
        if self.alarm_active and self.alarm_time:
            if current_chile_time.strftime("%H:%M:%S") == self.alarm_time.strftime("%H:%M:%S"):
                self.play_sound()
                self.alarm_active = False  # Deactivate alarm after it rings

    def set_alarm(self):
        """Set the alarm based on the input fields."""
        chile_tz = datetime.timezone(datetime.timedelta(hours=-3))  # Chile timezone (CLT)
        now = datetime.datetime.now(chile_tz)
        self.alarm_time = now.replace(
            hour=self.hours_input.value(),
            minute=self.minutes_input.value(),
            second=self.seconds_input.value(),
            microsecond=0
        )
        self.alarm_active = True
        QtWidgets.QMessageBox.information(self, "Alarma", f"Alarma establecida para {self.alarm_time.strftime('%H:%M:%S')}")

    def cancel_alarm(self):
        """Cancel the currently active alarm."""
        self.alarm_active = False
        self.alarm_time = None
        QtWidgets.QMessageBox.information(self, "Alarma", "Alarma cancelada.")

    def play_sound(self):
        """Play the selected sound using QSoundEffect."""
        selected_display_name = self.sound_combo.currentText()  # Get the selected name from the dropdown
        sound_path = self.sound_mapping.get(selected_display_name)  # Retrieve the full file path
        if sound_path:
            self.sound_effect = QSoundEffect()
            self.sound_effect.setSource(QtCore.QUrl.fromLocalFile(sound_path))  # Set the file URL
            self.sound_effect.setVolume(1.0)  # Volume range: 0.0 to 1.0
            self.sound_effect.play()
            QtWidgets.QMessageBox.information(self, "Alarma", "¡La alarma está sonando!")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "No se pudo cargar el sonido seleccionado.")

    def go_back_to_home(self):
        self.timer.stop()
        self.back_to_home.emit()

    def run(self):
        self.show()
