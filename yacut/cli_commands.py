from . import app, db


@app.cli.command('create_all')
def create_all_command():
    """Создать таблицы в базе данных."""
    db.create_all()
