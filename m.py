import tkinter as tk


class ClickerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Клікер")

        self.clicks = 0
        self.click_power = 1

        # Основний інтерфейс
        self.click_label = tk.Label(root, text=f"Кліків: {self.clicks}", font=("Arial", 24))
        self.click_label.pack(pady=20)

        self.click_button = tk.Button(
            root,
            text="Клікай!",
            font=("Arial", 18),
            command=self.add_click,
            bg="lightgreen",
            padx=20,
            pady=10
        )
        self.click_button.pack()

        # Кнопка апгрейду
        self.upgrade_button = tk.Button(
            root,
            text=f"Підвищити силу кліку (1 клік) - вартість: {self.get_upgrade_cost()}",
            font=("Arial", 12),
            command=self.upgrade_power,
            state=tk.DISABLED
        )
        self.upgrade_button.pack(pady=20)

        # Автоклікер (розблокується пізніше)
        self.auto_clicker_button = tk.Button(
            root,
            text="Купити автоклікер (5 кліків/сек) - вартість: 50",
            font=("Arial", 12),
            command=self.buy_auto_clicker,
            state=tk.DISABLED
        )
        self.auto_clicker_button.pack()

        self.auto_clickers = 0
        self.auto_clicker_active = False

    def add_click(self):
        self.clicks += self.click_power
        self.update_display()

        # Перевіряємо, чи можна активувати кнопку апгрейду
        if self.clicks >= self.get_upgrade_cost():
            self.upgrade_button.config(state=tk.NORMAL)
        else:
            self.upgrade_button.config(state=tk.DISABLED)

        # Перевіряємо, чи можна купити автоклікер
        if self.clicks >= 50:
            self.auto_clicker_button.config(state=tk.NORMAL)
        else:
            self.auto_clicker_button.config(state=tk.DISABLED)

    def get_upgrade_cost(self):
        return self.click_power * 10

    def upgrade_power(self):
        cost = self.get_upgrade_cost()
        if self.clicks >= cost:
            self.clicks -= cost
            self.click_power += 1
            self.update_display()
            self.upgrade_button.config(
                text=f"Підвищити силу кліку (+1) - вартість: {self.get_upgrade_cost()}"
            )

    def buy_auto_clicker(self):
        if self.clicks >= 50:
            self.clicks -= 50
            self.auto_clickers += 1
            self.update_display()

            if not self.auto_clicker_active:
                self.auto_clicker_active = True
                self.auto_click()

    def auto_click(self):
        if self.auto_clicker_active:
            self.clicks += self.auto_clickers * 5 * self.click_power
            self.update_display()
            self.root.after(1000, self.auto_click)  # Автоклік кожну секунду

    def update_display(self):
        self.click_label.config(text=f"Кліків: {self.clicks}\nСила кліку: {self.click_power}")
        if self.auto_clickers > 0:
            self.click_label.config(text=self.click_label["text"] + f"\nАвтоклікерів: {self.auto_clickers}")


if __name__ == "__main__":
    root = tk.Tk()
    game = ClickerGame(root)
    root.mainloop()