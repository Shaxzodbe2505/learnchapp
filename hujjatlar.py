import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QUrl
from PyQt5.QtGui import QDesktopServices

class DocumentViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hujjatlar")
        self.setGeometry(420, 180, 1200, 800)

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Fayl listini yaratish
        self.listWidget = QListWidget()
        self.listWidget.setViewMode(QListWidget.IconMode)  # Ikonka rejimi
        self.listWidget.setIconSize(QSize(100, 100))  # Ikonkaning o‘lchami
        self.listWidget.setGridSize(QSize(120, 120))  # Gridning o‘lchami (icon + bo‘sh joy)
        self.listWidget.setSpacing(20)  # Ikonkalar orasidagi masofa
        self.listWidget.setResizeMode(QListWidget.Adjust)  # Oyna kattalashtirilganda o‘lcham moslashadi
        self.listWidget.setMovement(QListWidget.Static)

        # Fayllarni qo‘shish
        self.folder_path = os.path.expanduser('hujjatlar')  # 'Hujjatlar' papkasini ochish
        if os.path.exists(self.folder_path):
            for file in os.listdir(self.folder_path):
                if file.endswith(('.pdf', '.docx', '.doc','.pptx')):  # Faqat kerakli fayllarni chiqarish
                    item = QListWidgetItem(file)
                    item.setData(32, os.path.join(self.folder_path, file))  # Fayl yo'lini saqlash

                    # Ikonka qo'shish
                    icon_path = 'images/ext_pdf_filetype_icon_176234.png'  # O‘zingizning ikonka faylingizni kiriting
                    if os.path.exists(icon_path):
                        item.setIcon(QIcon(icon_path))
                    else:
                        item.setIcon(QIcon.fromTheme("text-x-generic"))  # Standart ikonka

                    item.setSizeHint(QSize(120, 120))  # Ikonka bilan elementning o‘lchami
                    self.listWidget.addItem(item)

        # Faylni ustiga bosganda ochish uchun signal bog'lash
        self.listWidget.itemClicked.connect(self.openFile)

        # Listni dizaynlash
        self.listWidget.setStyleSheet("""
            QListWidget {
                background-color: #f0f0f0;
                color: #333;
                font-size: 18px;
                border: none;
            }
            QListWidget::item:hover {
                background-color: #d3d3d3;
            }
            QListWidget::item:selected {
                background-color: #81a4cd;
                color: white;
            }
        """)

        layout.addWidget(self.listWidget)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def openFile(self, item):
        file_path = item.data(32)  # Fayl yo'lini olish
        if file_path and os.path.exists(file_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))  # Faylni ochish

def main():
    app = QApplication(sys.argv)
    viewer = DocumentViewer()
    viewer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
