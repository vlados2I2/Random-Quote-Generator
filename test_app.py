"""Тесты для генератора случайных цитат."""

import unittest
import tempfile
from pathlib import Path

from quotes import QuoteManager, Quote
from history import HistoryManager
from utils import validate_non_empty


class TestQuoteManager(unittest.TestCase):
    def setUp(self):
        self.manager = QuoteManager()

    def test_get_random_returns_quote(self):
        quote = self.manager.get_random()
        self.assertIsInstance(quote, Quote)
        self.assertTrue(quote.text)
        self.assertTrue(quote.author)

    def test_add_quote_valid(self):
        initial = len(self.manager.get_all())
        self.manager.add_quote("Тест", "Автор", "Тема")
        self.assertEqual(len(self.manager.get_all()), initial + 1)

    def test_add_quote_empty_text_raises(self):
        with self.assertRaises(ValueError):
            self.manager.add_quote("   ", "Автор", "Тема")

    def test_add_quote_empty_author_raises(self):
        with self.assertRaises(ValueError):
            self.manager.add_quote("Текст", "", "Тема")

    def test_add_quote_empty_topic_raises(self):
        with self.assertRaises(ValueError):
            self.manager.add_quote("Текст", "Автор", "   ")

    def test_filter_by_author(self):
        self.manager.add_quote("Уникальная", "СпециальныйАвтор", "Тема")
        results = self.manager.filter_by_author("СпециальныйАвтор")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, "Уникальная")

    def test_filter_by_topic(self):
        results = self.manager.filter_by_topic("Вдохновение")
        self.assertTrue(len(results) >= 1)

    def test_filter_no_results(self):
        results = self.manager.filter_by_author("НесуществующийАвтор12345")
        self.assertEqual(len(results), 0)


class TestHistoryManager(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()
        self.history = HistoryManager(self.temp_file.name)

    def tearDown(self):
        Path(self.temp_file.name).unlink(missing_ok=True)

    def test_add_and_get(self):
        q = Quote("Тест", "Автор", "Тема")
        self.history.add(q)
        self.assertEqual(len(self.history.get_history()), 1)

    def test_save_and_load(self):
        q = Quote("Тест", "Автор", "Тема")
        self.history.add(q)

        # Создаем новый менеджер, читающий тот же файл
        new_history = HistoryManager(self.temp_file.name)
        self.assertEqual(len(new_history.get_history()), 1)
        self.assertEqual(new_history.get_history()[0].text, "Тест")

    def test_clear(self):
        self.history.add(Quote("Тест", "А", "Т"))
        self.history.clear()
        self.assertEqual(len(self.history.get_history()), 0)

    def test_load_corrupted_json(self):
        with open(self.temp_file.name, "w", encoding="utf-8") as f:
            f.write("не json")
        # Не должно упасть
        history = HistoryManager(self.temp_file.name)
        self.assertEqual(len(history.get_history()), 0)


class TestUtils(unittest.TestCase):
    def test_validate_non_empty_valid(self):
        self.assertEqual(validate_non_empty("  hello  ", "field"), "hello")

    def test_validate_non_empty_raises(self):
        with self.assertRaises(ValueError):
            validate_non_empty("   ", "field")

    def test_validate_non_empty_empty_string_raises(self):
        with self.assertRaises(ValueError):
            validate_non_empty("", "field")


if __name__ == "__main__":
    unittest.main()