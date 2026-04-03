#!/bin/bash

# Скрипт для быстрого запуска и тестирования конвертора валют

set -e

echo "🚀 Запуск Конвертора Валют через Крипто-Мост"
echo "=============================================="
echo ""

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не найден. Пожалуйста, установите Python 3.8+"
    exit 1
fi

echo "✅ Python найден: $(python3 --version)"
echo ""

# Установка зависимостей
echo "📦 Устанавливаю зависимости..."
pip install -q -r requirements.txt
echo "✅ Зависимости установлены"
echo ""

# Запуск примеров
echo "▶️  Запускаю примеры использования..."
echo ""
python3 examples.py
echo ""

# Запуск тестов
echo "🧪 Запускаю unit тесты..."
echo ""
python3 -m unittest discover -s tests -p "test_*.py" -v
echo ""

echo "=============================================="
echo "✅ Все готово! Проект работает корректно"
echo ""
echo "📚 Дальнейшие шаги:"
echo "  1. Посмотрите README.md для полной документации"
echo "  2. Используйте примеры из examples.py"
echo "  3. Изучите тесты в tests/ для понимания API"
echo ""
echo "🎉 Спасибо за использование!"
