import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QFileSystemModel, QVBoxLayout, QWidget
from PyQt5.QtCore import QDir


class DocumentViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hujjatlar ko'ruvchi")
        self.setGeometry(0, 0, 1920, 1080)

        self.initUI()

    def initUI(self):
        # Markaziy vidjet
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Fayl tizimi modeli
        self.model = QFileSystemModel()
        self.model.setRootPath('')  # Hamma yo'lni ko'rsatish uchun bo'sh qoldiramiz
        self.model.setFilter(QDir.AllDirs | QDir.Files)  # Faollarni ko'rsatish uchun

        # Faqat PDF va Word fayllarni ko'rsatish uchun filtr
        self.model.setNameFilters(["*.pdf", "*.docx", "*.doc"])
        self.model.setNameFilterDisables(False)  # Filtrni ishga tushirish

        # QTreeView yaratish (Windows fayl sistemasi ko'rinishida)
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(os.path.expanduser("hujjatlar")))  # Hujjatlar papkasini ochish
        self.tree.setSortingEnabled(True)  # Saralash imkoniyati

        # Interfeys dizayni
        self.tree.setStyleSheet("""
            QTreeView {
                background-color: #f0f0f0;
                alternate-background-color: #e6e6e6;
                selection-background-color: #a8d0e6;
                color: #333;
                font-size: 24px;
                border: none;
            }
            QTreeView::item:hover {
                background-color: #d3d3d3;
            }
            QTreeView::item:selected {
                background-color: #81a4cd;
                color: white;
            }
        """)

        layout.addWidget(self.tree)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


def main():
    app = QApplication(sys.argv)
    viewer = DocumentViewer()
    viewer.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
