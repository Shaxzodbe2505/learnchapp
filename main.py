import subprocess
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QGridLayout, QMessageBox
from PyQt5.QtGui import QFont, QPalette, QBrush, QPixmap, QIcon, QDesktopServices
from PyQt5.QtCore import Qt, QUrl
from login import LoginWindow

def main():
    app = QApplication(sys.argv)

    def show_main_window():
        print("Debug: Showing main window")  # Debug statement
        from main import CourseApp
        main_window = CourseApp()
        main_window.show()

    login_window = LoginWindow(on_success=show_main_window)
    login_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    print("Debug: Starting application")  # Debug statement
    main()

class CourseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Muhandislik Grafikasi')
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowIcon(QIcon('images/technical-drawing.ico'))
        self.is_menu_open = False
        self.initUI()





    def initUI(self):




        # Asosiy panel uchun palitra
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap("images/background.jpg")))
        self.setPalette(palette)



        # Asosiy layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)





        # Sarlavha
        title = QLabel("Muhandislik Grafikasi Darslari")
        title.setFont(QFont('Arial', 30, QFont.Bold))
        title.setStyleSheet("color: #000000;")
        title.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(title)




        # Tavsif
        description = QLabel("Biz bilan bu fanni qulayroq va osonroq o'rganing! 🚀")
        description.setFont(QFont('Arial', 18))
        description.setStyleSheet("color: #666666;")
        description.setAlignment(Qt.AlignLeft)
        description.setWordWrap(True)
        main_layout.addWidget(description)
        main_layout.addSpacing(100)  # Savoldan keyin biroz bo'sh joy qoldirish

        # Darslar ro‘yxati
        lessons = [
            ("1. Kirish", "00:00", True),
            ("2. Chizmachilik asoslari", "00:00", False),
            ("3. Mashg'ulotlar", "00:00", True),
            ("4. Tuzilish va kompozitsiya", "00:00", True),
            ("5. Sinov", "00:00", False),
            ("6. Dastur haqida", "00:00", True)
        ]

        lessons_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        for index, (lesson, time, is_active) in enumerate(lessons):
            bg_color = "rgba(106, 13, 173, 0.6)" if is_active else "rgba(240, 240, 240, 0.6)"
            fg_color = "#ffffff" if is_active else "#000000"

            # Tugma yaratish
            button = QPushButton(f"{lesson}  |  {time}")
            button.setFont(QFont('Arial', 20))
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {bg_color};
                    color: {fg_color};
                    padding: 10px;
                    border-radius: 12px;
                    text-align: left;
                    backdrop-filter: blur(10px); /* Orqa fonni blur qilish */
                    border: 1px solid rgba(255, 255, 255, 0.2); /* Yengil chegarasi */
                    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); /* Tashqi soya */
                    transition: background-color 0.3s ease, box-shadow 0.3s ease;
                }}
                QPushButton:hover {{
                    background-color: {'rgba(92, 11, 165, 0.8)' if is_active else 'rgba(224, 224, 224, 0.8)'};
                    box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.3);
                }}
                QPushButton:pressed {{
                    background-color: {'rgba(75, 10, 143, 0.8)' if is_active else 'rgba(208, 208, 208, 0.8)'};
                    box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.4);
                }}
            """)
            button.setFixedWidth(600)

            # Tugmaga signal bog‘lash
            button.clicked.connect(lambda checked, l=lesson: self.showLesson(l))

            if index < 3:
                left_layout.addWidget(button)
            else:
                right_layout.addWidget(button)

        lessons_layout.addLayout(left_layout)
        lessons_layout.addSpacing(20)
        lessons_layout.addLayout(right_layout)
        main_layout.addLayout(lessons_layout)
        main_layout.addSpacing(100)  # Savoldan keyin biroz bo'sh joy qoldirish

        # "Barcha darsliklar" tugmasi
        all_lessons_btn = QPushButton("Qo'shimcha")
        all_lessons_btn.setFont(QFont('Arial', 18))
        all_lessons_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(106, 13, 173, 0.6); /* Shaffof binafsha rang */
                color: #ffffff;
                padding: 10px;
                border-radius: 12px;
                backdrop-filter: blur(10px); /* Orqa fonni blur qilish */
                border: 1px solid rgba(255, 255, 255, 0.2); /* Yengil chegarasi */
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); /* Tashqi soya */
                transition: background-color 0.3s ease, box-shadow 0.3s ease;
            }
            QPushButton:hover {
                background-color: rgba(92, 11, 165, 0.8); /* Shaffof quyuqroq binafsha */
                box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.3); /* Kuchliroq yaltirash */
            }
            QPushButton:pressed {
                background-color: rgba(75, 10, 143, 0.8); /* Shaffof quyuq binafsha */
                box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.4); /* Kamroq yaltirash */
            }
        """)
        all_lessons_btn.setFixedWidth(300)
        main_layout.addWidget(all_lessons_btn, alignment=Qt.AlignCenter)

        # Statistik ma'lumotlar
        stats = [
            ("Daraja: ", "📊"),
            ("Talabalar: 25K", "👥"),
            ("Video qo'llanmalar: 10hrs", "📽️"),
            ("Hujjatlar: 3K", "📁")
        ]

        stats_layout = QGridLayout()
        stats_layout.setSpacing(20)

        from functools import partial

        for i, (text, icon) in enumerate(stats):
            stat_button = QPushButton(f"{icon}\n{text}")
            stat_button.setFixedSize(300, 120)
            stat_button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.3);
                    border-radius: 12px;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
                    font-size: 24px;
                    color: #000;
                    padding: 10px;
                    transition: background-color 0.3s ease, box-shadow 0.3s ease;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.5);
                    box-shadow: 0px 6px 14px rgba(0, 0, 0, 0.3);
                }
                QPushButton:pressed {
                    background-color: rgba(255, 255, 255, 0.6);
                    box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.4);
                }
            """)

            # To‘g‘ri ulash (functools.partial ishlatish)
            if text.strip() == "Hujjatlar:":
                stat_button.clicked.connect(partial(self.open_documents, "Hujjatlar"))

            stats_layout.addWidget(stat_button, i // 2, i % 2)

        main_layout.addLayout(stats_layout)

        # Overview qismi
        overview_title = QLabel("Aloqa:")
        overview_title.setFont(QFont('Arial', 14, QFont.Bold))
        overview_title.setStyleSheet("color: #000000; margin-top: 10px;")
        main_layout.addWidget(overview_title)

        overview_text = QLabel("Sahifalarimizga obuna bo'ling")
        overview_text.setFont(QFont('Arial', 12))
        overview_text.setStyleSheet("color: #666666;")
        overview_text.setWordWrap(True)
        main_layout.addWidget(overview_text)

        # Gorizontal layout (Telegram va Instagram yonma-yon turadi)
        icon_layout = QHBoxLayout()

        # Telegram icon
        telegram_icon = QLabel(self)
        telegram_pixmap = QPixmap('images/telegram.png')  # Fayl nomini moslashtiring
        telegram_icon.setPixmap(telegram_pixmap.scaled(32, 32, Qt.KeepAspectRatio))
        telegram_icon.setCursor(Qt.PointingHandCursor)
        telegram_icon.mousePressEvent = lambda event: self.open_link('https://t.me/MuhandislikGrafikasi_002')
        icon_layout.addWidget(telegram_icon)

        # Instagram icon
        instagram_icon = QLabel(self)
        instagram_pixmap = QPixmap('images/instagram.png')  # Fayl nomini moslashtiring
        instagram_icon.setPixmap(instagram_pixmap.scaled(32, 32, Qt.KeepAspectRatio))
        instagram_icon.setCursor(Qt.PointingHandCursor)
        instagram_icon.mousePressEvent = lambda event: self.open_link('https://instagram.com')
        icon_layout.addWidget(instagram_icon)

        # Ikonlar joylashishini markazga keltirish
        icon_layout.setAlignment(Qt.AlignLeft)

        # Gorizontal layoutni asosiy layoutga qo'shish
        main_layout.addLayout(icon_layout)
        icon_layout.addWidget(telegram_icon)
        icon_layout.addSpacing(20)  # 20 piksel bo'shliq
        icon_layout.addWidget(instagram_icon)




    def open_link(self, url):
        QDesktopServices.openUrl(QUrl(url))



    def showLesson(self, lesson):
        if lesson == "1. Kirish":
            reply = QMessageBox.question(self, "Ko'rish",
                                         f"Siz {lesson} ni belgiladingiz. Boshlaymizmi?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    subprocess.Popen(["python", "introduction.py"])
                except Exception as e:
                    QMessageBox.critical(self, "Xatolik", f"Xatolik yuz berdi: {e}")

        elif lesson == "5. Sinov":
            reply = QMessageBox.question(self, "Testni ishga tushirish",
                                         f"Siz {lesson} ni belgiladingiz. Boshlaymizmi?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    subprocess.Popen(["python", "test_uchun.py"])
                except Exception as e:
                    QMessageBox.critical(self, "Xatolik", f"Xatolik yuz berdi: {e}")


        else:
            QMessageBox.information(self, "Lesson Selected",
                                    f"{lesson} hali tayyor emas!")

    def open_documents(self, stats):
        if stats == "Hujjatlar":
            reply = QMessageBox.question(self, "Ko'rish",
                                         f"Siz {stats} ni belgiladingiz. Boshlaymizmi?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    subprocess.Popen(["python", "hujjatlar.py"])
                except Exception as e:
                    QMessageBox.critical(self, "Xatolik", f"Xatolik yuz berdi: {e}")
        else:
            QMessageBox.information(self, "Lesson Selected",
                                    f"{stats} hali tayyor emas!")


def main():
    app = QApplication(sys.argv)
    window = CourseApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
