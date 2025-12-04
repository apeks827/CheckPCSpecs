# 🔧 Troubleshooting Guide

## Частые проблемы и их решения

### 1. ImportError: attempted relative import with no known parent package

**Проблема:**
```
Traceback (most recent call last):
  File "checkpcspecs\app.py", line 10, in <module>
    from .core import SpecsChecker
ImportError: attempted relative import with no known parent package
```

**Причина:** Вы пытаетесь запустить файл напрямую (`python checkpcspecs/app.py`), а он использует относительные импорты.

**Решения:**

#### ✅ Вариант 1: Запуск как модуль (рекомендуется)
```bash
# Из корневой директории проекта
python -m checkpcspecs
```

#### ✅ Вариант 2: Использовать run.py
```bash
# Из корневой директории проекта
python run.py
```

#### ✅ Вариант 3: Установить как пакет
```bash
# Из корневой директории проекта
pip install -e .

# Теперь можно запускать
checkpcspecs
```

---

### 2. Unexpected indentation

**Проблема:**
```
IndentationError: unexpected indent
```

**Причина:** Смешение табуляций и пробелов, или неправильное количество пробелов.

**Решение:**

Файл должен быть исправлен (уже исправлен в последнем коммите). Если проблема осталась:

```bash
# Автоматически исправить форматирование
pip install black
black checkpcspecs/
```

**Стандарт:** Python использует **4 пробела** для отступов (PEP 8).

---

### 3. ModuleNotFoundError: No module named 'checkpcspecs'

**Проблема:**
```
ModuleNotFoundError: No module named 'checkpcspecs'
```

**Причина:** Пакет не установлен или вы не в правильной директории.

**Решение:**

```bash
# Убедитесь, что вы в корневой директории проекта
cd /path/to/CheckPCSpecs

# Установите пакет
pip install -e .

# Или запустите через модуль
python -m checkpcspecs
```

---

### 4. Зависимости не установлены

**Проблема:**
```
ModuleNotFoundError: No module named 'psutil'
```

**Решение:**

```bash
# Установить все зависимости
pip install -r requirements.txt

# Или установить пакет со всеми зависимостями
pip install -e .

# Или с dev-зависимостями
pip install -e ".[dev]"
```

---

### 5. Тесты не запускаются

**Проблема:**
```
pytest: command not found
```

**Решение:**

```bash
# Установить dev-зависимости
pip install -e ".[dev]"

# Или только pytest
pip install pytest pytest-cov pytest-asyncio

# Запустить тесты
pytest
```

---

### 6. Ошибка при определении типа диска

**Проблема:**
```
ImportError: No module named 'wmi'
```

**Причина:** На не-Windows системах или без установленного WMI.

**Решение:**

```bash
# На Windows
pip install wmi pywin32

# На Linux/Mac это не работает (только Windows)
# Приложение вернёт "Unknown" для типа диска
```

---

### 7. Ping требует прав администратора

**Проблема:** Ping возвращает ошибку или не работает.

**Решение:**

```bash
# Запустите приложение от имени администратора
# ПКМ на PowerShell/CMD -> "Запуск от имени администратора"
python -m checkpcspecs
```

**Альтернатива:** Приложение всё равно будет работать, просто не покажет точный пинг.

---

### 8. Ошибка при сборке executable

**Проблема:**
```
pyinstaller: command not found
```

**Решение:**

```bash
# Установить PyInstaller
pip install pyinstaller

# Собрать executable
pyinstaller checkpcspecs.spec

# Результат в dist/checkpcspecs.exe
```

---

### 9. Black/Flake8/Mypy не найдены

**Проблема:**
```
black: command not found
```

**Решение:**

```bash
# Установить все dev-инструменты
pip install -e ".[dev]"

# Или по отдельности
pip install black flake8 mypy isort
```

---

### 10. Git hooks не работают

**Проблема:** Pre-commit hooks не запускаются.

**Решение:**

```bash
# Установить pre-commit
pip install pre-commit

# Установить hooks
pre-commit install

# Запустить вручную
pre-commit run --all-files
```

---

## 📋 Checklist для проверки установки

```bash
# 1. Клонировать репозиторий
git clone https://github.com/apeks827/CheckPCSpecs.git
cd CheckPCSpecs
git checkout refactor/complete-restructure

# 2. Проверить Python версию (должна быть 3.8+)
python --version

# 3. Установить зависимости
pip install -e ".[dev]"

# 4. Проверить установку
python -c "import checkpcspecs; print('OK')"

# 5. Запустить тесты
pytest

# 6. Запустить приложение
python -m checkpcspecs
```

---

## 🆘 Если ничего не помогло

1. **Проверьте версию Python:**
   ```bash
   python --version  # Должна быть 3.8+
   ```

2. **Создайте виртуальное окружение:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Переустановите зависимости:**
   ```bash
   pip uninstall checkpcspecs -y
   pip install -e ".[dev]" --force-reinstall
   ```

4. **Проверьте структуру проекта:**
   ```bash
   # Убедитесь, что есть эти файлы
   ls checkpcspecs/__init__.py
   ls checkpcspecs/__main__.py
   ls pyproject.toml
   ```

5. **Создайте issue на GitHub:**
   - [https://github.com/apeks827/CheckPCSpecs/issues](https://github.com/apeks827/CheckPCSpecs/issues)
   - Укажите версию Python, ОС, полный текст ошибки

---

## 💡 Полезные команды

```bash
# Проверить где установлен Python
where python  # Windows
which python  # Linux/Mac

# Проверить установленные пакеты
pip list

# Проверить путь к модулю
python -c "import checkpcspecs; print(checkpcspecs.__file__)"

# Очистить кэш Python
find . -type d -name __pycache__ -exec rm -r {} +  # Linux/Mac
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"  # Windows

# Пересобрать проект
pip install -e . --no-build-isolation --force-reinstall
```

---

## 📚 Дополнительная информация

- **Документация по установке:** [README.md](README.md)
- **Руководство по тестам:** [tests/README.md](tests/README.md)
- **Подробности улучшений:** [IMPROVEMENTS.md](IMPROVEMENTS.md)
- **Сводка изменений:** [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md)
