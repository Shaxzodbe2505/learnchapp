import json
import os
import requests
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QMessageBox, QLineEdit,
    QHBoxLayout, QFormLayout, QRadioButton, QButtonGroup, QStackedWidget, QApplication,
    QFileDialog, QDialog, QInputDialog
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont, QPainter

class DrawingEditor(QDialog):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chizma Nuqtalarini Tanlash")
        self.image_path = image_path
        self.points = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.image_label = QLabel(self)
        pixmap = QPixmap(self.image_path)
        if pixmap.isNull():
            pixmap = QPixmap(600, 400)
            pixmap.fill(Qt.white)
            painter = QPainter(pixmap)
            painter.setFont(QFont("Arial", 20))
            painter.drawText(pixmap.rect(), Qt.AlignCenter, "Rasm topilmadi")
            painter.end()
        self.image_label.setPixmap(pixmap.scaled(600, 400, Qt.KeepAspectRatio))
        self.image_label.mousePressEvent = self.add_point
        layout.addWidget(self.image_label)

        self.save_button = QPushButton("Saqlash")
        self.save_button.setStyleSheet("""
            QPushButton { background-color: #28a745; color: white; border-radius: 10px; padding: 10px; font-size: 16px; }
            QPushButton:hover { background-color: #218838; }
        """)
        self.save_button.clicked.connect(self.accept)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def add_point(self, event):
        x, y = event.pos().x(), event.pos().y()
        name, ok1 = QInputDialog.getText(self, "Qism nomi", "Qism nomini kiriting:")
        if not ok1 or not name:
            return
        origin, ok2 = QInputDialog.getText(self, "Kelib chiqishi", "Kelib chiqishini kiriting:")
        if not ok2 or not origin:
            return

        self.points.append((x, y, name, origin))
        self.update_image()

    def update_image(self):
        pixmap = QPixmap(self.image_path).scaled(600, 400, Qt.KeepAspectRatio)
        painter = QPainter(pixmap)
        painter.setPen(Qt.red)
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        for i, (x, y, _, _) in enumerate(self.points, 1):
            painter.drawEllipse(x-10, y-10, 20, 20)
            painter.drawText(x-5, y+5, str(i))
        painter.end()
        self.image_label.setPixmap(pixmap)

class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Panel")
        self.setGeometry(600, 300, 900, 600)
        self.setStyleSheet("background-color: #f5f5f5; border-radius: 20px;")
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_students)
        self.timer.start(5000)

        main_layout = QHBoxLayout()

        # Talabalar Ro'yxati Bo'limi
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignTop)
        title = QLabel("Talabalar Ro'yxati")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("color: #007BFF;")
        left_layout.addWidget(title)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Qidiruv...")
        self.search_input.setStyleSheet(self.input_style())
        self.search_input.textChanged.connect(self.filter_students)
        left_layout.addWidget(self.search_input)

        self.students_list = QListWidget()
        self.students_list.setStyleSheet(self.list_style())
        left_layout.addWidget(self.students_list)

        main_layout.addLayout(left_layout)

        # O'ng panel: Test Tuzish, Video Qo'llanmalar va Tuzilish va Kompozitsiya
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignTop)

        toggle_layout = QHBoxLayout()
        self.test_toggle_btn = QPushButton("Test Tuzish")
        self.test_toggle_btn.setStyleSheet(self.button_style())
        self.test_toggle_btn.clicked.connect(self.show_test_panel)
        toggle_layout.addWidget(self.test_toggle_btn)

        self.video_toggle_btn = QPushButton("Video Qo'llanmalar")
        self.video_toggle_btn.setStyleSheet(self.button_style())
        self.video_toggle_btn.clicked.connect(self.show_video_panel)
        toggle_layout.addWidget(self.video_toggle_btn)

        self.structure_toggle_btn = QPushButton("Tuzilish va Kompozitsiya")
        self.structure_toggle_btn.setStyleSheet(self.button_style())
        self.structure_toggle_btn.clicked.connect(self.show_structure_panel)
        toggle_layout.addWidget(self.structure_toggle_btn)

        right_layout.addLayout(toggle_layout)

        self.stacked_widget = QStackedWidget()
        self.test_panel = self.create_test_panel()
        self.video_panel = self.create_video_panel()
        self.structure_panel = self.create_structure_panel()
        self.stacked_widget.addWidget(self.test_panel)
        self.stacked_widget.addWidget(self.video_panel)
        self.stacked_widget.addWidget(self.structure_panel)
        right_layout.addWidget(self.stacked_widget)

        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

        self.students = []
        self.load_students()

    def input_style(self):
        return ("QLineEdit { background-color: white; border: 1px solid #ccc; border-radius: 10px; "
                "padding: 8px; font-size: 14px; color: #000; }")

    def button_style(self):
        return ("QPushButton { background-color: #28a745; color: white; border-radius: 10px; "
                "padding: 10px; font-size: 16px; font-weight: bold; } "
                "QPushButton:hover { background-color: #218838; }")

    def list_style(self):
        return ("QListWidget { background-color: white; border: 1px solid #ccc; border-radius: 10px; "
                "padding: 8px; font-size: 14px; }")

    def load_students(self):
        try:
            response = requests.get("http://127.0.0.1:5000/register")
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
            self.students_list.addItem(f"{student['first_name']} {student['last_name']} - "
                                       f"{student['direction']} ({student['group']})")

    def filter_students(self):
        search_text = self.search_input.text().strip().lower()
        self.students_list.clear()
        for student in self.students:
            student_text = f"{student['first_name']} {student['last_name']} - " \
                           f"{student['direction']} ({student['group']})".lower()
            if search_text in student_text:
                self.students_list.addItem(student_text)

    # Test Panel
    def create_test_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)

        test_title = QLabel("Test Tuzish")
        test_title.setFont(QFont("Arial", 18, QFont.Bold))
        test_title.setStyleSheet("color: #FF5733;")
        layout.addWidget(test_title)

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
        layout.addLayout(form_layout)

        self.add_test_button = QPushButton("Testni qo'shish")
        self.add_test_button.setStyleSheet(self.button_style())
        self.add_test_button.clicked.connect(self.add_test)
        layout.addWidget(self.add_test_button)

        self.delete_test_button = QPushButton("Avvalgi Testlarni O'chirish")
        self.delete_test_button.setStyleSheet(self.button_style())
        self.delete_test_button.clicked.connect(self.delete_tests)
        layout.addWidget(self.delete_test_button)

        return panel

    # Video Panel
    def create_video_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)

        video_title = QLabel("Video Qo'llanmalar")
        video_title.setFont(QFont("Arial", 18, QFont.Bold))
        video_title.setStyleSheet("color: #007BFF;")
        layout.addWidget(video_title)

        form_layout = QFormLayout()
        self.video_link_input = QLineEdit()
        self.video_link_input.setPlaceholderText("Video linkini kiriting")
        self.video_link_input.setStyleSheet(self.input_style())
        form_layout.addRow("Link:", self.video_link_input)

        self.video_subject_input = QLineEdit()
        self.video_subject_input.setPlaceholderText("Video mavzusini kiriting")
        self.video_subject_input.setStyleSheet(self.input_style())
        form_layout.addRow("Mavzu:", self.video_subject_input)

        layout.addLayout(form_layout)

        self.add_video_button = QPushButton("Videoni qo'shish")
        self.add_video_button.setStyleSheet(self.button_style())
        self.add_video_button.clicked.connect(self.add_video)
        layout.addWidget(self.add_video_button)

        self.video_search_input = QLineEdit()
        self.video_search_input.setPlaceholderText("Videolarni qidirish...")
        self.video_search_input.setStyleSheet(self.input_style())
        self.video_search_input.textChanged.connect(self.filter_videos)
        layout.addWidget(self.video_search_input)

        self.video_label = QLabel("Qo'shilgan videolar:")
        self.video_label.setFont(QFont("Arial", 14))
        layout.addWidget(self.video_label)
        self.video_list = QListWidget()
        self.video_list.setStyleSheet(self.list_style())
        layout.addWidget(self.video_list)

        self.delete_selected_video_button = QPushButton("Tanlangan videoni o'chirish")
        self.delete_selected_video_button.setStyleSheet(self.button_style())
        self.delete_selected_video_button.clicked.connect(self.delete_selected_video)
        layout.addWidget(self.delete_selected_video_button)

        self.delete_video_button = QPushButton("Barcha videolarni o'chirish")
        self.delete_video_button.setStyleSheet(self.button_style())
        self.delete_video_button.clicked.connect(self.delete_videos)
        layout.addWidget(self.delete_video_button)

        self.update_video_list()
        return panel

    # Tuzilish va Kompozitsiya Panel
    def create_structure_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)

        structure_title = QLabel("Tuzilish va Kompozitsiya")
        structure_title.setFont(QFont("Arial", 18, QFont.Bold))
        structure_title.setStyleSheet("color: #28a745;")
        layout.addWidget(structure_title)

        form_layout = QFormLayout()
        self.drawing_name_input = QLineEdit()
        self.drawing_name_input.setPlaceholderText("Chizma nomini kiriting")
        self.drawing_name_input.setStyleSheet(self.input_style())
        form_layout.addRow("Chizma nomi:", self.drawing_name_input)

        self.drawing_file_button = QPushButton("Chizma faylini tanlash")
        self.drawing_file_button.setStyleSheet(self.button_style())
        self.drawing_file_button.clicked.connect(self.select_drawing_file)
        form_layout.addRow("Fayl:", self.drawing_file_button)

        layout.addLayout(form_layout)

        self.add_drawing_button = QPushButton("Chizmani qo'shish va nuqtalarni tanlash")
        self.add_drawing_button.setStyleSheet(self.button_style())
        self.add_drawing_button.clicked.connect(self.add_drawing)
        layout.addWidget(self.add_drawing_button)

        self.drawing_list = QListWidget()
        self.drawing_list.setStyleSheet(self.list_style())
        layout.addWidget(self.drawing_list)

        self.delete_drawing_button = QPushButton("Tanlangan chizmani o'chirish")
        self.delete_drawing_button.setStyleSheet(self.button_style())
        self.delete_drawing_button.clicked.connect(self.delete_drawing)
        layout.addWidget(self.delete_drawing_button)

        self.update_drawing_list()
        return panel

    def show_test_panel(self):
        self.stacked_widget.setCurrentWidget(self.test_panel)

    def show_video_panel(self):
        self.stacked_widget.setCurrentWidget(self.video_panel)
        self.update_video_list()

    def show_structure_panel(self):
        self.stacked_widget.setCurrentWidget(self.structure_panel)
        self.update_drawing_list()

    def add_test(self):
        question = self.question_input.text().strip()
        options = [opt.text().strip() for opt in self.option_inputs]
        correct_index = self.correct_option.checkedId()

        if not question or any(opt == "" for opt in options) or correct_index == -1:
            QMessageBox.warning(self, "Xatolik", "Barcha maydonlarni to'ldiring va to'g'ri javobni belgilang!")
            return

        test = {"question": question, "options": options, "correct": correct_index}
        with open("test.json", "a", encoding="utf-8") as file:
            json.dump(test, file, ensure_ascii=False)
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

    def add_video(self):
        video_link = self.video_link_input.text().strip()
        video_subject = self.video_subject_input.text().strip()

        if not video_link or not video_subject:
            QMessageBox.warning(self, "Xatolik", "Iltimos, video linki va mavzusini kiriting!")
            return

        video = {"link": video_link, "subject": video_subject}
        with open("videos.json", "a", encoding="utf-8") as file:
            json.dump(video, file, ensure_ascii=False)
            file.write("\n")

        QMessageBox.information(self, "Muvaffaqiyatli", "Video qo'shildi!")
        self.video_link_input.clear()
        self.video_subject_input.clear()
        self.update_video_list()

    def delete_videos(self):
        if os.path.exists("videos.json"):
            os.remove("videos.json")
            QMessageBox.information(self, "O'chirildi", "Barcha videolar muvaffaqiyatli o'chirildi!")
            self.update_video_list()

    def update_video_list(self):
        self.video_list.clear()
        self.videos = []
        if os.path.exists("videos.json"):
            try:
                with open("videos.json", "r", encoding="utf-8") as file:
                    for line in file:
                        if line.strip():
                            video = json.loads(line)
                            self.videos.append(video)
                            self.video_list.addItem(f"{video['subject']} - {video['link']}")
            except Exception as e:
                print(f"Xatolik yuz berdi: {e}")
        if not self.videos:
            self.video_list.addItem("Videolar mavjud emas")

    def filter_videos(self):
        search_text = self.video_search_input.text().strip().lower()
        self.video_list.clear()
        for video in self.videos:
            video_text = f"{video['subject']} - {video['link']}".lower()
            if search_text in video_text:
                self.video_list.addItem(f"{video['subject']} - {video['link']}")
        if self.video_list.count() == 0:
            self.video_list.addItem("Hech narsa topilmadi")

    def delete_selected_video(self):
        selected_item = self.video_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Xatolik", "Iltimos, o'chirish uchun videoni tanlang!")
            return

        selected_text = selected_item.text()
        selected_subject = selected_text.split(" - ")[0]
        selected_link = selected_text.split(" - ")[1]

        if os.path.exists("videos.json"):
            temp_videos = []
            with open("videos.json", "r", encoding="utf-8") as file:
                for line in file:
                    if line.strip():
                        video = json.loads(line)
                        if video["subject"] != selected_subject or video["link"] != selected_link:
                            temp_videos.append(video)

            with open("videos.json", "w", encoding="utf-8") as file:
                for video in temp_videos:
                    json.dump(video, file, ensure_ascii=False)
                    file.write("\n")

            QMessageBox.information(self, "O'chirildi", "Tanlangan video muvaffaqiyatli o'chirildi!")
            self.update_video_list()

    def select_drawing_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Chizma faylini tanlash", "", "Images (*.png *.jpg *.jpeg)")
        if file_name:
            self.drawing_file_button.setText(f"Tanlandi: {os.path.basename(file_name)}")
            self.selected_drawing_file = file_name

    def add_drawing(self):
        drawing_name = self.drawing_name_input.text().strip()
        if not drawing_name or not hasattr(self, 'selected_drawing_file'):
            QMessageBox.warning(self, "Xatolik", "Chizma nomi va faylni tanlang!")
            return

        # Chizma muharririni ochish
        editor = DrawingEditor(self.selected_drawing_file, self)
        if editor.exec_():
            points = editor.points
            drawing = {
                "name": drawing_name,
                "image_path": self.selected_drawing_file,
                "points": points
            }

            with open("drawings.json", "a", encoding="utf-8") as file:
                json.dump(drawing, file, ensure_ascii=False)
                file.write("\n")

            QMessageBox.information(self, "Muvaffaqiyatli", "Chizma va nuqtalar qo'shildi!")
            self.drawing_name_input.clear()
            self.drawing_file_button.setText("Chizma faylini tanlash")
            del self.selected_drawing_file
            self.update_drawing_list()

    def update_drawing_list(self):
        self.drawing_list.clear()
        if os.path.exists("drawings.json"):
            try:
                with open("drawings.json", "r", encoding="utf-8") as file:
                    for line in file:
                        if line.strip():
                            drawing = json.loads(line)
                            self.drawing_list.addItem(f"{drawing['name']} - {drawing['image_path']}")
            except Exception as e:
                print(f"Xatolik yuz berdi: {e}")

    def delete_drawing(self):
        selected_item = self.drawing_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Xatolik", "Iltimos, o'chirish uchun chizmani tanlang!")
            return

        selected_text = selected_item.text()
        selected_name = selected_text.split(" - ")[0]
        selected_path = selected_text.split(" - ")[1]

        if os.path.exists("drawings.json"):
            temp_drawings = []
            with open("drawings.json", "r", encoding="utf-8") as file:
                for line in file:
                    if line.strip():
                        drawing = json.loads(line)
                        if drawing["name"] != selected_name or drawing["image_path"] != selected_path:
                            temp_drawings.append(drawing)

            with open("drawings.json", "w", encoding="utf-8") as file:
                for drawing in temp_drawings:
                    json.dump(drawing, file, ensure_ascii=False)
                    file.write("\n")

            QMessageBox.information(self, "O'chirildi", "Tanlangan chizma muvaffaqiyatli o'chirildi!")
            self.update_drawing_list()

if __name__ == "__main__":
    app = QApplication([])
    panel = AdminPanel()
    panel.show()
    app.exec_()