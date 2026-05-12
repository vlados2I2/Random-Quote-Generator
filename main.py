"""Главный модуль GUI-приложения Random Quote Generator."""

import tkinter as tk
from tkinter import ttk, messagebox

from quotes import QuoteManager
from history import HistoryManager


class QuoteApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Генератор случайных цитат")
        self.root.geometry("700x600")
        self.root.minsize(600, 500)

        self.quote_manager = QuoteManager()
        self.history_manager = HistoryManager()

        self._build_ui()
        self._refresh_history()

    def _build_ui(self):
        #Верхняя часть: Генерация
        gen_frame = ttk.LabelFrame(self.root, text="Генерация цитаты", padding=10)
        gen_frame.pack(fill="x", padx=10, pady=5)

        self.quote_label = ttk.Label(
            gen_frame,
            text="Нажмите кнопку, чтобы сгенерировать цитату",
            wraplength=650,
            justify="center",
            font=("Helvetica", 12, "italic"),
        )
        self.quote_label.pack(pady=5)

        self.author_label = ttk.Label(gen_frame, text="", font=("Helvetica", 10, "bold"))
        self.author_label.pack(pady=2)

        ttk.Button(gen_frame, text="Сгенерировать цитату", command=self._generate_quote).pack(pady=5)

        # Средняя часть: Добавление новой цитаты
        add_frame = ttk.LabelFrame(self.root, text="Добавить новую цитату", padding=10)
        add_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(add_frame, text="Текст:").grid(row=0, column=0, sticky="w")
        self.new_text = ttk.Entry(add_frame, width=60)
        self.new_text.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(add_frame, text="Автор:").grid(row=1, column=0, sticky="w")
        self.new_author = ttk.Entry(add_frame, width=60)
        self.new_author.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(add_frame, text="Тема:").grid(row=2, column=0, sticky="w")
        self.new_topic = ttk.Entry(add_frame, width=60)
        self.new_topic.grid(row=2, column=1, padx=5, pady=2)

        ttk.Button(add_frame, text="Добавить цитату", command=self._add_quote).grid(row=3, column=1, sticky="e", pady=5)

        #Фильтрация
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация истории", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="Автор:").grid(row=0, column=0, sticky="w")
        self.filter_author = ttk.Combobox(filter_frame, values=self.quote_manager.get_authors(), width=20)
        self.filter_author.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(filter_frame, text="Тема:").grid(row=0, column=2, sticky="w")
        self.filter_topic = ttk.Combobox(filter_frame, values=self.quote_manager.get_topics(), width=20)
        self.filter_topic.grid(row=0, column=3, padx=5, pady=2)

        ttk.Button(filter_frame, text="Применить фильтр", command=self._apply_filter).grid(row=0, column=4, padx=5)
        ttk.Button(filter_frame, text="Сбросить", command=self._refresh_history).grid(row=0, column=5, padx=5)

        #История
        hist_frame = ttk.LabelFrame(self.root, text="История сгенерированных цитат", padding=10)
        hist_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.history_list = tk.Listbox(hist_frame, width=80, height=12)
        scrollbar = ttk.Scrollbar(hist_frame, orient="vertical", command=self.history_list.yview)
        self.history_list.configure(yscrollcommand=scrollbar.set)

        self.history_list.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ttk.Button(hist_frame, text="Очистить историю", command=self._clear_history).pack(pady=5)

    def _generate_quote(self):
        try:
            quote = self.quote_manager.get_random()
            self.quote_label.config(text=f'"{quote.text}"')
            self.author_label.config(text=f"— {quote.author} | Тема: {quote.topic}")
            self.history_manager.add(quote)
            self._refresh_history()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _add_quote(self):
        text = self.new_text.get()
        author = self.new_author.get()
        topic = self.new_topic.get()

        try:
            self.quote_manager.add_quote(text, author, topic)
            messagebox.showinfo("Успех", "Цитата добавлена!")

            # Обновляем списки фильтров
            self.filter_author["values"] = self.quote_manager.get_authors()
            self.filter_topic["values"] = self.quote_manager.get_topics()

            self.new_text.delete(0, "end")
            self.new_author.delete(0, "end")
            self.new_topic.delete(0, "end")
        except ValueError as e:
            messagebox.showerror("Ошибка валидации", str(e))

    def _refresh_history(self, quotes=None):
        self.history_list.delete(0, "end")
        quotes = quotes or self.history_manager.get_history()
        for q in quotes:
            self.history_list.insert("end", f"{q.author} [{q.topic}]: {q.text[:50]}...")

    def _apply_filter(self):
        author = self.filter_author.get().strip()
        topic = self.filter_topic.get().strip()

        history = self.history_manager.get_history()

        if author:
            history = [q for q in history if q.author.lower() == author.lower()]
        if topic:
            history = [q for q in history if q.topic.lower() == topic.lower()]

        self._refresh_history(history)

    def _clear_history(self):
        self.history_manager.clear()
        self._refresh_history()


def main():
    root = tk.Tk()
    app = QuoteApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()