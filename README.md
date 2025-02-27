# University Choice Advisor Bot 🎓

Telegram бот, помогающий абитуриентам выбрать подходящий университет на основе своих предпочтений, используя метод анализа иерархий (МАИ/AHP).

## Описание проекта

Бот помогает пользователям принять обоснованное решение при выборе университета, анализируя различные пользовательские критерии (критерии, введенные пользователем и оцененные на основе собственныех предпочтений):
**Пример** критериев ввода:
- Академическая репутация
- Стоимость обучения
- Расположение
- Перспективы трудоустройства
- Инфраструктура
- И другие важные факторы

## Технологии

- Python 3.10+
- aiogram 3.x
- Метод анализа иерархий (AHP - Analytic Hierarchy Process) библиотека ahpy
- SQLite
- redis
## Установка и запуск

1. Клонировать репозиторий:
```bash
git clone https://github.com/your-Efosee/university-choice-ahp-bot.git
cd university-choice-ahp-bot
```

2. Установить зависимости:
```bash
pip install -r requirements.txt ** (Файл requirements.txt в данный момент не доступен) **
```

3. Создать файл `.env` и добавить необходимые переменные окружения:
```

```

4. Запустить бота:
```bash
python main.py
```

## Использование

1. Найдите бота в Telegram: [@your_bot_username]
2. Начните диалог командой /start
3. Следуйте инструкциям бота для оценки критериев
4. Получите рекомендации по выбору университета

## Структура проекта

```
university-choice-ahp-bot/
├── main.py
├── dictionary.py
├── requirements.txt ** (В данный момент отсутствует) **
├── .env
├── .gitignore
└── core/
    ├── db/
    |   ├──CreateDB.py
    |   └── db_utils.py
    ├── filters/ ...
    ├── handlers/ ...
    ├── keyboards/ ...
    ├── middlewaries/ ...
    ├── redis/ ...
    └── utils/ ...

```

## Автор

[Efosee] - [(https://github.com/Efosee)]
