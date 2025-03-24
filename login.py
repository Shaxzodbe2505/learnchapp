import sys
import json

import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from admin_panel import AdminPanel

class LoginWindow(QWidget):
    def __init__(self, on_success=None):
        super().__init__()
        self.setWindowTitle("Kirish")
        self.setGeometry(800, 300, 600, 400)
        self.setStyleSheet("background-color: #f5f5f5; border-radius: 20px;")
        self.setWindowIcon(QIcon('images/login-square-arrow-button-outline_icon-icons.com_73220 (1).ico'))
        self.on_success = on_success

        main_layout = QHBoxLayout()

        # Chap qism (foydalanuvchi ma'lumotlari)
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Kirish")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #007BFF;")
        left_layout.addWidget(title)

        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("Ism")
        self.first_name.setStyleSheet(self.input_style())
        left_layout.addWidget(self.first_name)

        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText("Familiya")
        self.last_name.setStyleSheet(self.input_style())
        left_layout.addWidget(self.last_name)

        self.direction = QLineEdit()
        self.direction.setPlaceholderText("Yo'nalish")
        self.direction.setStyleSheet(self.input_style())
        left_layout.addWidget(self.direction)

        self.group = QLineEdit()
        self.group.setPlaceholderText("Guruh")
        self.group.setStyleSheet(self.input_style())
        left_layout.addWidget(self.group)

        # Ma'lumotlarni yuklash 🔥
        self.load_student_data()

        self.login_button = QPushButton("Davom etish")
        self.login_button.setStyleSheet(self.button_style())
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.clicked.connect(self.login)
        left_layout.addWidget(self.login_button)

        # O'ng qism (admin panel login)
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignCenter)

        admin_title = QLabel("Admin panel")
        admin_title.setFont(QFont("Arial", 18, QFont.Bold))
        admin_title.setStyleSheet("color: #FF4500;")
        right_layout.addWidget(admin_title)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Login")
        self.username.setStyleSheet(self.input_style())
        right_layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Parol")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet(self.input_style())
        right_layout.addWidget(self.password)

        self.admin_button = QPushButton("Admin panelga o'tish")
        self.admin_button.setStyleSheet(self.button_style())
        self.admin_button.setCursor(Qt.PointingHandCursor)
        self.admin_button.clicked.connect(self.check_login)
        right_layout.addWidget(self.admin_button)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def input_style(self):
        return (
            "QLineEdit {"
            "background-color: white;"
            "border: 1px solid #ccc;"
            "border-radius: 10px;"
            "padding: 12px;"
            "font-size: 16px;"
            "color: #000;"
            "}"
        )

    def button_style(self):
        return (
            "QPushButton {"
            "background-color: #007BFF;"
            "color: white;"
            "border-radius: 10px;"
            "padding: 12px;"
            "font-size: 18px;"
            "font-weight: bold;"
            "}"
            "QPushButton:hover {"
            "background-color: #0056b3;"
            "}"
        )

    def login(self):
        first_name = self.first_name.text().strip()
        last_name = self.last_name.text().strip()
        direction = self.direction.text().strip()
        group = self.group.text().strip()

        if not (first_name and last_name and direction and group):
            QMessageBox.warning(self, "Xatolik", "Iltimos, barcha maydonlarni to'ldiring!")
            return

        self.save_student_data(first_name, last_name, direction, group)
        QMessageBox.information(self, "Xush kelibsiz", f"Xush kelibsiz, {first_name} {last_name}!")
        self.close()

        if self.on_success:
            self.on_success()

    def save_student_data(self, first_name, last_name, direction, group):
        new_data = {
            "first_name": first_name,
            "last_name": last_name,
            "direction": direction,
            "group": group
        }

        try:
            # ✅ Ma'lumotni serverga yuborish
            response = requests.post("http://127.0.0.1:5000/register", json=new_data)
            if response.status_code == 201:
                print("Ma'lumot serverga saqlandi!")
            else:
                print("Xatolik yuz berdi:", response.json())
        except Exception as e:
            print("Server bilan bog‘lanishda xatolik:", e)

    def load_student_data(self):
        try:
            with open("data.json", "r") as file:
                students = json.load(file)
                if isinstance(students, list) and students:
                    data = students[-1]  # Oxirgi yozuvni olish
                    self.first_name.setText(data.get("first_name", ""))
                    self.last_name.setText(data.get("last_name", ""))
                    self.direction.setText(data.get("direction", ""))
                    self.group.setText(data.get("group", ""))
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def check_login(self):
        username = self.username.text().strip()
        password = self.password.text().strip()

        if username == "admin" and password == "124578":
            QMessageBox.information(self, "Muvaffaqiyatli", "Admin paneliga xush kelibsiz!")
            self.open_admin_panel()
        else:
            QMessageBox.critical(self, "Xatolik", "Login yoki parol xato!")

    def open_admin_panel(self):
        self.close()  # Oynani yopish
        self.admin_panel = AdminPanel()
        self.admin_panel.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    def show_main_window():
        from main import CourseApp
        main_window = CourseApp()
        main_window.show()

    login_window = LoginWindow(on_success=show_main_window)
    login_window.show()

    sys.exit(app.exec_())