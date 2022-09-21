from . import app, db


@app.cli.command('create_all')  # FIXME
def create_all_command():
    """Создать таблицы в базе данных."""  # FIXME
    db.create_all()
