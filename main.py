import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MegaClicker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bitcoin Clicker")
        self.setGeometry(100, 100, 400, 500)

        # Центральний віджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Вертикальне розташування
        layout = QVBoxLayout()

        # Зображення біткоїна (можете замінити на своє)
        self.bitcoin_image = QLabel()
        self.bitcoin_image.setAlignment(Qt.AlignCenter)

        # Завантажуємо зображення з інтернету (або локального файлу)
        try:
            pixmap = QPixmap("bitcoin.png")  # Локальний файл
            if pixmap.isNull():  # Якщо файл не знайдено, завантажуємо з інтернету
                import requests
                from io import BytesIO
                response = requests.get("https://bitcoin.org/img/icons/opengraph.png")
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)

            self.bitcoin_image.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        except Exception as e:
            self.bitcoin_image.setText("Не вдалося завантажити зображення")
            print(f"Помилка: {e}")

        layout.addWidget(self.bitcoin_image)

        # Кнопка для кліків
        self.click_button = QPushButton("Майнити Bitcoin!")
        self.click_button.setStyleSheet("""
            QPushButton {
                background-color: #f7931a;
                color: white;
                font-size: 20px;
                padding: 15px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #ffaa2b;
            }
        """)
        self.click_button.clicked.connect(self.on_click)
        layout.addWidget(self.click_button)

        # Лічильник кліків
        self.counter_label = QLabel("BTC: 0")
        self.counter_label.setStyleSheet("font-size: 24px; color: #f7931a;")
        self.counter_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.counter_label)

        # Лічильник
        self.click_count = 0

        central_widget.setLayout(layout)

    def on_click(self):
        self.click_count += 0.0001  # Додаємо невелику кількість BTC
        self.counter_label.setText(f"BTC: {self.click_count:.4f}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MegaClicker()
    window.show()
    sys.exit(app.exec_())