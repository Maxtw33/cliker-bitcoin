import sys
import os
import json
import random
import hashlib
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel,
                             QVBoxLayout, QWidget, QHBoxLayout, QScrollArea,
                             QGridLayout, QDialog, QMessageBox, QInputDialog,
                             QLineEdit, QStackedWidget, QTableWidget, QTableWidgetItem)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer

SAVE_DIR = "saves"
USER_DATA_FILE = os.path.join(SAVE_DIR, "users.json")
os.makedirs(SAVE_DIR, exist_ok=True)


class Cryptocurrency:
    def __init__(self, name, price, image, next_crypto=None):
        self.name = name
        self.price = price
        self.image = image
        self.next_crypto = next_crypto
        self.unlocked = False


CRYPTOCURRENCIES = [
    Cryptocurrency("Bitcoin", 0, "bitcoin.png", "Ethereum"),
    Cryptocurrency("Ethereum", 1000, "ethereum.png", "BNB"),
    Cryptocurrency("BNB", 100000, "bnb.png", "Monero"),
    Cryptocurrency("Monero", 10000000, "monero.png")
]


class LoginWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Bitcoin Miner Tycoon PRO - Вхід")
        self.setFixedSize(400, 300)
        self.setWindowIcon(QIcon(f"images/{CRYPTOCURRENCIES[0].image}"))

        self.init_ui()
        self.load_users()

    def init_ui(self):
        layout = QVBoxLayout()

        self.stack = QStackedWidget()

        # Login Page
        login_page = QWidget()
        login_layout = QVBoxLayout()

        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Логін")
        login_layout.addWidget(self.login_username)

        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Пароль")
        self.login_password.setEchoMode(QLineEdit.Password)
        login_layout.addWidget(self.login_password)

        login_btn = QPushButton("Увійти")
        login_btn.clicked.connect(self.handle_login)
        login_layout.addWidget(login_btn)

        register_btn = QPushButton("Реєстрація")
        register_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        login_layout.addWidget(register_btn)

        login_page.setLayout(login_layout)
        self.stack.addWidget(login_page)

        # Register Page
        register_page = QWidget()
        register_layout = QVBoxLayout()

        self.register_username = QLineEdit()
        self.register_username.setPlaceholderText("Логін")
        register_layout.addWidget(self.register_username)

        self.register_password = QLineEdit()
        self.register_password.setPlaceholderText("Пароль")
        self.register_password.setEchoMode(QLineEdit.Password)
        register_layout.addWidget(self.register_password)

        self.register_confirm = QLineEdit()
        self.register_confirm.setPlaceholderText("Підтвердіть пароль")
        self.register_confirm.setEchoMode(QLineEdit.Password)
        register_layout.addWidget(self.register_confirm)

        register_submit_btn = QPushButton("Зареєструватися")
        register_submit_btn.clicked.connect(self.handle_register)
        register_layout.addWidget(register_submit_btn)

        back_btn = QPushButton("Назад")
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        register_layout.addWidget(back_btn)

        register_page.setLayout(register_layout)
        self.stack.addWidget(register_page)

        layout.addWidget(self.stack)
        self.setLayout(layout)

    def load_users(self):
        try:
            if os.path.exists(USER_DATA_FILE):
                with open(USER_DATA_FILE, "r") as f:
                    self.users = json.load(f)
            else:
                self.users = {}
        except:
            self.users = {}

    def save_users(self):
        try:
            with open(USER_DATA_FILE, "w") as f:
                json.dump(self.users, f)
            return True
        except:
            return False

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def handle_login(self):
        username = self.login_username.text().strip()
        password = self.login_password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Помилка", "Будь ласка, введіть логін та пароль")
            return

        if username in self.users:
            hashed_password = self.hash_password(password)
            if self.users[username]["password"] == hashed_password:
                self.accept()  # Close the dialog with success
                self.logged_in_user = username
                return

        QMessageBox.warning(self, "Помилка", "Невірний логін або пароль")

    def handle_register(self):
        username = self.register_username.text().strip()
        password = self.register_password.text().strip()
        confirm = self.register_confirm.text().strip()

        if not username or not password or not confirm:
            QMessageBox.warning(self, "Помилка", "Будь ласка, заповніть всі поля")
            return

        if password != confirm:
            QMessageBox.warning(self, "Помилка", "Паролі не співпадають")
            return

        if len(password) < 4:
            QMessageBox.warning(self, "Помилка", "Пароль повинен містити принаймні 4 символи")
            return

        if username in self.users:
            QMessageBox.warning(self, "Помилка", "Користувач з таким логіном вже існує")
            return

        hashed_password = self.hash_password(password)
        self.users[username] = {
            "password": hashed_password,
            "save_file": os.path.join(SAVE_DIR, f"{username}.json")
        }

        if self.save_users():
            QMessageBox.information(self, "Успіх", "Реєстрація успішна! Тепер ви можете увійти.")
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Помилка", "Не вдалося зберегти дані користувача")


class MinerShop(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Магазин майнерів")
        self.setFixedSize(800, 600)
        self.setWindowIcon(QIcon(f"images/{CRYPTOCURRENCIES[0].image}"))

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

        info = QLabel(
            f"Ціна: {miner['price']:.2f} {CRYPTOCURRENCIES[0].name}\nПотужність: {miner['power']:.4f} {CRYPTOCURRENCIES[0].name}/сек")
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


class UpgradeCryptoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Прокачка криптовалют")
        self.setFixedSize(500, 400)
        self.parent = parent

        self.init_ui()

    def init_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        layout = QVBoxLayout()

        for i, crypto in enumerate(CRYPTOCURRENCIES[1:], start=1):
            if not CRYPTOCURRENCIES[i - 1].unlocked:
                continue

            crypto_widget = self.create_crypto_widget(crypto, i)
            layout.addWidget(crypto_widget)

        container.setLayout(layout)
        scroll.setWidget(container)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def create_crypto_widget(self, crypto, index):
        widget = QWidget()
        widget.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 10px;")
        layout = QHBoxLayout()

        # Image
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        self.load_image(image_label, crypto.image)
        layout.addWidget(image_label)

        # Info
        info_layout = QVBoxLayout()

        name_label = QLabel(crypto.name)
        name_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        info_layout.addWidget(name_label)

        price_label = QLabel(f"Ціна: {crypto.price:,} {CRYPTOCURRENCIES[index - 1].name}")
        info_layout.addWidget(price_label)

        if crypto.next_crypto:
            next_label = QLabel(f"Розблокує: {crypto.next_crypto}")
            info_layout.addWidget(next_label)

        layout.addLayout(info_layout)

        # Upgrade button
        btn_upgrade = QPushButton("Прокачати")
        btn_upgrade.setStyleSheet("background-color: #FFA500; color: white; min-width: 100px;")
        btn_upgrade.clicked.connect(lambda _, c=crypto: self.upgrade_crypto(c))

        current_crypto = self.parent.current_crypto
        if current_crypto.name == crypto.name:
            btn_upgrade.setEnabled(False)
            btn_upgrade.setText("Активна")
            btn_upgrade.setStyleSheet("background-color: #4CAF50; color: white; min-width: 100px;")
        elif not crypto.unlocked:
            btn_upgrade.setEnabled(self.parent.can_unlock(crypto))

        layout.addWidget(btn_upgrade)

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
                label.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio))
            else:
                label.setText("No image")
                print(f"Image not found: {full_path}")
        except Exception as e:
            label.setText("Image error")
            print(f"Error loading image: {e}")

    def upgrade_crypto(self, crypto):
        self.parent.upgrade_crypto(crypto)
        self.close()


class LeaderboardWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Таблиця лідерів")
        self.setFixedSize(600, 400)
        self.parent = parent

        self.init_ui()
        self.load_leaderboard()

    def init_ui(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Гравець", "Загальний дохід", "Найвища крипта"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        layout.addWidget(self.table)

        buttons_layout = QHBoxLayout()
        btn_close = QPushButton("Закрити")
        btn_close.clicked.connect(self.close)
        buttons_layout.addWidget(btn_close)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def load_leaderboard(self):
        try:
            if not os.path.exists(USER_DATA_FILE):
                return

            with open(USER_DATA_FILE, "r") as f:
                users = json.load(f)

            leaderboard_data = []

            for username, user_data in users.items():
                save_file = user_data.get("save_file")
                if not save_file or not os.path.exists(save_file):
                    continue

                with open(save_file, "r") as f:
                    game_data = json.load(f)

                # Конвертуємо всі доходи в Bitcoin для порівняння
                total_income = 0
                current_value = game_data.get("bitcoins", 0)
                current_crypto = game_data.get("current_crypto", "Bitcoin")

                # Знаходимо індекс поточної криптовалюти
                crypto_index = 0
                for i, crypto in enumerate(CRYPTOCURRENCIES):
                    if crypto.name == current_crypto:
                        crypto_index = i
                        break

                # Конвертація через всі попередні криптовалюти
                for i in range(crypto_index, 0, -1):
                    conversion_rate = CRYPTOCURRENCIES[i].price
                    current_value *= conversion_rate

                total_income = current_value

                # Додаємо доходи від майнерів (якщо вони є)
                if "owned_miners" in game_data:
                    for miner_name, miner_data in game_data["owned_miners"].items():
                        miner_power = miner_data["data"]["power"] * miner_data["count"]
                        # Конвертуємо потужність майнерів в Bitcoin
                        for i in range(crypto_index, 0, -1):
                            miner_power *= CRYPTOCURRENCIES[i].price
                        total_income += miner_power * 1000  # Припускаємо, що майнери працювали 1000 секунд

                leaderboard_data.append({
                    "username": username,
                    "total_income": total_income,
                    "highest_crypto": current_crypto
                })

            # Сортуємо за загальним доходом
            leaderboard_data.sort(key=lambda x: x["total_income"], reverse=True)

            self.table.setRowCount(len(leaderboard_data))
            for row, data in enumerate(leaderboard_data):
                self.table.setItem(row, 0, QTableWidgetItem(data["username"]))
                self.table.setItem(row, 1, QTableWidgetItem(f"{data['total_income']:,.8f} BTC"))
                self.table.setItem(row, 2, QTableWidgetItem(data["highest_crypto"]))

            self.table.resizeColumnsToContents()

        except Exception as e:
            print("Помилка завантаження таблиці лідерів:", e)


class MegaClicker(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"Bitcoin Miner Tycoon PRO - {username}")
        self.setGeometry(100, 100, 800, 800)

        self.current_crypto = CRYPTOCURRENCIES[0]
        self.bitcoins = 0.0
        self.click_power = 0.0001
        self.owned_miners = {}
        self.upgrade_cost = 0.0005

        # Розблокуємо Bitcoin за замовчуванням
        CRYPTOCURRENCIES[0].unlocked = True

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        # Відображення лого поточної криптовалюти
        self.crypto_image = QLabel()
        self.crypto_image.setAlignment(Qt.AlignCenter)
        self.load_crypto_image()
        main_layout.addWidget(self.crypto_image)

        self.balance_label = QLabel(f"{self.current_crypto.name}: {self.bitcoins:.8f}")
        self.balance_label.setStyleSheet("font-size: 28px; color: #f7931a; font-weight: bold;")
        self.balance_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.balance_label)

        self.mine_button = QPushButton(f"Майнити ({self.click_power:.4f} {self.current_crypto.name})")
        self.mine_button.setStyleSheet(self.get_button_style("#f7931a"))
        self.mine_button.clicked.connect(self.mine_bitcoin)
        main_layout.addWidget(self.mine_button)

        buttons_layout = QHBoxLayout()

        self.upgrade_button = QPushButton(f"Покращити майнер\nЦіна: {self.upgrade_cost:.4f} {self.current_crypto.name}")
        self.upgrade_button.setStyleSheet(self.get_button_style("#ff9500"))
        self.upgrade_button.clicked.connect(self.upgrade_click)
        buttons_layout.addWidget(self.upgrade_button)

        self.shop_button = QPushButton("Магазин майнерів")
        self.shop_button.setStyleSheet(self.get_button_style("#4baf50"))
        self.shop_button.clicked.connect(self.open_shop)
        buttons_layout.addWidget(self.shop_button)

        self.invest_button = QPushButton("Інвестиції")
        self.invest_button.setStyleSheet(self.get_button_style("#FFA500"))
        self.invest_button.clicked.connect(self.invest)
        buttons_layout.addWidget(self.invest_button)

        self.upgrade_crypto_button = QPushButton("Прокачка крипти")
        self.upgrade_crypto_button.setStyleSheet(self.get_button_style("#9b59b6"))
        self.upgrade_crypto_button.clicked.connect(self.open_upgrade_crypto)
        buttons_layout.addWidget(self.upgrade_crypto_button)

        self.leaderboard_button = QPushButton("Таблиця лідерів")
        self.leaderboard_button.setStyleSheet(self.get_button_style("#3498db"))
        self.leaderboard_button.clicked.connect(self.show_leaderboard)
        buttons_layout.addWidget(self.leaderboard_button)

        self.reset_button = QPushButton("Знищити прогрес")
        self.reset_button.setStyleSheet(self.get_button_style("#e74c3c"))
        self.reset_button.clicked.connect(self.reset_progress)
        buttons_layout.addWidget(self.reset_button)

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

    def load_crypto_image(self):
        try:
            base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            image_path = os.path.join(base_dir, "images", self.current_crypto.image)

            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                self.crypto_image.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
            else:
                self.crypto_image.setText(f"{self.current_crypto.name} Logo")
        except Exception as e:
            self.crypto_image.setText("Image Error")
            print(f"Error loading crypto image: {e}")

    def can_unlock(self, crypto):
        index = CRYPTOCURRENCIES.index(crypto)
        prev_crypto = CRYPTOCURRENCIES[index - 1]
        return prev_crypto.unlocked and self.bitcoins >= crypto.price

    def upgrade_crypto(self, crypto):
        if self.can_unlock(crypto):
            # Скидаємо всі значення при переході на нову криптовалюту
            self.bitcoins = 0.0
            self.click_power = 0.0001
            self.upgrade_cost = 0.0005
            self.owned_miners = {}

            crypto.unlocked = True
            self.current_crypto = crypto
            self.update_ui()
            QMessageBox.information(self, "Вітаємо!",
                                    f"Ви прокачали свою крипту до {crypto.name}! Всі значення скинуті.")
        else:
            QMessageBox.warning(self, "Помилка",
                                "У вас недостатньо коштів для прокачки або не розблоковано попередню криптовалюту!")

    def open_upgrade_crypto(self):
        dialog = UpgradeCryptoDialog(self)
        dialog.exec_()

    def show_leaderboard(self):
        leaderboard = LeaderboardWindow(self)
        leaderboard.exec_()

    def reset_progress(self):
        reply = QMessageBox.question(
            self,
            "Підтвердження",
            "Ви впевнені, що хочете повністю скинути прогрес? Цю дію неможливо скасувати!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Скидаємо всі значення
            self.current_crypto = CRYPTOCURRENCIES[0]
            self.bitcoins = 0.0
            self.click_power = 0.0001
            self.upgrade_cost = 0.0005
            self.owned_miners = {}

            # Скидаємо розблокування криптовалют (крім Bitcoin)
            for crypto in CRYPTOCURRENCIES[1:]:
                crypto.unlocked = False

            self.update_ui()
            QMessageBox.information(self, "Прогрес скинуто", "Весь ваш прогрес було скинуто до початкових значень.")

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

    def update_ui(self):
        self.balance_label.setText(f"{self.current_crypto.name}: {self.bitcoins:.8f}")
        self.mine_button.setText(f"Майнити ({self.click_power:.4f} {self.current_crypto.name})")
        self.upgrade_button.setText(f"Покращити майнер\nЦіна: {self.upgrade_cost:.4f} {self.current_crypto.name}")

        if self.owned_miners:
            total_power = sum(item["data"]["power"] * item["count"] for item in self.owned_miners.values())
            miners_text = "Ваші майнери:\n"
            for name, item in self.owned_miners.items():
                miners_text += f"{name}: {item['count']} шт. ({item['data']['power'] * item['count']:.4f} {self.current_crypto.name}/сек)\n"
            miners_text += f"\nЗагальна потужність: {total_power:.4f} {self.current_crypto.name}/сек"
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
            QMessageBox.warning(self, "Недостатньо коштів",
                                f"У вас недостатньо {self.current_crypto.name} для цього покращення!")

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
            QMessageBox.warning(self, "Недостатньо коштів",
                                f"У вас недостатньо {self.current_crypto.name} для покупки цього майнера!")

    def invest(self):
        amount, ok = QInputDialog.getDouble(
            self,
            "Інвестиції",
            f"Введіть суму {self.current_crypto.name} для інвестиції:",
            value=0.001,
            min=0.0001,
            max=self.bitcoins,
            decimals=8
        )

        if ok and amount > 0:
            if amount > self.bitcoins:
                QMessageBox.warning(self, "Помилка", f"У вас недостатньо {self.current_crypto.name}!")
                return

            if random.random() < 0.5:  # Виграш
                multiplier = random.uniform(1.1, 3.0)
                profit = amount * multiplier
                self.bitcoins += profit
                QMessageBox.information(
                    self,
                    "Вітаємо!",
                    f"Ваша інвестиція вдалася!\nВи отримали {profit:.8f} {self.current_crypto.name} (x{multiplier:.2f})"
                )
            else:  # Програш
                loss_multiplier = random.uniform(0.1, 0.9)
                loss = amount * loss_multiplier
                self.bitcoins -= loss
                QMessageBox.warning(
                    self,
                    "Не пощастило",
                    f"Ваша інвестиція не вдалася.\nВи втратили {loss:.8f} {self.current_crypto.name} ({loss_multiplier * 100:.0f}%)"
                )

            self.update_ui()

    def save_game(self):
        try:
            # Load users to find our save file path
            with open(USER_DATA_FILE, "r") as f:
                users = json.load(f)

            save_file = users[self.username]["save_file"]

            data = {
                "current_crypto": self.current_crypto.name,
                "bitcoins": self.bitcoins,
                "click_power": self.click_power,
                "owned_miners": {k: {"count": v["count"], "data": v["data"]} for k, v in self.owned_miners.items()},
                "upgrade_cost": self.upgrade_cost,
                "unlocked_cryptos": [crypto.name for crypto in CRYPTOCURRENCIES if crypto.unlocked],
                "timestamp": int(time.time())  # Додаємо час останнього збереження
            }
            with open(save_file, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print("Не вдалося зберегти гру:", e)

    def load_game(self):
        try:
            # Load users to find our save file path
            with open(USER_DATA_FILE, "r") as f:
                users = json.load(f)

            save_file = users[self.username]["save_file"]

            if os.path.exists(save_file):
                with open(save_file, "r") as f:
                    data = json.load(f)

                self.bitcoins = data.get("bitcoins", 0.0)
                self.click_power = data.get("click_power", 0.0001)
                self.owned_miners = data.get("owned_miners", {})
                self.upgrade_cost = data.get("upgrade_cost", 0.0005)

                # Відновлення поточної криптовалюти
                current_crypto_name = data.get("current_crypto", "Bitcoin")
                for crypto in CRYPTOCURRENCIES:
                    if crypto.name == current_crypto_name:
                        self.current_crypto = crypto
                        break

                # Відновлення розблокованих криптовалют
                unlocked_names = data.get("unlocked_cryptos", ["Bitcoin"])
                for crypto in CRYPTOCURRENCIES:
                    crypto.unlocked = crypto.name in unlocked_names

        except Exception as e:
            print("Не вдалося завантажити збереження:", e)

        self.update_ui()

    def closeEvent(self, event):
        self.save_game()
        event.accept()


def main():
    app = QApplication(sys.argv)

    # Show login window first
    login = LoginWindow()
    if login.exec_() == QDialog.Accepted:
        # If login successful, show the main game window
        window = MegaClicker(login.logged_in_user)
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()