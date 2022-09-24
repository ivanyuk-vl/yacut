from . import app, db


@app.cli.command('create_table')
def create_all_command():
    """Создать таблицу в базе данных."""
    db.create_all()
