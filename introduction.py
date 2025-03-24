import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea
from PyQt5.QtGui import QFont, QPixmap, QIcon, QPalette, QBrush
from PyQt5.QtCore import Qt

class IntroductionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Muhandislik Grafikasi')
        self.setGeometry(0, 0, 1920, 1080)
        self.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        self.setWindowIcon(QIcon('images/technical-drawing.ico'))



        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        # Asosiy panel uchun palitra
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap("images/introbg.jpg")))
        self.setPalette(palette)


        # ScrollArea yaratish (ko'proq ma'lumot ko'rsatish uchun)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")

        content_widget = QWidget()
        content_layout = QVBoxLayout()

        # Muhandislik Grafikasi haqida matn
        text = f"""
        Muhandislik grafikasi fani haqida umumiy ma'lumot

Muhandislik grafikasi — umumiy geometriyaning bir bo‘limi bo‘lib, u narsalarning geometrik xususiyatlariga asoslanib, ularning shakllari, o‘lchamlari va o‘zaro joylashishini tasvirlash usullari orqali o‘rganadi. Bu fan pozitsion, metrik va konstruktiv masalalarni yechish algoritmlarini o‘rgatadi.

Muhandislik grafikasi orqali talabaning fazoviy tasavvurlari kengayadi, tasvirlarni yasash va oldindan yasalgan chizmalarni o‘qiy bilish ko‘nikmasi shakllanadi. Muhandislik grafikasi qonunlari asosida nafaqat mavjud narsalar, balki tasavvurdagi ob’ektlar ham tasvirlanadi. Bu esa yangilik va ixtirolarni amalga oshirishga asos bo‘ladi.

📌 Muhandislik grafikasining asosiy mazmuni 
Fazodagi figuralarning tekislikda tasvirlarini yasash usullarini yaratish va tahlil qilish.
Figuralarning berilgan tasvirlariga asoslanib, unga oid fazoviy masalalarni yechish va tekshirish usullarini o‘rganish.
Muhandislik grafikasi qonunlari asosida buyumlarning tekislikdagi chizmalari hosil qilinadi. Bu orqali buyumning shakli, o‘lchamlari va joylashuvi haqida to‘liq tasavvur qilish mumkin bo‘ladi.

📌 Muhandislik grafikasi va tarixiy yutuqlar
Texnikaning rivojlanishida o‘rta osiyolik olimlarning hissasi katta bo‘lgan. Masalan, Abu Ali ibn Sino tomonidan ishlab chiqilgan yuk ko‘targich mexanizmi bunga yorqin misol bo‘la oladi. Tarixiy yutuqlarni zamonaviy texnik taraqqiyot bilan uyg‘unlashtirish intellektual salohiyatli kadrlar tayyorlashning asosiy omillaridan biridir.

📌 Ta'lim jarayonidagi ahamiyati
O‘zbekistonda ta’lim sohasidagi islohotlar shaxs manfaatlari va ta’lim ustuvorligi asosiga qurilgan. Shu sababli, muhandislik grafikasi fanini o‘qitishda DTS (Davlat Ta’lim Standarti) talablariga muvofiq bilim, ko‘nikma va malakalarni shakllantirishga alohida e’tibor qaratilmoqda.

Talabalar semestr davomida muhandislik grafikasi fanidan 8 ta hisob-grafik vazifani bajaradilar. Joriy nazorat uchun 20 ball ajratilgan bo‘lib, har bir grafik masalaga 2,5 ball belgilangan. Grafik masalalarning mazmuni, formati va topshirish muddati fan dasturida aniq ko‘rsatilgan.

Muhandislik grafikasi fanini o‘qitishda talabalarning nazariy bilimlari va amaliy ko‘nikmalarini mustahkamlash uchun maxsus metodik tavsiyalar ishlab chiqilgan. Talabalar grafik masalalarni bajarish orqali nafaqat bilim va ko‘nikmalarni rivojlantiradi, balki muhandislik fikrlash qobiliyatini ham shakllantiradi. ✅
        """

        text_label = QLabel(text)
        text_label.setFont(QFont('Arial', 14))
        text_label.setStyleSheet("color: #ffffff;")
        text_label.setWordWrap(True)
        text_label.setAlignment(Qt.AlignTop)

        content_layout.addWidget(text_label)

        # Rasmni qo'shish
        image = QPixmap("images/1616092917782_MGkMv7y.jpg")  # Rasm fayl nomini moslab o'zgartiring
        image_label = QLabel()
        image_label.setPixmap(image.scaled(500, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)

        content_layout.addWidget(image_label)

        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)

        layout.addWidget(scroll_area)

        # Chiqish tugmasi
        close_button = QPushButton("Orqaga")
        close_button.setFont(QFont('Arial', 14))
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #6a0dad;
                color: #ffffff;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7b1fa2;
            }
        """)
        close_button.clicked.connect(self.close)

        layout.addWidget(close_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    window = IntroductionWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
