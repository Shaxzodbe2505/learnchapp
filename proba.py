import subprocess
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QGridLayout, QMessageBox, QStackedWidget
from PyQt5.QtGui import QFont, QPalette, QBrush, QPixmap, QIcon
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect


class CourseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Muhandislik Grafikasi')
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowIcon(QIcon('images/technical-drawing.ico'))
        self.is_menu_open = False
        self.initUI()

    def initUI(self):
        # palette = QPalette()
        # palette.setBrush(QPalette.Window, QBrush(QPixmap("images/background.jpg")))
        # self.setPalette(palette)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # # Sarlavha
        # title = QLabel("Muhandislik Grafikasi Darslari")
        # title.setFont(QFont('Arial', 30, QFont.Bold))
        # title.setStyleSheet("color: #000000;")
        # title.setAlignment(Qt.AlignLeft)
        # main_layout.addWidget(title)

        # Sozlamalar tugmasi
        self.settings_button = QPushButton("⚙️")
        self.settings_button.setFont(QFont('Arial', 24))
        self.settings_button.setFixedSize(50, 50)
        self.settings_button.setStyleSheet("border: none;")
        self.settings_button.clicked.connect(self.toggleSettings)

        top_layout = QHBoxLayout()
        # top_layout.addWidget(title)
        top_layout.addStretch()
        top_layout.addWidget(self.settings_button)
        main_layout.addLayout(top_layout)

        # Sozlamalar paneli
        self.settings_panel = QFrame(self)
        self.settings_panel.setGeometry(1920, 0, 300, 400)
        self.settings_panel.setStyleSheet("background-color: rgba(0, 0, 0, 0.8); border-radius: 12px;")

        settings_layout = QVBoxLayout(self.settings_panel)
        settings_layout.setContentsMargins(20, 20, 20, 20)

        create_test_btn = QPushButton("➕ Yangi test tuzish")
        create_test_btn.setFont(QFont('Arial', 16))
        create_test_btn.setStyleSheet("color: white; background-color: #6A0DAD; padding: 10px; border-radius: 8px;")
        create_test_btn.clicked.connect(self.createTest)
        settings_layout.addWidget(create_test_btn)

        about_btn = QPushButton("ℹ️ Ilova haqida")
        about_btn.setFont(QFont('Arial', 16))
        about_btn.setStyleSheet("color: white; background-color: #6A0DAD; padding: 10px; border-radius: 8px;")
        about_btn.clicked.connect(self.showAbout)
        settings_layout.addWidget(about_btn)

        close_btn = QPushButton("❌ Yopish")
        close_btn.setFont(QFont('Arial', 16))
        close_btn.setStyleSheet("color: white; background-color: #6A0DAD; padding: 10px; border-radius: 8px;")
        close_btn.clicked.connect(self.toggleSettings)
        settings_layout.addWidget(close_btn)

        self.animation = QPropertyAnimation(self.settings_panel, b"geometry")

    def toggleSettings(self):
        if self.is_menu_open:
            self.animation.setDuration(300)
            self.animation.setStartValue(QRect(1620, 0, 300, 400))
            self.animation.setEndValue(QRect(1920, 0, 300, 400))
            self.is_menu_open = False
        else:
            self.animation.setDuration(300)
            self.animation.setStartValue(QRect(1920, 0, 300, 400))
            self.animation.setEndValue(QRect(1620, 0, 300, 400))
            self.is_menu_open = True

        self.animation.start()

    def createTest(self):
        QMessageBox.information(self, "Test", "Yangi test tuzish funksiyasi ishlab chiqilmoqda.")

    def showAbout(self):
        QMessageBox.information(self, "Ilova haqida", "Bu dastur Muhandislik Grafikasi uchun darslarni o'rganish uchun ishlatiladi.")


def main():
    app = QApplication(sys.argv)
    window = CourseApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
