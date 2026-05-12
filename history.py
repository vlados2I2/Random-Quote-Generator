"""Модуль для управления историей сгенерированных цитат и сохранения в JSON."""

import json
from dataclasses import asdict
from pathlib import Path
from quotes import Quote


class HistoryManager:
    def __init__(self, filepath: str = "history.json"):
        self._filepath = Path(filepath)
        self._history: list[Quote] = []
        self.load()

    def add(self, quote: Quote) -> None:
        """Добавляет цитату в историю."""
        self._history.append(quote)
        self.save()

    def get_history(self) -> list[Quote]:
        """Возвращает историю."""
        return list(self._history)

    def clear(self) -> None:
        """Очищает историю."""
        self._history.clear()
        self.save()

    def save(self) -> None:
        """Сохраняет историю в JSON."""
        data = [asdict(q) for q in self._history]
        with open(self._filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self) -> None:
        """Загружает историю из JSON."""
        if not self._filepath.exists():
            return
        try:
            with open(self._filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._history = [Quote(**item) for item in data]
        except (json.JSONDecodeError, TypeError, KeyError):
            self._history = []