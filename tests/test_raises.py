import unittest

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_sqla2api import SQLA2api, generate_blueprint


class RaisesTest(unittest.TestCase):
    def setUp(self):
        self.api = SQLA2api()
        self.app = Flask(__name__)

    def test__append_blueprints__no_app__throws(self):
        with self.assertRaises(ValueError):
            self.api.append_blueprints(None)

    def test__generate_blueprint__no_model__throws(self):
        db = SQLAlchemy(self.app)
        with self.assertRaises(ValueError):
            generate_blueprint(None, db)

    def test__generate_blueprint__no_db__throws(self):
        db = SQLAlchemy(self.app)

        class TestModel(db.Model):
            id = db.Column(db.Integer, primary_key=True)

        with self.assertRaises(ValueError):
            generate_blueprint(TestModel, None)
