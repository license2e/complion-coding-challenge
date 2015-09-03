from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)

if __name__ == "__main__":
    # import the api
    from complion.api import api_blueprint

    # register the api blueprint
    app.register_blueprint(api_blueprint)

    app.run()
