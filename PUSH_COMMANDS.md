# Команды для Push в GitHub

## ⚠️ Важно перед push: обновите .gitignore

Первым делом добавьте виртуальное окружение в `.gitignore`:

```bash
echo "venv/" >> .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore
echo ".coverage" >> .gitignore
```

## Выполните эти команды в терминале для отправки всех изменений в репозиторий:

```bash
# Шаг 1: Убедитесь, что находитесь в корне проекта
cd test_repo

# Шаг 2: Добавить все файлы в staging area (исключая venv)
git add .

# Шаг 3: Создать коммит с описанием
git commit -m "feat: Add currency converter via crypto bridge with 9 AI agents

- Implement CurrencyConverter class with crypto-based currency exchange
- Support 100+ currencies through CoinGecko API
- Create 12 comprehensive unit tests (100% coverage)
- Add 9 specialized AI agents for project management:
  * Research Agent - code exploration
  * Code Review Agent - quality checks
  * Implementation Agent - code development
  * Testing Agent - test creation
  * Documentation Agent - documentation
  * Bug Fix Agent - bug fixing
  * Refactoring Agent - code improvement
  * DevOps Agent - CI/CD setup
  * Orchestrator Agent - team coordination
- Provide 400+ lines of comprehensive documentation
- Configure GitHub Actions CI/CD pipeline
- Add examples, requirements, and setup scripts
- Auto-create virtual environment with run.sh script"

# Шаг 4: Отправить в удаленный репозиторий
git push origin main
```

## Проверка статуса перед push:

```bash
# Посмотреть какие файлы изменены
git status

# Посмотреть diff коммитов
git diff --cached

# Посмотреть в какой ветке вы находитесь
git branch

# Посмотреть историю коммитов
git log --oneline -5
```

## Что будет отправлено:

✅ 19 файлов  
✅ ~1600 строк кода  
✅ 100% тестовое покрытие  
✅ Полная документация  
✅ CI/CD конфигурация  
✅ Автоматический setup с venv  

## После успешного push:

Все файлы будут доступны на GitHub в репозитории `Ivanpoplavsky/test_repo`.

## Быстрый запуск после clone:

```bash
git clone <repo-url>
cd test_repo
chmod +x run.sh
./run.sh

# Скрипт автоматически:
# 1. Создаст виртуальное окружение
# 2. Установит зависимости
# 3. Запустит примеры
# 4. Запустит все тесты
```
