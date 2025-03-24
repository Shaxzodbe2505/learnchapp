import json
import os

import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QMessageBox, QLineEdit, QHBoxLayout, QFormLayout, QRadioButton, QButtonGroup
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont


class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Panel")
        self.setGeometry(600, 300, 800, 600)
        self.setStyleSheet("background-color: #f5f5f5; border-radius: 20px;")
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_students)
        self.timer.start(5000)  # Har 5 soniyada yangilaydi
        main_layout = QHBoxLayout()


        # *** Talabalar Ro'yxati Bo'limi ***
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignTop)

        title = QLabel("Talabalar Ro'yxati")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("color: #007BFF;")
        left_layout.addWidget(title)

        # Qidiruv maydoni
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Qidiruv...")
        self.search_input.setStyleSheet(self.input_style())
        self.search_input.textChanged.connect(self.filter_students)
        left_layout.addWidget(self.search_input)

        self.students_list = QListWidget()
        self.students_list.setStyleSheet(self.list_style())
        left_layout.addWidget(self.students_list)

        main_layout.addLayout(left_layout)

        # *** Test Tuzish Bo'limi ***
        right_layout = QVBoxLayout()

        test_title = QLabel("Test Tuzish")
        test_title.setFont(QFont("Arial", 18, QFont.Bold))
        test_title.setStyleSheet("color: #FF5733;")
        right_layout.addWidget(test_title)

        form_layout = QFormLayout()

        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("Savolni kiriting")
        self.question_input.setStyleSheet(self.input_style())
        form_layout.addRow("Savol:", self.question_input)

        self.option_inputs = []
        self.correct_option = QButtonGroup()

        for i in ['A', 'B', 'C', 'D']:
            option_input = QLineEdit()
            option_input.setPlaceholderText(f"Variant {i}")
            option_input.setStyleSheet(self.input_style())
            self.option_inputs.append(option_input)

            radio_button = QRadioButton()
            self.correct_option.addButton(radio_button)

            h_layout = QHBoxLayout()
            h_layout.addWidget(option_input)
            h_layout.addWidget(radio_button)
            form_layout.addRow(f"{i}:", h_layout)

        right_layout.addLayout(form_layout)

        self.add_test_button = QPushButton("Testni qo'shish")
        self.add_test_button.setStyleSheet(self.button_style())
        self.add_test_button.clicked.connect(self.add_test)
        right_layout.addWidget(self.add_test_button)

        self.delete_test_button = QPushButton("Avvalgi Testlarni O'chirish")
        self.delete_test_button.setStyleSheet(self.button_style())
        self.delete_test_button.clicked.connect(self.delete_tests)
        right_layout.addWidget(self.delete_test_button)

        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

        self.students = []  # Talabalar ro'yxati
        self.load_students()

    def input_style(self):
        return "QLineEdit { background-color: white; border: 1px solid #ccc; border-radius: 10px; padding: 8px; font-size: 14px; color: #000; }"

    def button_style(self):
        return "QPushButton { background-color: #28a745; color: white; border-radius: 10px; padding: 10px; font-size: 16px; font-weight: bold; } QPushButton:hover { background-color: #218838; }"

    def list_style(self):
        return "QListWidget { background-color: white; border: 1px solid #ccc; border-radius: 10px; padding: 8px; font-size: 14px; }"

    def load_students(self):
        try:
            response = requests.get("http://127.0.0.1:5000/students")
            if response.status_code == 200:
                self.students = response.json()
                self.display_students()
            else:
                print("Xatolik yuz berdi:", response.json())
        except Exception as e:
            print("Server bilan bog‘lanishda xatolik:", e)

    def display_students(self):
        self.students_list.clear()
        for student in self.students:
            self.students_list.addItem(f"{student['first_name']} {student['last_name']} - {student['direction']} ({student['group']})")

    def filter_students(self):
        search_text = self.search_input.text().strip().lower()
        self.students_list.clear()
        for student in self.students:
            student_text = f"{student['first_name']} {student['last_name']} - {student['direction']} ({student['group']})".lower()
            if search_text in student_text:
                self.students_list.addItem(student_text)

    def add_test(self):
        question = self.question_input.text().strip()
        options = [opt.text().strip() for opt in self.option_inputs]
        correct_index = self.correct_option.checkedId()

        if not question or any(opt == "" for opt in options) or correct_index == -1:
            QMessageBox.warning(self, "Xatolik", "Barcha maydonlarni to'ldiring va to'g'ri javobni belgilang!")
            return

        test = {
            "question": question,
            "options": options,
            "correct": correct_index
        }

        with open("test.json", "a") as file:
            json.dump(test, file)
            file.write("\n")

        QMessageBox.information(self, "Muvaffaqiyatli", "Test muvaffaqiyatli qo'shildi!")

        self.clear_test_inputs()

    def delete_tests(self):
        if os.path.exists("test.json"):
            os.remove("test.json")
            QMessageBox.information(self, "O'chirildi", "Barcha testlar muvaffaqiyatli o'chirildi!")

    def clear_test_inputs(self):
        self.question_input.clear()
        for option in self.option_inputs:
            option.clear()
        self.correct_option.setExclusive(False)
        for btn in self.correct_option.buttons():
            btn.setChecked(False)
        self.correct_option.setExclusive(True)

if __name__ == "__main__":
    pass