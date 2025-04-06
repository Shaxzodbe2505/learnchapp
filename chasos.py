from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt, QTimer
import sys


class ChizmachilikAsoslari(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chizmachilik Asoslari")
        self.setGeometry(100, 100, 900, 600)

        # Orqa fon rasmi
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("images/introbg.jpg")))  # Rasmingni shu joyga yukla
        self.setPalette(palette)

        # **Sarlavha**
        title = QLabel("Chizmachilik Asoslari", self)
        title.setFont(QFont("Times", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        # **Mavzular (bosilganda yangi sahifa ochiladi)**
        topics = [
            "1. Chizmachilikka kirish",
            "2. Chizma geometrik asoslari",
            "3. Proyeksiya usullari",
            "4. Kesim va qirqimlar",
            "5. Aksonometrik proyeksiya"
        ]

        self.topic_buttons = []
        topic_layout = QVBoxLayout()

        for topic in topics:
            btn = QPushButton(topic)
            btn.setFont(QFont("Times", 14))
            btn.setStyleSheet("background-color: #ffffff; color: #000066; border: 2px solid #000066; padding: 5px;")
            btn.clicked.connect(self.open_topic)
            self.topic_buttons.append(btn)
            topic_layout.addWidget(btn)

        # **O'ng tarafdagi rasm slayd-shousi**
        self.image_label = QLabel(self)
        self.image_list = ["images/instagram.png", "images/telegram.png", "images/blackboard.jpg"]  # Slaydlar uchun rasmlarni shu joyga yukla
        self.current_image = 0
        self.update_image()

        timer = QTimer(self)
        timer.timeout.connect(self.next_image)
        timer.start(3000)  # Har 3 soniyada slayd almashinadi

        # **Umumiy Layout**
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        left_layout.addWidget(title)
        left_layout.addLayout(topic_layout)

        right_layout.addWidget(self.image_label)

        main_layout.addLayout(left_layout, 3)
        main_layout.addLayout(right_layout, 2)

        self.setLayout(main_layout)

    def open_topic(self):
        sender = self.sender()
        print(f"{sender.text()} ochildi!")

    def update_image(self):
        pixmap = QPixmap(self.image_list[self.current_image])
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

    def next_image(self):
        self.current_image = (self.current_image + 1) % len(self.image_list)
        self.update_image()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChizmachilikAsoslari()
    window.show()
    sys.exit(app.exec_())
