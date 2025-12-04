# CheckPCSpecs

<div align="center">
  <img src="logo.png" alt="CheckPCSpecs Logo" width="200"/>
  <p><strong>Проверка соответствия ПК системным требованиям</strong></p>
</div>

## О проекте

CheckPCSpecs — это инструмент для проверки соответствия компьютера минимальным системным требованиям. Приложение анализирует характеристики ПК и предоставляет подробный отчёт о совместимости.

## Возможности

- ✅ **Проверка операционной системы** — версия и разрядность Windows
- 💾 **Анализ оперативной памяти** — объём RAM
- 🔧 **Тестирование процессора** — определение модели и количества ядер
- 💿 **Проверка типа накопителя** — SSD/HDD/eMMC
- 🌐 **Тестирование сети** — скорость загрузки/отдачи и пинг
- 📊 **Общая оценка** — вердикт о соответствии требованиям

## Установка

### Из исходников

```bash
# Клонировать репозиторий
git clone https://github.com/apeks827/CheckPCSpecs.git
cd CheckPCSpecs

# Установить зависимости
pip install -r requirements.txt

# Запустить приложение
python -m checkpcspecs
```

### Как модуль Python

```bash
pip install -e .
checkpcspecs
```

### Сборка EXE (PyInstaller)

```bash
pip install pyinstaller
pyinstaller checkpcspecs.spec
```

Готовый исполняемый файл будет в папке `dist/`.

## Использование

### Графический интерфейс

```bash
python -m checkpcspecs
```

1. Введите ФИО
2. Нажмите "Сохранить"
3. Дождитесь завершения проверки
4. Изучите результаты

### Программное использование

```python
from checkpcspecs import SpecsChecker, SpeedTester, PingTester

# Проверка характеристик
checker = SpecsChecker()

os_result = checker.check_os()
print(f"OS: {os_result.version}, Score: {os_result.score}")

cpu_result = checker.check_cpu()
print(f"CPU: {cpu_result.name}")

# Тест сети
speed = SpeedTester.test()
print(f"Download: {speed.download} Mbps, Upload: {speed.upload} Mbps")

ping = PingTester.test()
print(f"Ping: {ping.latency} ms")
```

## Структура проекта

```
CheckPCSpecs/
├── checkpcspecs/
│   ├── __init__.py          # Главный модуль
│   ├── __main__.py          # Точка входа
│   ├── app.py               # Контроллер приложения
│   ├── core/                # Проверка характеристик
│   │   ├── __init__.py
│   │   ├── models.py        # Модели данных
│   │   └── specs_checker.py # Логика проверки
│   ├── network/             # Сетевые тесты
│   │   ├── __init__.py
│   │   ├── speedtest.py     # Тест скорости
│   │   ├── ping.py          # Тест пинга
│   │   └── evaluator.py     # Оценка сети
│   ├── ui/                  # Графический интерфейс
│   │   ├── __init__.py
│   │   ├── main_window.py   # Главное окно
│   │   └── components.py    # UI компоненты
│   └── utils/               # Утилиты
│       ├── __init__.py
│       ├── resources.py     # Управление ресурсами
│       └── scoring.py       # Подсчёт баллов
├── icon.ico                 # Иконка приложения
├── logo.png                 # Логотип
├── requirements.txt         # Зависимости
├── setup.py                 # Установка пакета
├── checkpcspecs.spec        # PyInstaller конфиг
└── README.md                # Документация
```

## Системные требования

### Минимальные
- **ОС:** Windows 7/8/8.1/10/11 (x64)
- **RAM:** 4 GB
- **Процессор:** Dual-core 2.0 GHz
- **Интернет:** 10 Mbps

### Рекомендуемые
- **ОС:** Windows 10/11 (x64)
- **RAM:** 8 GB+
- **Процессор:** Quad-core 2.5 GHz+
- **Диск:** SSD
- **Интернет:** 20 Mbps+

## Критерии оценки

| Компонент | Отлично | Хорошо | Минимум | Не соответствует |
|-----------|---------|--------|---------|------------------|
| **ОС** | Windows 11 | Windows 10 | Windows 7/8 | Другие |
| **RAM** | ≥8 GB | ≥6 GB | ≥4 GB | <4 GB |
| **CPU** | 4+ ядра | 2+ ядра + HT | 2 ядра | Устаревшие |
| **Диск** | SSD | HDD/eMMC | HDD | — |
| **Интернет** | ≥20 Mbps, <30ms | ≥20 Mbps, <100ms | ≥10 Mbps | <10 Mbps |

**Итоговая оценка:**
- **≥18 баллов** — соответствует требованиям ✅
- **0-17 баллов** — соответствует минимальным требованиям ⚠️
- **<0 баллов** — не соответствует требованиям ❌

## Разработка

### Установка dev-зависимостей

```bash
pip install -e ".[dev]"
```

### Запуск тестов

```bash
pytest
```

### Форматирование кода

```bash
black checkpcspecs/
flake8 checkpcspecs/
mypy checkpcspecs/
```

## Зависимости

- **psutil** — информация о системе
- **py-cpuinfo** — данные о процессоре
- **Pillow** — работа с изображениями
- **speedtest-cli** — тест скорости интернета
- **icmplib** — ICMP ping
- **nest-asyncio** — поддержка async в Tkinter

## Известные проблемы

1. **Ping требует прав администратора** — для точного измерения пинга рекомендуется запускать от имени администратора
2. **Определение типа диска** — может не работать на старых системах без PowerShell
3. **Тест скорости** — может занять 30-60 секунд в зависимости от соединения

## Лицензия

MIT License — см. [LICENSE](LICENSE)

## Автор

**apeks827** — [GitHub](https://github.com/apeks827)

## Скриншоты

<div align="center">
  <img src="screen.png" alt="CheckPCSpecs Screenshot" width="600"/>
</div>

---

<div align="center">
  Made with ❤️ in Russia
</div>
