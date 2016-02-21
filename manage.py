from app import create_app
from app.database import db, populate_db
from flask_migrate import Migrate, MigrateCommand
from flask_script import (
    Server,
    Shell,
    Manager,
    prompt_bool,
)


def _make_context():
    return dict(
        app=create_app(),
        db=db,
        populate_db=populate_db
    )

app = create_app()

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)


@manager.command
def create_db(num_users=5):
    """Creates database tables and populates them."""
    db.create_all()
    populate_db()


@manager.command
def drop_db():
    """Drops database tables."""
    if prompt_bool('Are you sure?'):
        db.drop_all()


@manager.command
def recreate_db():
    """Same as running drop_db() and create_db()."""
    drop_db()
    create_db()


if __name__ == '__main__':
    manager.run()
