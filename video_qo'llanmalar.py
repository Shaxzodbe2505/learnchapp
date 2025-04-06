from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys
import json
import os
from googleapiclient.discovery import build

# YouTube API sozlamalari
API_KEY = "AIzaSyBk6HZR18e6ed1z_jwJHwsgLAXj9ntmV_c"


# --- VIDEO MA'LUMOTLARI MODELI ---
class VideoData:
    def __init__(self, title, duration, youtube_url):
        self.title = title
        self.duration = duration
        self.youtube_url = youtube_url


# --- HAR BIR VIDEO UCHUN KARTOCHKA ---
class VideoCard(QWidget):
    def __init__(self, video: VideoData):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        self.video_preview = QWebEngineView()
        self.video_preview.setFixedSize(300, 300)
        self.video_preview.load(QUrl(f"{video.youtube_url}&controls=0"))
        layout.addWidget(self.video_preview)

        info_layout = QVBoxLayout()
        info_layout.setAlignment(Qt.AlignCenter)

        title = QLabel(video.title)
        title.setFont(QFont("Arial", 12, QFont.Bold))
        info_layout.addWidget(title)

        duration = QLabel(video.duration)
        duration.setStyleSheet("color: gray; font-size: 12px;")
        info_layout.addWidget(duration)

        play_btn = QPushButton("Play")
        play_btn.setStyleSheet(
            "background-color: red; color: white; border-radius: 10px; font-size: 16px; padding: 10px 20px;"
        )
        play_btn.clicked.connect(lambda: self.play_fullscreen(video.youtube_url))
        info_layout.addWidget(play_btn)

        info_layout.addStretch()
        layout.addLayout(info_layout)
        self.setLayout(layout)

    def play_fullscreen(self, youtube_url):
        self.fullscreen_window = QWidget()
        self.fullscreen_window.setWindowFlags(Qt.Window)
        layout = QVBoxLayout()

        self.fullscreen_video = QWebEngineView()
        self.fullscreen_video.load(QUrl(f"{youtube_url}&autoplay=1&controls=1"))
        layout.addWidget(self.fullscreen_video)

        close_btn = QPushButton("Close")
        close_btn.setStyleSheet(
            "background-color: gray; color: white; border-radius: 5px; font-size: 14px; padding: 5px 10px;")
        close_btn.clicked.connect(self.close_fullscreen)
        layout.addWidget(close_btn)

        self.fullscreen_window.setLayout(layout)
        self.fullscreen_window.showFullScreen()

    def close_fullscreen(self):
        self.fullscreen_window.close()


# --- ASOSIY INTERFEYS ---
class VideoLibrary(QWidget):
    def __init__(self):
        super().__init__()
        self.videos = self.load_videos()
        self.videos_per_page = 3
        self.current_page = 1
        self.init_ui()

        # Real-time yangilanish uchun timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_videos)
        self.timer.start(10000)  # Har 5 soniyada yangilash

    def init_ui(self):
        self.setWindowTitle("Video Qo'llanmalar")
        self.resize(1920, 1080)

        self.main_layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.video_container = QWidget()
        self.video_layout = QVBoxLayout()
        self.video_container.setLayout(self.video_layout)
        self.scroll_area.setWidget(self.video_container)
        self.main_layout.addWidget(self.scroll_area)

        self.pagination_layout = QHBoxLayout()
        self.main_layout.addLayout(self.pagination_layout)

        self.setLayout(self.main_layout)
        self.update_display()

    def get_video_duration(self, video_id):
        try:
            youtube = build('youtube', 'v3', developerKey=API_KEY)
            request = youtube.videos().list(part="contentDetails", id=video_id)
            response = request.execute()
            duration = response['items'][0]['contentDetails']['duration']  # PT3M45S formatida
            return self.parse_duration(duration)
        except Exception as e:
            print(f"Davomiylikni olishda xatolik: {e}")
            return "05:00"  # Xatolik bo'lsa standart davomiylik

    def parse_duration(self, duration):
        # PT3M45S -> 03:45 formatiga o'tkazish
        minutes = 0
        seconds = 0
        if 'M' in duration:
            minutes = int(duration.split('PT')[1].split('M')[0])
            if 'S' in duration:
                seconds = int(duration.split('M')[1].split('S')[0])
        elif 'S' in duration:
            seconds = int(duration.split('PT')[1].split('S')[0])
        return f"{minutes:02d}:{seconds:02d}"

    def load_videos(self):
        video_list = []
        if os.path.exists("videos.json"):
            try:
                with open("videos.json", "r", encoding="utf-8") as file:
                    for line in file:
                        if line.strip():
                            video_data = json.loads(line)
                            # Video ID ni URL dan ajratib olish
                            video_id = video_data["link"].split("/embed/")[1].split("?")[0]
                            duration = self.get_video_duration(video_id)
                            video_list.append(
                                VideoData(video_data["subject"], duration, video_data["link"])
                            )
            except Exception as e:
                print(f"Xatolik yuz berdi: {e}")

        if not video_list:
            video_list = [
                VideoData("To'g'ri chiziq tahlili", "03:45",
                          "https://www.youtube.com/embed/uSy8s3KcthY?si=uIuOAqsNFkufc92P"),
                VideoData("TEKISLIK TAHLILI. ПЛОСКИЙ АНАЛИЗ.", "04:12",
                          "https://www.youtube.com/embed/jYWvt1XV0-c?si=PgRXTKE5oyIfNXDr"),
                VideoData("To'g'ri chiziq Tahlili 2. Прямой анализ.", "02:30",
                          "https://www.youtube.com/embed/cXsCDWrN_Ik?si=G9xj9I5-NdFG1NqI"),
                VideoData("Video 4", "05:00", "https://www.youtube.com/embed/WgctMnHukoY?si=qVdd6beHibib9YhJ"),
                VideoData("Video 5", "03:20", "https://www.youtube.com/embed/GS9Ug22BdJs?si=L6TCnayXNjmy6Dr_"),
            ]

        return video_list

    def refresh_videos(self):
        self.videos = self.load_videos()
        self.update_display()

    def get_filtered_videos(self):
        return self.videos

    def update_display(self):
        for i in reversed(range(self.video_layout.count())):
            widget = self.video_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        filtered = self.get_filtered_videos()
        start = (self.current_page - 1) * self.videos_per_page
        end = start + self.videos_per_page
        for video in filtered[start:end]:
            self.video_layout.addWidget(VideoCard(video))

        for i in reversed(range(self.pagination_layout.count())):
            widget = self.pagination_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        total_pages = (len(filtered) + self.videos_per_page - 1) // self.videos_per_page
        for i in range(1, total_pages + 1):
            btn = QPushButton(str(i))
            btn.setCheckable(True)
            if i == self.current_page:
                btn.setStyleSheet("font-weight: bold; background-color: lightblue;")
                btn.setChecked(True)
            btn.clicked.connect(lambda _, p=i: self.set_page(p))
            self.pagination_layout.addWidget(btn)

    def set_page(self, page):
        self.current_page = page
        self.update_display()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoLibrary()
    window.show()
    sys.exit(app.exec_())