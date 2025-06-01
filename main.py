import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel,
                             QVBoxLayout, QWidget, QHBoxLayout, QScrollArea,
                             QGridLayout, QDialog, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

SAVE_FILE = "save_data.json"

class MinerShop(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Магазин майнерів")
        self.setFixedSize(800, 600)

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

        title = QLabel(miner["name"])
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        image = QLabel()
        image.setAlignment(Qt.AlignCenter)
        self.load_image(image, miner["image"])
        layout.addWidget(image)

        info = QLabel(f"Ціна: {miner['price']:.2f} BTC\nПотужність: {miner['power']:.4f} BTC/сек")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)

        btn = QPushButton("Купити")
        btn.setStyleSheet("background-color: #4CAF50; color: white;")
        btn.clicked.connect(lambda _, m=miner: self.buy_miner(m))
        layout.addWidget(btn)

        widget.setLayout(layout)
        return widget

    def load_image(self, label, image_path):
        try:
            base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            full_path = os.path.join(base_dir, "images", image_path)

            if os.path.exists(full_path):
                pixmap = QPixmap(full_path)
                if pixmap.isNull():
                    raise Exception("Image file is invalid or corrupted")
                label.setPixmap(pixmap.scaled(200, 150, Qt.KeepAspectRatio))
            else:
                label.setText("No image")
                print(f"Image not found: {full_path}")
        except Exception as e:
            label.setText("Image error")
            print(f"Error loading image: {e}")

    def buy_miner(self, miner):
        parent = self.parent()
        if parent and hasattr(parent, 'buy_miner'):
            parent.buy_miner(miner)


class MegaClicker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bitcoin Miner Tycoon PRO")
        self.setGeometry(100, 100, 800, 800)

        self.bitcoins = 0.0
        self.click_power = 0.0001
        self.owned_miners = {}
        self.upgrade_cost = 0.0005

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        # Відображення лого біткоіна з файла
        self.bitcoin_image = QLabel()
        self.bitcoin_image.setAlignment(Qt.AlignCenter)
        self.load_bitcoin_image()
        main_layout.addWidget(self.bitcoin_image)

        self.balance_label = QLabel(f"BTC: {self.bitcoins:.8f}")
        self.balance_label.setStyleSheet("font-size: 28px; color: #f7931a; font-weight: bold;")
        self.balance_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.balance_label)

        self.mine_button = QPushButton(f"Майнити ({self.click_power:.4f} BTC)")
        self.mine_button.setStyleSheet(self.get_button_style("#f7931a"))
        self.mine_button.clicked.connect(self.mine_bitcoin)
        main_layout.addWidget(self.mine_button)

        buttons_layout = QHBoxLayout()

        self.upgrade_button = QPushButton(f"Покращити майнер\nЦіна: {self.upgrade_cost:.4f} BTC")
        self.upgrade_button.setStyleSheet(self.get_button_style("#ff9500"))
        self.upgrade_button.clicked.connect(self.upgrade_click)
        buttons_layout.addWidget(self.upgrade_button)

        self.shop_button = QPushButton("Магазин майнерів")
        self.shop_button.setStyleSheet(self.get_button_style("#4baf50"))
        self.shop_button.clicked.connect(self.open_shop)
        buttons_layout.addWidget(self.shop_button)

        main_layout.addLayout(buttons_layout)

        self.miners_info = QLabel("У вас немає майнерів")
        self.miners_info.setStyleSheet("font-size: 16px;")
        self.miners_info.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.miners_info)

        central_widget.setLayout(main_layout)

        self.auto_click_timer = QTimer()
        self.auto_click_timer.timeout.connect(self.auto_mine)
        self.auto_click_timer.start(1000)

        self.load_game()

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

        if self.owned_miners:
            total_power = sum(item["data"]["power"] * item["count"] for item in self.owned_miners.values())
            miners_text = "Ваші майнери:\n"
            for name, item in self.owned_miners.items():
                miners_text += f"{name}: {item['count']} шт. ({item['data']['power'] * item['count']:.4f} BTC/сек)\n"
            miners_text += f"\nЗагальна потужність: {total_power:.4f} BTC/сек"
            self.miners_info.setText(miners_text)
        else:
            self.miners_info.setText("У вас немає майнерів")

        self.upgrade_button.setEnabled(self.bitcoins >= self.upgrade_cost)

    def mine_bitcoin(self):
        self.bitcoins += self.click_power
        self.update_ui()

    def auto_mine(self):
        if self.owned_miners:
            total_power = sum(item["data"]["power"] * item["count"] for item in self.owned_miners.values())
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
        price = miner["price"]
        if self.bitcoins >= price:
            self.bitcoins -= price
            name = miner["name"]
            if name in self.owned_miners:
                self.owned_miners[name]["count"] += 1
            else:
                self.owned_miners[name] = {"data": miner, "count": 1}
            self.update_ui()
        else:
            QMessageBox.warning(self, "Недостатньо BTC", "У вас недостатньо Bitcoin для покупки цього майнера!")

    def save_game(self):
        try:
            data = {
                "bitcoins": self.bitcoins,
                "click_power": self.click_power,
                "owned_miners": {k: {"count": v["count"], "data": v["data"]} for k, v in self.owned_miners.items()},
                "upgrade_cost": self.upgrade_cost
            }
            with open(SAVE_FILE, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print("Не вдалося зберегти гру:", e)

    def load_game(self):
        try:
            if os.path.exists(SAVE_FILE):
                with open(SAVE_FILE, "r") as f:
                    data = json.load(f)
                self.bitcoins = data.get("bitcoins", 0.0)
                self.click_power = data.get("click_power", 0.0001)
                self.owned_miners = data.get("owned_miners", {})
                # Перевірка і приведення даних майнерів
                for k, v in self.owned_miners.items():
                    if "data" in v and "name" not in v["data"]:
                        v["data"]["name"] = k
                self.upgrade_cost = data.get("upgrade_cost", 0.0005)
        except Exception as e:
            print("Не вдалося завантажити збереження:", e)
        self.update_ui()

    def closeEvent(self, event):
        self.save_game()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = MegaClicker()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
