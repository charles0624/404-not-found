# web server and database stuff
from flask import Flask, render_template, request
from pathlib import Path

from databased.db import db
from databased.models.Question import Question
from databased.models.DeckTag import DeckTag
from databased.models.Category import Category
from databased.models.Question_Tag_Relationship import Question_Decktag

# our html pages
# from api.routes import api_blueprint
from gui.routes import gui_blueprint


# name the app as the parent dir
APP_NAME = Path(__file__).stem
print(f"APP_NAME: {APP_NAME}")
app = Flask(APP_NAME)

# add access to the gui folder
app.register_blueprint(gui_blueprint)

# add access to the api folder
# app.register_blueprint(api_blueprint, url_prefix="/api")

# name the database as parentdir.db
APP_DB = f"{Path.cwd()}/databased/{APP_NAME}.db"
print(f"APP DATABASE: {APP_DB}")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{APP_DB}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# call this function when cleaning up
# app.teardown_appcontext(close_db)

# create database
db.init_app(app)
with app.app_context():
    db.create_all()

app.run(debug=True)
