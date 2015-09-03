from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from app import app, db
from utils.FixturesCommand import FixturesCommand

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('fixtures', FixturesCommand)

if __name__ == '__main__':
    manager.run()
