from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PyQt5.QtGui import QPixmap, QFont, QPainter, QColor
from PyQt5.QtCore import Qt, QPoint
import sys
import json
import os

# Chizma ma'lumotlari modeli
class DrawingData:
    def __init__(self, image_path, points):
        self.image_path = image_path
        self.points = points

# Raqamli nuqta
class NumberPoint(QPushButton):
    def __init__(self, number, x, y, name, origin, info_panel, parent=None):
        super().__init__(str(number), parent)
        self.setFixedSize(30, 30)
        self.move(x, y)
        self.name = name
        self.origin = origin
        self.info_panel = info_panel
        self.setStyleSheet("""
            QPushButton {
                background-color: #FF5733;
                color: white;
                border-radius: 15px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #C70039;
            }
        """)
        self.clicked.connect(self.show_info)

    def show_info(self):
        self.info_panel.update_info(self.name, self.origin)

# Ma'lumot paneli
class InfoPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(300)
        self.setStyleSheet("background-color: #fff; border: 1px solid #ccc; border-radius: 5px; padding: 10px;")
        layout = QVBoxLayout()

        self.name_label = QLabel("Qism: Noma'lum")
        self.name_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(self.name_label)

        self.origin_label = QLabel("Kelib chiqishi: Noma'lum")
        self.origin_label.setFont(QFont("Arial", 10))
        layout.addWidget(self.origin_label)

        self.setLayout(layout)

    def update_info(self, name, origin):
        self.name_label.setText(f"Qism: {name}")
        self.origin_label.setText(f"Kelib chiqishi: {origin}")

# Asosiy interfeys
class StructureComposition(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tuzilish va Kompozitsiya")
        self.resize(1000, 700)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.drawings = self.load_drawings()
        self.current_drawing_index = 0
        self.zoom_factor = 1.0

        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()

        # Chizma va ma'lumot paneli
        drawing_layout = QVBoxLayout()

        self.drawing_label = QLabel(self)
        self.drawing_label.setAlignment(Qt.AlignCenter)
        self.drawing_label.setStyleSheet("background-color: white; border: 2px solid #ccc; border-radius: 10px;")
        drawing_layout.addWidget(self.drawing_label)

        # Zoom tugmalari
        zoom_layout = QHBoxLayout()
        self.zoom_in_button = QPushButton("+")
        self.zoom_in_button.setStyleSheet("background-color: #28a745; color: white; border-radius: 5px; padding: 5px;")
        self.zoom_in_button.clicked.connect(self.zoom_in)
        zoom_layout.addWidget(self.zoom_in_button)

        self.zoom_out_button = QPushButton("-")
        self.zoom_out_button.setStyleSheet("background-color: #28a745; color: white; border-radius: 5px; padding: 5px;")
        self.zoom_out_button.clicked.connect(self.zoom_out)
        zoom_layout.addWidget(self.zoom_out_button)

        drawing_layout.addLayout(zoom_layout)
        main_layout.addLayout(drawing_layout)

        # Ma'lumot paneli
        self.info_panel = InfoPanel(self)
        main_layout.addWidget(self.info_panel)

        # Navigatsiya tugmalari
        nav_layout = QHBoxLayout()
        nav_layout.addStretch()

        self.prev_button = QPushButton("Oldingi")
        self.prev_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.prev_button.clicked.connect(self.show_previous)
        nav_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Keyingi")
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.next_button.clicked.connect(self.show_next)
        nav_layout.addWidget(self.next_button)

        nav_layout.addStretch()

        outer_layout = QVBoxLayout()
        outer_layout.addLayout(main_layout)
        outer_layout.addLayout(nav_layout)
        self.setLayout(outer_layout)

        self.load_drawing()

    def load_drawings(self):
        drawings = []
        if os.path.exists("drawings.json"):
            try:
                with open("drawings.json", "r", encoding="utf-8") as file:
                    for line in file:
                        if line.strip():
                            drawing = json.loads(line)
                            drawings.append(DrawingData(drawing["image_path"], drawing["points"]))
            except Exception as e:
                print(f"Xatolik yuz berdi: {e}")
        if not drawings:
            drawings = [
                DrawingData("drawing1.png", [(100, 150, "Val", "Mexanizm"), (200, 300, "Podshipnik", "Dvigatel")]),
                DrawingData("drawing2.png", [(150, 200, "Shaft", "Transmissiya"), (250, 250, "Tishli", "Reduktor")]),
            ]
        return drawings

    def load_drawing(self):
        for child in self.drawing_label.findChildren(NumberPoint):
            child.deleteLater()

        current_drawing = self.drawings[self.current_drawing_index]
        pixmap = QPixmap(current_drawing.image_path)
        if pixmap.isNull():
            pixmap = QPixmap(700, 400)
            pixmap.fill(Qt.white)
            painter = QPainter(pixmap)
            painter.setFont(QFont("Arial", 20))
            painter.drawText(pixmap.rect(), Qt.AlignCenter, "Rasm topilmadi")
            painter.end()
        scaled_pixmap = pixmap.scaled(int(600 * self.zoom_factor), int(400 * self.zoom_factor), Qt.KeepAspectRatio)
        self.drawing_label.setPixmap(scaled_pixmap)

        for i, (x, y, name, origin) in enumerate(current_drawing.points, 1):
            scaled_x = int(x * self.zoom_factor)
            scaled_y = int(y * self.zoom_factor)
            point = NumberPoint(i, scaled_x, scaled_y, name, origin, self.info_panel, self.drawing_label)
            point.show()

        self.prev_button.setEnabled(self.current_drawing_index > 0)
        self.next_button.setEnabled(self.current_drawing_index < len(self.drawings) - 1)

    def zoom_in(self):
        self.zoom_factor += 0.2
        self.load_drawing()

    def zoom_out(self):
        if self.zoom_factor > 0.4:
            self.zoom_factor -= 0.2
            self.load_drawing()

    def show_previous(self):
        if self.current_drawing_index > 0:
            self.current_drawing_index -= 1
            self.load_drawing()

    def show_next(self):
        if self.current_drawing_index < len(self.drawings) - 1:
            self.current_drawing_index += 1
            self.load_drawing()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StructureComposition()
    window.show()
    sys.exit(app.exec_())