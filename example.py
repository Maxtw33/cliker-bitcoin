import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel,
                             QVBoxLayout, QWidget, QHBoxLayout, QScrollArea,
                             QGridLayout, QDialog, QMessageBox)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer, QSize


class MinerShop(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Магазин майнерів")
        self.setFixedSize(800, 600)

        # Локальні зображення (замініть на свої шляхи)
        self.miners = [
            {"name": "Raspberry Pi", "price": 0.01, "power": 0.0001, "image": "miner1.png"},
            {"name": "Antminer S9", "price": 0.1, "power": 0.001, "image": "miner2.png"},
            {"name": "Antminer S19", "price": 0.5, "power": 0.005, "image": "miner3.png"},
            {"name": "Whatsminer M30S", "price": 1.0, "power": 0.01, "image": "miner4.png"},
            {"name": "Small Farm", "price": 5.0, "power": 0.05, "image": "miner5.png"},
            {"name": "Medium Farm", "price": 20.0, "power": 0.2, "image": "miner6.png"},
            {"name": "Large Farm", "price": 100.0, "power": 1.0, "image": "miner7.png"},
            {"name": "Industrial", "price": 500.0, "power": 5.0, "image": "miner8.png"}
        ]

        self.init_ui()

    def init_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        layout = QGridLayout()

        row, col = 0, 0
        for miner in self.miners:
            miner_widget = self.create_miner_widget(miner)
            layout.addWidget(miner_widget, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

        container.setLayout(layout)
        scroll.setWidget(container)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def create_miner_widget(self, miner):
        widget = QWidget()
        layout = QVBoxLayout()

        # Заголовок
        title = QLabel(miner["name"])
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Зображення
        image = QLabel()
        image.setAlignment(Qt.AlignCenter)
        self.load_image(image, miner["image"])
        layout.addWidget(image)

        # Інформація
        info = QLabel(f"Ціна: {miner['price']:.2f} BTC\nПотужність: {miner['power']:.4f} BTC/сек")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)

        # Кнопка купівлі
        btn = QPushButton("Купити")
        btn.setStyleSheet("background-color: #4CAF50; color: white;")
        btn.clicked.connect(lambda _, m=miner: self.parent().buy_miner(m))
        layout.addWidget(btn)

        widget.setLayout(layout)
        return widget

    def load_image(self, label, image_path):
        try:
            # Шукаємо зображення в папці з грою
            base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            full_path = os.path.join(base_dir, "images", image_path)

            if os.path.exists(full_path):
                pixmap = QPixmap(full_path)
                label.setPixmap(pixmap.scaled(200, 150, Qt.KeepAspectRatio))
            else:
                label.setText("No image")
                print(f"Image not found: {full_path}")
        except Exception as e:
            label.setText("Image error")
            print(f"Error loading image: {e}")


class MegaClicker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bitcoin Miner Tycoon PRO")
        self.setGeometry(100, 100, 800, 800)

        # Грошова система
        self.bitcoins = 0.0
        self.click_power = 0.0001
        self.owned_miners = {}
        self.upgrade_cost = 0.0005

        # Центральний віджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основний layout
        main_layout = QVBoxLayout()

        # Зображення біткоїна
        self.bitcoin_image = QLabel()
        self.bitcoin_image.setAlignment(Qt.AlignCenter)
        self.load_bitcoin_image()
        main_layout.addWidget(self.bitcoin_image)

        # Відображення балансу
        self.balance_label = QLabel(f"BTC: {self.bitcoins:.8f}")
        self.balance_label.setStyleSheet("font-size: 28px; color: #f7931a; font-weight: bold;")
        self.balance_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.balance_label)

        # Кнопка майнінгу
        self.mine_button = QPushButton(f"Майнити ({self.click_power:.4f} BTC)")
        self.mine_button.setStyleSheet(self.get_button_style("#f7931a"))
        self.mine_button.clicked.connect(self.mine_bitcoin)
        main_layout.addWidget(self.mine_button)

        # Layout для кнопок
        buttons_layout = QHBoxLayout()

        # Кнопка апгрейду
        self.upgrade_button = QPushButton(f"Покращити майнер\nЦіна: {self.upgrade_cost:.4f} BTC")
        self.upgrade_button.setStyleSheet(self.get_button_style("#ff9500"))
        self.upgrade_button.clicked.connect(self.upgrade_click)
        buttons_layout.addWidget(self.upgrade_button)

        # Кнопка магазину
        self.shop_button = QPushButton("Магазин майнерів")
        self.shop_button.setStyleSheet(self.get_button_style("#4baf50"))
        self.shop_button.clicked.connect(self.open_shop)
        buttons_layout.addWidget(self.shop_button)

        main_layout.addLayout(buttons_layout)

        # Інформація про майнери
        self.miners_info = QLabel("У вас немає майнерів")
        self.miners_info.setStyleSheet("font-size: 16px;")
        self.miners_info.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.miners_info)

        central_widget.setLayout(main_layout)

        # Таймер для авто-майнінгу
        self.auto_click_timer = QTimer()
        self.auto_click_timer.timeout.connect(self.auto_mine)
        self.auto_click_timer.start(1000)

    def get_button_style(self, color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 8px;
                min-height: 60px;
            }}
            QPushButton:hover {{
                background-color: {self.lighten_color(color)};
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
            }}
        """

    def lighten_color(self, color):
        try:
            r = min(255, int(color[1:3], 16) + 40)
            g = min(255, int(color[3:5], 16) + 40)
            b = min(255, int(color[5:7], 16) + 40)
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return color

    def load_bitcoin_image(self):
        try:
            base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            image_path = os.path.join(base_dir, "images", "bitcoin.png")

            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                self.bitcoin_image.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
            else:
                self.bitcoin_image.setText("BTC Logo")
        except Exception as e:
            self.bitcoin_image.setText("Image Error")
            print(f"Error loading bitcoin image: {e}")

    def update_ui(self):
        self.balance_label.setText(f"BTC: {self.bitcoins:.8f}")
        self.mine_button.setText(f"Майнити ({self.click_power:.4f} BTC)")
        self.upgrade_button.setText(f"Покращити майнер\nЦіна: {self.upgrade_cost:.4f} BTC")

        # Оновлення інформації про майнери
        if self.owned_miners:
            total_power = sum(miner["power"] * count for miner, count in self.owned_miners.items())
            miners_text = "Ваші майнери:\n"
            for miner, count in self.owned_miners.items():
                miners_text += f"{miner['name']}: {count} шт. ({miner['power'] * count:.4f} BTC/сек)\n"
            miners_text += f"\nЗагальна потужність: {total_power:.4f} BTC/сек"
            self.miners_info.setText(miners_text)
        else:
            self.miners_info.setText("У вас немає майнерів")

        # Вимкнення кнопок, якщо недостатньо BTC
        self.upgrade_button.setEnabled(self.bitcoins >= self.upgrade_cost)

    def mine_bitcoin(self):
        self.bitcoins += self.click_power
        self.update_ui()

    def auto_mine(self):
        if self.owned_miners:
            total_power = sum(miner["power"] * count for miner, count in self.owned_miners.items())
            self.bitcoins += total_power
            self.update_ui()

    def upgrade_click(self):
        if self.bitcoins >= self.upgrade_cost:
            self.bitcoins -= self.upgrade_cost
            self.click_power *= 2
            self.upgrade_cost *= 3
            self.update_ui()
        else:
            QMessageBox.warning(self, "Недостатньо BTC", "У вас недостатньо Bitcoin для цього покращення!")

    def open_shop(self):
        shop = MinerShop(self)
        shop.exec_()

    def buy_miner(self, miner):
        if self.bitcoins >= miner["price"]:
            self.bitcoins -= miner["price"]
            if miner in self.owned_miners:
                self.owned_miners[miner] += 1
            else:
                self.owned_miners[miner] = 1
            self.update_ui()
        else:
            QMessageBox.warning(self, "Недостатньо BTC",
                                f"Вам потрібно ще {miner['price'] - self.bitcoins:.2f} BTC для покупки цього майнера!")


if __name__ == "__main__":
    # Перевірка наявності папки images
    if not os.path.exists("images"):
        os.makedirs("images")
        print("Створено папку 'images'. Будь ласка, додайте туди зображення майнерів.")

    app = QApplication(sys.argv)
    window = MegaClicker()
    window.show()
    sys.exit(app.exec_())