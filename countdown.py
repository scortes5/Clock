from PyQt5 import QtWidgets, QtCore, QtMultimedia
from PyQt5.QtMultimedia import QSoundEffect
import os

class CountDown(QtWidgets.QMainWindow):
    back_to_home = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Temporizador")
        self.setGeometry(500, 200, 500, 400)

        # Central widget and layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        # Display Label
        self.time_label = QtWidgets.QLabel("00:00:00")
        self.time_label.setStyleSheet("font-size: 48px; font-weight: bold;")
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.time_label)

        # Input Fields
        input_layout = QtWidgets.QHBoxLayout()
        self.hours_input = QtWidgets.QSpinBox()
        self.hours_input.setRange(0, 23)
        self.minutes_input = QtWidgets.QSpinBox()
        self.minutes_input.setRange(0, 59)
        self.seconds_input = QtWidgets.QSpinBox()
        self.seconds_input.setRange(0, 59)

        input_layout.addWidget(QtWidgets.QLabel("Horas"))
        input_layout.addWidget(self.hours_input)
        input_layout.addWidget(QtWidgets.QLabel("Minutos"))
        input_layout.addWidget(self.minutes_input)
        input_layout.addWidget(QtWidgets.QLabel("Segundos"))
        input_layout.addWidget(self.seconds_input)
        layout.addLayout(input_layout)

        # Control Buttons
        button_layout = QtWidgets.QHBoxLayout()
        self.start_button = QtWidgets.QPushButton("Iniciar")
        self.stop_button = QtWidgets.QPushButton("Pausa")
        self.reset_button = QtWidgets.QPushButton("Resetear")

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.reset_button)
        layout.addLayout(button_layout)

        # Sound Selection
        self.sound_combo = QtWidgets.QComboBox()
        self.load_sounds()
        layout.addWidget(QtWidgets.QLabel("Selecciona un sonido:"))
        layout.addWidget(self.sound_combo)

        # Back Button
        self.back_button = QtWidgets.QPushButton("Volver al inicio")
        self.back_button.clicked.connect(self.go_back_to_home)
        layout.addWidget(self.back_button)

        # Progress Bar
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_bar.setStyleSheet("font-size: 16px; color: blue;")
        layout.addWidget(self.progress_bar)

        # Connect Buttons to Slots
        self.start_button.clicked.connect(self.start_timer)
        self.stop_button.clicked.connect(self.stop_timer)
        self.reset_button.clicked.connect(self.reset_timer)

        # Timer Initialization
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.remaining_seconds = 0
        self.total_seconds = 0
        self.timer_running = False

        # Media Player for Sound
        self.media_player = QtMultimedia.QMediaPlayer()

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



    def start_timer(self):
        if not self.timer_running:
            hours = self.hours_input.value()
            minutes = self.minutes_input.value()
            seconds = self.seconds_input.value()
            self.remaining_seconds = hours * 3600 + minutes * 60 + seconds
            self.total_seconds = self.remaining_seconds
            if self.remaining_seconds > 0:
                self.timer_running = True
                self.timer.start(1000)
                self.start_button.setEnabled(False)
                self.progress_bar.setMaximum(self.total_seconds)
                self.progress_bar.setValue(self.remaining_seconds)

    def stop_timer(self):
        self.timer.stop()
        self.timer_running = False
        self.start_button.setEnabled(True)

    def reset_timer(self):
        self.timer.stop()
        self.timer_running = False
        self.remaining_seconds = 0
        self.time_label.setText("00:00:00")
        self.progress_bar.setValue(0)
        self.start_button.setEnabled(True)
        self.hours_input.setValue(0)
        self.minutes_input.setValue(0)
        self.seconds_input.setValue(0)

    def update_timer(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            hours, remainder = divmod(self.remaining_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.time_label.setText(f"{hours:02}:{minutes:02}:{seconds:02}")
            self.progress_bar.setValue(self.remaining_seconds)
        else:
            self.timer.stop()
            self.timer_running = False
            self.play_sound()
            self.start_button.setEnabled(True)

    def play_sound(self):
        """Play the selected sound using QSoundEffect."""
        selected_display_name = self.sound_combo.currentText()  # Get the selected name from the dropdown
        sound_path = self.sound_mapping.get(selected_display_name)  # Retrieve the full file path
        if sound_path:
            print(f"Playing sound: {sound_path}")  # Debugging line
            
            # Initialize QSoundEffect and set its properties
            self.sound_effect = QSoundEffect()
            self.sound_effect.setSource(QtCore.QUrl.fromLocalFile(sound_path))  # Set the file URL
            self.sound_effect.setVolume(1.0)  # Volume range: 0.0 to 1.0
            self.sound_effect.play()  # Play the sound
            
            # Debugging line to confirm playback
            if self.sound_effect.isLoaded():
                print("Sound loaded and played successfully.")
            else:
                print("Sound failed to load.")
        else:
            print("No sound selected or mapping issue.")



    def go_back_to_home(self):
        self.timer.stop()
        self.back_to_home.emit()

    def run(self):
        self.show()
