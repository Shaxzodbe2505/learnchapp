import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QGridLayout, \
    QSpacerItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy


class TestApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Test Window')
        self.setGeometry(0, 0, 1920, 1080)
        self.setStyleSheet("background-color: #80bfff; color: #ffffff;")

        self.initData()
        self.initUI()

    def initData(self):
        # Savollar va javoblar
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

    def initUI(self):
        layout = QVBoxLayout()



        # Savol maydoni
        self.question_label = QLabel("")
        self.question_label.setFont(QFont('Arial', 30))
        self.question_label.setStyleSheet("color: #ffffff;")
        self.question_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.question_label)
        layout.addSpacing(600)  # Savoldan keyin biroz bo'sh joy qoldirish

        # Javob tugmalari (2 ta qator, 2 ta ustun)
        self.grid_layout = QGridLayout()
        button_layout = QVBoxLayout()
        self.answer_buttons = []
        for i in range(4):
            button = QPushButton("")
            button.setFont(QFont('Arial', 20))
            button.setMaximumWidth(700)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #6a0dad;
                    color: #ffffff;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #7b1fa2;
                }
            """)
            button.clicked.connect(lambda checked, i=i: self.checkAnswer(i))
            self.answer_buttons.append(button)

            # 2 ta qator, 2 ta ustunda joylashtirish
            self.grid_layout.addWidget(button, i // 2, i % 2)

        layout.addLayout(self.grid_layout)
        self.setLayout(layout)
        self.loadQuestion()
        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.loadQuestion()

    def loadQuestion(self):
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            self.question_label.setText(f"{self.current_question + 1}. {question_data['question']}")

            answers = list(question_data["answers"].items())
            for i in range(4):
                self.answer_buttons[i].setText(f"{answers[i][0]}. {answers[i][1]}")
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
            QMessageBox.warning(self, "Natija", f"❌ Noto‘g‘ri javob. To‘g‘ri javob: {question_data['correct']}")

        # Keyingi savolga o‘tish
        self.current_question += 1
        self.loadQuestion()

    def showResult(self):
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

