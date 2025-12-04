# Contributing to CheckPCSpecs

Спасибо, что рассматриваете возможность внести вклад в CheckPCSpecs! 🎉

## Как помочь

### Сообщения об ошибках

Если вы нашли ошибку:

1. Проверьте [Issues](https://github.com/apeks827/CheckPCSpecs/issues) - может она уже сообщена
2. Создайте новый issue с подробным описанием:
   - Версия приложения
   - Версия Python
   - Операционная система
   - Шаги для воспроизведения
   - Ожидаемое поведение
   - Фактическое поведение
   - Скриншоты (если применимо)

### Предложения по улучшению

Мы открыты к новым идеям! Создайте issue с меткой `enhancement` и опишите:
- Что вы хотите улучшить
- Почему это важно
- Как это должно работать

### Pull Requests

1. **Fork репозитория**

2. **Создайте ветку**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Установите зависимости**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Внесите изменения**

5. **Проверьте код**
   ```bash
   # Форматирование
   black checkpcspecs/
   
   # Линтинг
   flake8 checkpcspecs/
   
   # Типы
   mypy checkpcspecs/
   
   # Тесты
   pytest
   ```

6. **Создайте коммит**
   ```bash
   git commit -m "feat: add amazing feature"
   ```
   
   Используйте [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` - новая функциональность
   - `fix:` - исправление ошибки
   - `docs:` - документация
   - `style:` - форматирование
   - `refactor:` - рефакторинг
   - `test:` - тесты
   - `chore:` - рутинные задачи

7. **Отправьте изменения**
   ```bash
   git push origin feature/amazing-feature
   ```

8. **Создайте Pull Request**

## Стандарты кода

### Python Style Guide

- Следуйте [PEP 8](https://pep8.org/)
- Используйте `black` для форматирования
- Добавляйте type hints
- Пишите docstrings (формат Google)

### Пример docstring

```python
def check_cpu(cores: int, threads: int) -> CPUResult:
    """Check CPU specifications.
    
    Args:
        cores: Number of physical cores
        threads: Number of logical threads
        
    Returns:
        CPUResult with rating and score
        
    Raises:
        ValueError: If cores or threads < 1
    """
    pass
```

### Структура импортов

```python
# Стандартная библиотека
import os
import sys
from pathlib import Path

# Сторонние библиотеки
import psutil
import speedtest

# Локальные импорты
from .core import SpecsChecker
from .utils import ResourceManager
```

## Тестирование

### Написание тестов

```python
import pytest
from checkpcspecs.core import SpecsChecker

def test_check_os():
    """Test OS checking functionality."""
    checker = SpecsChecker()
    result = checker.check_os()
    
    assert result.version is not None
    assert result.score in [-999, 1, 2]
    assert result.rating in [-1, 0, 1, 2]
```

### Запуск тестов

```bash
# Все тесты
pytest

# С покрытием
pytest --cov=checkpcspecs

# Определённый файл
pytest tests/test_core.py
```

## Документация

- Обновляйте README.md при добавлении функций
- Добавляйте записи в CHANGELOG.md
- Пишите комментарии к сложному коду

## Правила поведения

- Будьте уважительны
- Конструктивная критика
- Помогайте новичкам
- Цените разнообразие мнений

## Вопросы?

Не стесняйтесь задавать вопросы в [Issues](https://github.com/apeks827/CheckPCSpecs/issues) или свяжитесь с майнтейнерами.

Спасибо за ваш вклад! ❤️
