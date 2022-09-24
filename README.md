<p align="center">
  <a href="https://github.com/ivanyuk-vl/yacut"><img alt="GitHub Actions status" src="https://github.com/ivanyuk-vl/yacut/workflows/tests/badge.svg"></a>
</p>

# Проект YaCut

## Описание
Проект YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.

## Технологии
- flask 2.0.2
- flask_babel 2.0.0
- flask_sqlalchemy 2.5.1
- flask_wtf 1.0.0

## Запуск проекта
Клонировать репозиторий и перейти в него в командной строке:

`git clone git@github.com:ivanyuk-vl/yacut.git`

`cd yacut`

Cоздать и активировать виртуальное окружение:

`python -m venv venv`

* Если у вас Linux/MacOS

    `source venv/bin/activate`

* Если у вас windows

    `source venv/scripts/activate`

Установить зависимости из файла requirements.txt:

`python -m pip install --upgrade pip`

`pip install -r requirements.txt`

Создать в корне проекта файл .env по шаблону:

```
FLASK_ENV=development
FLASK_APP=yacut
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=<secret_key>
```

Создать базу данных с таблицей:

`flask create_all`

Запустить сервер:

`flask run`

## Автор
https://github.com/ivanyuk-vl
