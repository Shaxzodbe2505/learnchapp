from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLCDNumber, QPushButton
from PyQt5.QtCore import QTimer

class ChronometerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.time_left = 100  # Vaqtni soniyalar bilan boshlaymiz
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # LCD formatidagi chronometer
        self.lcd = QLCDNumber(self)
        self.lcd.setDigitCount(5)  # Formati: MM:SS
        self.lcd.setStyleSheet("""
            background-color: #1e1e1e;
            color: #00ff00;
            border: 3px solid #00ff00;
            border-radius: 12px;
            padding: 5px;
            font-size: 36px;
        """)
        self.layout.addWidget(self.lcd)

        # Start tugmasi
        self.start_button = QPushButton('Start Timer', self)
        self.start_button.setStyleSheet("""
            background-color: #00ff00;
            color: black;
            border: 2px solid #00cc00;
            border-radius: 8px;
            padding: 8px;
            font-size: 18px;
            font-weight: bold;
        """)
        self.start_button.clicked.connect(self.startTimer)
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTimer)

        # Oyna dizayni
        self.setStyleSheet("""
            background-color: #2b2b2b;
            border-radius: 16px;
        """)
        self.setGeometry(300, 300, 280, 150)
        self.setWindowTitle('Chronometer Timer')

    def startTimer(self):
        self.time_left = 40
        self.updateTimer()
        self.timer.start(1000)

    def updateTimer(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.lcd.display(f"{minutes:02}:{seconds:02}")

        if self.time_left <= 10:
            # 10 soniyadan kam qolsa qizil rangga o'tadi
            self.lcd.setStyleSheet("""
                background-color: #1e1e1e;
                color: #ff0000;
                border: 3px solid #ff0000;
                border-radius: 12px;
                padding: 5px;
                font-size: 36px;
            """)
        else:
            # Oddiy holatda yashil rangda
            self.lcd.setStyleSheet("""
                background-color: #1e1e1e;
                color: #00ff00;
                border: 3px solid #00ff00;
                border-radius: 12px;
                padding: 5px;
                font-size: 36px;
            """)

        if self.time_left == 0:
            self.timer.stop()
        else:
            self.time_left -= 1

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = ChronometerApp()
    ex.show()
    sys.exit(app.exec_())
