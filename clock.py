from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtWidgets import QGridLayout, QStackedLayout, QTabWidget, QVBoxLayout
from PyQt5.QtGui import QIcon, QFont, QIntValidator
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtMultimedia import QSound
import sys


class TimerWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.play_icon = "timer_assets/play.png"
        self.pause_icon = "timer_assets/pause.png"
        self.reset_icon = "timer_assets/reset.png"
        self.alarm_sound = "timer_assets/alarm.wav"

        self.timer_duration = QTime(0, 5, 0)
        self.zero_time = QTime(0, 0, 0)
        self.timer_is_running = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.init_window()

    def init_window(self):

        self.stack = QStackedLayout()
        self.stack.addWidget(self.create_timer_window())
        self.stack.addWidget(self.create_change_time_window())

        self.setLayout(self.stack)

    def change_window(self, index):
        self.stack.setCurrentIndex(index)

        if self.stack.currentIndex() == 0:
            self.display_timer_time()

    # WINDOW
    def create_timer_window(self):
        # shows timer window

        self.timer_time = self.timer_duration

        self.timer_time_label = QLabel()
        self.timer_time_label.setAlignment(Qt.AlignCenter)
        self.timer_time_label.setFont(QFont("Arial", 20))

        self.display_timer_time()

        self.change_time_button = QPushButton("Change Time")
        self.change_time_button.setFixedWidth(200)
        self.change_time_button.clicked.connect(lambda: self.change_window(1))

        self.reset_timer_button = QPushButton()
        self.reset_timer_button.setIcon(QIcon(self.reset_icon))
        self.reset_timer_button.setFixedWidth(200)
        self.reset_timer_button.clicked.connect(self.reset_timer)

        self.toggle_timer_button = QPushButton()
        self.toggle_timer_button.setIcon(QIcon(self.play_icon))
        self.toggle_timer_button.setFixedWidth(200)
        self.toggle_timer_button.clicked.connect(self.toggle_timer)

        if self.timer_time == self.zero_time:
            self.toggle_timer_button.setDisabled(True)
        else:
            self.toggle_timer_button.setDisabled(False)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.timer_time_label)
        self.vbox.addWidget(self.change_time_button, alignment=Qt.AlignHCenter)
        self.vbox.addWidget(self.reset_timer_button, alignment=Qt.AlignHCenter, stretch=1)
        self.vbox.addWidget(self.toggle_timer_button, alignment=Qt.AlignHCenter, stretch=2)

        self.timer_widget = QWidget()
        self.timer_widget.setLayout(self.vbox)

        return self.timer_widget

    def display_timer_time(self):
        self.timer_time_label.setText(self.timer_time.toString("hh:mm:ss"))

    # EFFECT
    def change_timer_button_logo(self, action):

        if action == "start":
            self.toggle_timer_button.setIcon(QIcon(self.play_icon))
        elif action == "pause":
            self.toggle_timer_button.setIcon(QIcon(self.pause_icon))

    # EFFECT
    def play_alarm_sound_effect(self):
        # plays sound effect

        self.sound_effect = QSound(self.alarm_sound)
        self.sound_effect.play()

    def toggle_timer(self):
        # starts timer if it's not running or
        # stops timer if it is running

        if self.timer_is_running:
            self.timer_is_running = False
            self.change_timer_button_logo("start")
            self.stop_timer()
        else:
            # resume playing timer
            if self.timer_time != self.zero_time:
                self.timer_is_running = True
                self.change_timer_button_logo("pause")
                self.start_timer()

    def start_timer(self):
        # starts timer countdown

        self.timer.start(1000)

    def stop_timer(self):
        self.timer.stop()

    def update_timer(self):
        # updates timer's time every 1 second

        # decrements one second from time
        self.timer_time = self.timer_time.addSecs(-1)

        if self.timer_time == self.zero_time:
            self.stop_timer()
            self.timer_is_running = False
            self.change_timer_button_logo("start")
            self.toggle_timer_button.setDisabled(True)
            self.play_alarm_sound_effect()

        self.display_timer_time()

    def reset_timer(self):
        # changes timer countdown back to normal

        self.timer_time = self.timer_duration
        self.display_timer_time()

        if self.timer_time == self.zero_time:
            self.toggle_timer_button.setDisabled(True)
        else:
            self.toggle_timer_button.setDisabled(False)

    # WINDOW
    def create_change_time_window(self):
        # shows change time window

        self.stop_timer()

        self.hour_input = QLineEdit()
        self.hour_input.setAlignment(Qt.AlignHCenter)
        self.hour_input.setValidator(QIntValidator())
        self.hour_input.setText(self.timer_duration.toString("hh"))

        self.hour_label = QLabel("HH")

        self.minute_input = QLineEdit()
        self.minute_input.setAlignment(Qt.AlignHCenter)
        self.minute_input.setValidator(QIntValidator())
        self.minute_input.setText(self.timer_duration.toString("mm"))

        self.minute_label = QLabel("MM")

        self.second_input = QLineEdit()
        self.second_input.setAlignment(Qt.AlignHCenter)
        self.second_input.setValidator(QIntValidator())
        self.second_input.setText(self.timer_duration.toString("ss"))

        self.second_label = QLabel("SS")

        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.hour_input, 0, 0)
        self.grid_layout.addWidget(self.hour_label, 1, 0, alignment=Qt.AlignHCenter)

        self.grid_layout.addWidget(self.minute_input, 0, 1)
        self.grid_layout.addWidget(self.minute_label, 1, 1, alignment=Qt.AlignHCenter)

        self.grid_layout.addWidget(self.second_input, 0, 2)
        self.grid_layout.addWidget(self.second_label, 1, 2, alignment=Qt.AlignHCenter)

        self.set_time_button = QPushButton("Set Time")
        self.set_time_button.clicked.connect(self.check_time_input)

        self.vbox = QVBoxLayout()
        self.vbox.addStretch()
        self.vbox.addLayout(self.grid_layout)
        self.vbox.addStretch()
        self.vbox.addWidget(self.set_time_button)

        self.change_time_widget = QWidget()
        self.change_time_widget.setLayout(self.vbox)

        return self.change_time_widget

    def check_time_input(self):
        # checks if user's HH, MM, SS in Change Time Window
        # are valid inputs

        hours = self.hour_input.text()
        minutes = self.minute_input.text()
        seconds = self.second_input.text()

        if hours == "":
            hours = 0
        if minutes == "":
            minutes = 0
        if seconds == "":
            seconds = 0

        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)

        if hours >= 0 and minutes >= 0 and seconds >= 0:
            if hours < 24 and minutes < 60 and seconds < 60:
                self.timer_duration = QTime(hours, minutes, seconds)
                self.change_window(0)

                self.timer_time = self.timer_duration
                self.display_timer_time()
            else:
                # button turns red to give user feedback
                self.show_button_effect()
        else:
            self.show_button_effect()

    # EFFECT
    def show_button_effect(self):
        # changes button's color to red and returns back to normal after half a second

        self.set_time_button.setStyleSheet("background-color: red")
        QTimer.singleShot(500, self.reset_button_color)

    # EFFECT
    def reset_button_color(self):
        # resets buttons color back to light grey

        self.set_time_button.setStyleSheet("background-color: light grey")


class StopwatchWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.window_icon = "timer_assets/timer.png"
        self.play_icon = "timer_assets/play.png"
        self.pause_icon = "timer_assets/pause.png"
        self.reset_icon = "timer_assets/reset.png"

        self.stopwatch_time = QTime(0, 0, 0, 0)
        self.stopwatch_is_running = False

        self.stopwatch = QTimer()
        self.stopwatch.timeout.connect(self.update_stopwatch)

        self.init_window()

    def init_window(self):

        self.stopwatch_vbox = self.create_stopwatch_window()
        self.setLayout(self.stopwatch_vbox)

    # STOPWATCH
    def create_stopwatch_window(self):

        self.stopwatch_time_label = QLabel(self.stopwatch_time.toString("hh:mm:ss.zz"))
        self.stopwatch_time_label.setAlignment(Qt.AlignCenter)
        self.stopwatch_time_label.setFont(QFont("Arial", 20))

        self.reset_stopwatch_button = QPushButton()
        self.reset_stopwatch_button.setIcon(QIcon(self.reset_icon))
        self.reset_stopwatch_button.setFixedWidth(200)
        self.reset_stopwatch_button.clicked.connect(self.reset_stopwatch)

        self.toggle_stopwatch_button = QPushButton()
        self.toggle_stopwatch_button.setIcon(QIcon(self.play_icon))
        self.toggle_stopwatch_button.setFixedWidth(200)
        self.toggle_stopwatch_button.clicked.connect(self.toggle_stopwatch)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.stopwatch_time_label)
        self.vbox.addWidget(self.reset_stopwatch_button, alignment=Qt.AlignHCenter)
        self.vbox.addWidget(self.toggle_stopwatch_button, alignment=Qt.AlignHCenter)
        self.vbox.addSpacing(20)

        return self.vbox

    def display_stopwatch_time(self):
        # msec displays the hundreds and tens place only

        msec = str(int(self.stopwatch_time.msec() / 10))
        self.stopwatch_time_label.setText(self.stopwatch_time.toString(f"hh:mm:ss.{msec.ljust(2, '0')}"))

    def toggle_stopwatch(self):
        # starts stopwatch if it's not running or
        # stops stopwatch if it is running

        if self.stopwatch_is_running:
            self.stopwatch_is_running = False
            self.change_stopwatch_button_logo("start")
            self.stop_stopwatch()
        else:
            self.stopwatch_is_running = True
            self.change_stopwatch_button_logo("pause")
            self.start_stopwatch()

    # EFFECT
    def change_stopwatch_button_logo(self, action):
        # changes button logo

        if action == "start":
            self.toggle_stopwatch_button.setIcon(QIcon(self.play_icon))
        elif action == "pause":
            self.toggle_stopwatch_button.setIcon(QIcon(self.pause_icon))

    def start_stopwatch(self):
        # runs stopwatch

        self.stopwatch.start(10)

    def stop_stopwatch(self):
        # stops stopwatch

        self.stopwatch.stop()

    def update_stopwatch(self):
        # stopwatch's interval is every 10 ms so only the hundreds and tens digits are shown

        self.stopwatch_time = self.stopwatch_time.addMSecs(10)
        self.display_stopwatch_time()

    def reset_stopwatch(self):
        # resets stopwatch time to zero

        self.stopwatch_time = QTime(0, 0, 0, 0)
        self.display_stopwatch_time()


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.title = "Clock"
        self.window_icon = "timer_assets/timer.png"

        self.init_window()

    def init_window(self):

        self.setGeometry(100, 100, 300, 270)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(self.window_icon))

        self.create_tab_layout()

    def create_tab_layout(self):

        self.tab_widget = QTabWidget()
        self.tab_widget.setFont(QFont("Arial", 10))
        self.tab_widget.setStyleSheet("""QTabBar::tab {
            width: 150px;
            height: 30px 
        }""")

        self.timer_widget = TimerWidget()
        self.stopwatch_widget = StopwatchWidget()
        self.tab_widget.addTab(self.timer_widget, "Timer")
        self.tab_widget.addTab(self.stopwatch_widget, "Stopwatch")

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.tab_widget)
        self.vbox.setContentsMargins(0, 0, 0, 0)

        self.center_widget = QWidget()
        self.center_widget.setLayout(self.vbox)
        self.setCentralWidget(self.center_widget)


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())
