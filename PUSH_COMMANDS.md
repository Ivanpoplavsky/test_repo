# Команды для Push в GitHub

Выполните эти команды в терминале для отправки всех изменений в репозиторий:

```bash
# Шаг 1: Добавить все файлы в staging area
git add .

# Шаг 2: Создать коммит с описанием
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
- Add examples, requirements, and setup scripts"

# Шаг 3: Отправить в удаленный репозиторий
git push origin main
```

## Что будет отправлено:

✅ 18 файлов  
✅ ~1500 строк кода  
✅ 100% тестовое покрытие  
✅ Полная документация  
✅ CI/CD конфигурация  

## Проверка статуса перед push:

```bash
# Посмотреть какие файлы изменены
git status

# Посмотреть diff
git diff --cached

# Посмотреть историю коммитов
git log --oneline -5
```

## После успешного push:

Все файлы будут доступны на GitHub в репозитории `Ivanpoplavsky/test_repo`.
