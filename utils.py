"""Утилиты для валидации ввода."""


def validate_non_empty(value: str, field_name: str) -> str:
    """Проверяет, что строка не пустая после очистки."""
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"Поле '{field_name}' не может быть пустым")
    return cleaned