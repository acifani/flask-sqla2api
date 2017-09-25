import unittest
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_sqla2api import SQLA2api

GOOD_ENTRY = {'id': '1', 'name': 'entry mcentryface'}

class ApiTests(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.db = SQLAlchemy(app)

        class Entry(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            name = self.db.Column(self.db.String(80))

        api = SQLA2api(app, Entry, self.db)
        app.register_blueprint(api.make_blueprint(), url_prefix='/')

        self.db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def test_get_all(self):
        self.client.post('/entry', data=GOOD_ENTRY)
        res = self.client.get('/entry')
        json_res = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertEqual(1, len(json_res))
        self.assertEqual(GOOD_ENTRY, json_res[0])

    def test_post(self):
        res = self.client.post('/entry', data=GOOD_ENTRY)
        json_res = json.loads(res.data)

        self.assertEqual(201, res.status_code)
        self.assertEqual(GOOD_ENTRY, json_res)
