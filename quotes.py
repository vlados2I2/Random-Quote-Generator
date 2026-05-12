"""Модуль с предопределенными цитатами и их управлением."""

import random
from dataclasses import dataclass


@dataclass
class Quote:
    text: str
    author: str
    topic: str


DEFAULT_QUOTES = [
    Quote("Будь тем изменением, которое хочешь видеть в мире.", "Махатма Ганди", "Вдохновение"),
    Quote("Единственный способ делать великую работу - любить то, что делаешь.", "Стив Джобс", "Работа"),
    Quote("Жизнь - это то, что с тобой происходит, пока ты строишь планы.", "Джон Леннон", "Жизнь"),
    Quote("Не бойся быть не таким, как все. Бойся быть таким, как все.", "Неизвестный автор", "Мотивация"),
    Quote("Успех - это способность двигаться от неудачи к неудаче, не теряя энтузиазма.", "Уинстон Черчилль", "Успех"),
    Quote("Образование - это самое мощное оружие, которое можно использовать для изменения мира.", "Нельсон Мандела", "Образование"),
    Quote("Счастье не в том, чтобы делать всегда что хочешь, а в том, чтобы всегда хотеть того, что делаешь.", "Лев Толстой", "Счастье"),
    Quote("Всё, что ни делается, - к лучшему.", "Михаил Булгаков", "Философия"),
    Quote("Мы - то, что мы думаем. Всё, что мы есть, возникло с нашими мыслями.", "Будда", "Философия"),
    Quote("Лучший способ предсказать будущее - изобрести его.", "Алан Кей", "Технологии"),
    Quote("Простота - это высшая степень утонченности.", "Леонардо да Винчи", "Искусство"),
    Quote("Если хочешь изменить мир - начни с себя.", "Лев Толстой", "Вдохновение"),
]


class QuoteManager:
    def __init__(self):
        self._quotes = list(DEFAULT_QUOTES)

    def get_random(self) -> Quote:
        """Возвращает случайную цитату."""
        if not self._quotes:
            raise ValueError("Список цитат пуст")
        return random.choice(self._quotes)

    def add_quote(self, text: str, author: str, topic: str) -> None:
        """Добавляет новую цитату с валидацией."""
        text = text.strip()
        author = author.strip()
        topic = topic.strip()

        if not text:
            raise ValueError("Текст цитаты не может быть пустым")
        if not author:
            raise ValueError("Имя автора не может быть пустым")
        if not topic:
            raise ValueError("Тема не может быть пустой")

        self._quotes.append(Quote(text, author, topic))

    def get_all(self) -> list[Quote]:
        """Возвращает все цитаты."""
        return list(self._quotes)

    def get_authors(self) -> list[str]:
        """Возвращает список уникальных авторов."""
        return sorted(set(q.author for q in self._quotes))

    def get_topics(self) -> list[str]:
        """Возвращает список уникальных тем."""
        return sorted(set(q.topic for q in self._quotes))

    def filter_by_author(self, author: str) -> list[Quote]:
        """Фильтрует цитаты по автору."""
        return [q for q in self._quotes if q.author.lower() == author.lower().strip()]

    def filter_by_topic(self, topic: str) -> list[Quote]:
        """Фильтрует цитаты по теме."""
        return [q for q in self._quotes if q.topic.lower() == topic.lower().strip()]