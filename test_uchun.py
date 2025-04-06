import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QGridLayout, \
    QSpacerItem, QGraphicsDropShadowEffect, QFrame
from PyQt5.QtGui import QFont, QPalette, QBrush, QPixmap, QColor
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QSizePolicy


class TestApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Test Window')
        self.setGeometry(0, 0, 1920, 1080)
        # self.setStyleSheet("background-color: #80bfff; color: #ffffff;")

        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap("images/vivid-blurred-colorful-wallpaper-background.jpg")))
        self.setPalette(palette)



        self.initData()
        self.initUI()

    def initData(self):
        self.questions = [
            {"question": "Chizma tuzishda asosiy proyeksiya usullari qaysilar?",
             "answers": {"A": "Frontal va gorizontal", "B": "Diogonal va parallel", "C": "Markaziy va yon",
                         "D": "Vertikal va yon"},
             "correct": "A"},

            {"question": "Qaysi chizma turi uch o‘lchamli tasvirni ifodalaydi?",
             "answers": {"A": "Proyeksiya chizmasi", "B": "Aksometrik chizma", "C": "Tekislik chizmasi",
                         "D": "Kontur chizmasi"},
             "correct": "B"},

            {"question": "Chizma elementlarida chiziqlar qalinligi qanday belgilangan?",
             "answers": {"A": "4 xil", "B": "3 xil", "C": "2 xil", "D": "5 xil"},
             "correct": "B"},

            {"question": "Ko'ndalang kesim chizmasi nima uchun ishlatiladi?",
             "answers": {"A": "Buyum shaklini to'liq ko'rsatish uchun", "B": "Buyum ichki tuzilishini ko'rsatish uchun",
                         "C": "Buyum tashqi ko'rinishini ko'rsatish uchun", "D": "Buyum o'lchamlarini belgilash uchun"},
             "correct": "B"},

            {"question": "Izometrik proyeksiya chizmasida burchak qancha bo‘ladi?",
             "answers": {"A": "30°", "B": "45°", "C": "60°", "D": "90°"},
             "correct": "A"},

            {"question": "Chizma chizishda qaysi ranglar o‘lcham chiziqlar uchun ishlatiladi?",
             "answers": {"A": "Qora", "B": "Qizil", "C": "Ko‘k", "D": "Yashil"},
             "correct": "A"},

            {"question": "Masshtab 1:2 nimani bildiradi?",
             "answers": {"A": "Chizma hajmi aslidan 2 marta kichik", "B": "Chizma hajmi aslidan 2 marta katta",
                         "C": "Chizma hajmi aslidan 2 marta qisqa", "D": "Chizma hajmi aslidan 2 marta uzun"},
             "correct": "A"},

            {"question": "Biriktirilgan o‘lcham chizig‘idagi uchburchak belgi nimani bildiradi?",
             "answers": {"A": "Ko'ndalang chiziq", "B": "Diametr", "C": "Radius", "D": "Burchak"},
             "correct": "C"},

            {"question": "Kesim chizmasida ichki tuzilish qanday chiziq bilan ko‘rsatiladi?",
             "answers": {"A": "Uzlukli chiziq", "B": "To‘liq chiziq", "C": "Nuqtali chiziq", "D": "Qalin chiziq"},
             "correct": "A"},

            {"question": "Proyeksiya chizmasida ko'ndalang chiziqlar qanday maqsadda ishlatiladi?",
             "answers": {"A": "Buyum tashqi qirralarini ko‘rsatish uchun", "B": "Ichki tuzilishini ko‘rsatish uchun",
                         "C": "O‘lcham belgilash uchun", "D": "Ko'ndalang burchaklarni belgilash uchun"},
             "correct": "C"}
        ]

        self.current_question = 0
        self.correct_answers = 0
        self.wrong_answers = 0
        self.time_left = 100

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTimer)

    def initUI(self):
        layout = QVBoxLayout()
        layout.addSpacing(100)  # Savoldan keyin biroz bo'sh joy qoldirish
        # Taymerni ko'rsatish qismi
        self.timer_label = QLabel(f"Qolgan vaqt: {self.time_left} soniya")
        self.timer_label.setFont(QFont('Arial', 20))
        self.timer_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.timer_label)
        layout.addSpacing(200)  # Savoldan keyin biroz bo'sh joy qoldirish

        # Savol maydoni uchun frame
        self.question_frame = QFrame()
        self.question_frame.setStyleSheet("""
            background-color: rgba(255, 255, 255, 150); /* Shaffof oq rang */
            border-radius: 15px;
            padding: 10px;
        """)

        # Shaffoflik va soya effekti
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)  # Soya tarqalish darajasi
        shadow.setColor(QColor(0, 0, 0, 100))  # Soya rangi (qora, shaffof)
        shadow.setOffset(5, 5)  # Soyaning yo'nalishi
        self.question_frame.setGraphicsEffect(shadow)

        # Layoutni yaratish
        question_layout = QVBoxLayout()

        # Savolni chiqarish
        self.question_label = QLabel(
            "Bu savol matni juda uzun bo'lishi mumkin, shuning uchun avtomatik o'lchamda chiqadi.")
        self.question_label.setFont(QFont('Arial', 24))
        self.question_label.setStyleSheet("color: #000000;")  # Matn rangi qora
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setWordWrap(True)  # Matnni keyingi qatorga tushirish

        # Labelni frame ichiga joylashtirish
        question_layout.addWidget(self.question_label)
        self.question_frame.setLayout(question_layout)

        # Asosiy layoutga qo'shish
        layout.addWidget(self.question_frame)
        layout.addSpacing(100)  # Savoldan keyin biroz bo'sh joy qoldirish

        # Javob tugmalari
        self.grid_layout = QGridLayout()
        self.answer_buttons = []
        for i in range(4):
            button = QPushButton("")
            button.setFont(QFont('Arial', 20))
            button.setMaximumWidth(700)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #ff3300;
                    color: #ffffff;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color:  #00e600;
                }
            """)
            button.clicked.connect(lambda checked, i=i: self.checkAnswer(i))
            self.answer_buttons.append(button)
            self.grid_layout.addWidget(button, i // 2, i % 2)

        layout.addLayout(self.grid_layout)

        # Bo'sh joy qo'shish
        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(layout)

        self.loadQuestion()
        self.startTimer()

    def startTimer(self):
        self.time_left = 60
        self.timer.start(1000)  # Har 1 sekundda yangilash
        self.updateTimer()  # Boshlanganda vaqtni darhol yangilash

    def updateTimer(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.timer_label.setText(f"Qolgan vaqt: {minutes:02}:{seconds:02}")

        if self.time_left == 0:
            self.timer.stop()
            self.timer_label.setStyleSheet("color: red; font-weight: bold;")
            self.timer_label.setText("Vaqt tugadi!")
            self.showResult()
        else:
            self.time_left -= 1

    def loadQuestion(self):
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            self.question_label.setText(f"{self.current_question + 1}. {question_data['question']}")

            answers = list(question_data["answers"].items())
            for i in range(4):
                self.answer_buttons[i].setText(f"{answers[i][0]}) {answers[i][1]}")
                self.answer_buttons[i].setEnabled(True)
        else:
            self.showResult()

    def checkAnswer(self, selected_index):
        question_data = self.questions[self.current_question]
        answers = list(question_data["answers"].keys())

        selected_answer = answers[selected_index]
        if selected_answer == question_data["correct"]:
            self.correct_answers += 1
            QMessageBox.information(self, "Natija", "✅ To‘g‘ri javob!")
        else:
            self.wrong_answers += 1
            QMessageBox.warning(self, "Natija",
                                f"❌ Noto‘g‘ri javob. To‘g‘ri javob: {question_data['correct']}")

        # Keyingi savolga o'tish
        self.current_question += 1
        self.loadQuestion()

    def showResult(self):
        self.timer.stop()  # Taymerni to'xtatish
        msg = QMessageBox(self)
        msg.setWindowTitle("Test yakuni")
        msg.setText(f"✅ To‘g‘ri javoblar: {self.correct_answers}\n❌ Noto‘g‘ri javoblar: {self.wrong_answers}")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setStyleSheet("color: #ffffff; background-color: #333333;")
        msg.exec_()
        self.close()


def main():
    app = QApplication(sys.argv)
    window = TestApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
