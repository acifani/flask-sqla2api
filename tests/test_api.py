import unittest

from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy

from flask_sqla2api import SQLA2api

GOOD_ENTRY = {'id': 1, 'name': 'entry mcentryface'}


class ApiTests(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.db = SQLAlchemy(app)

        class Entry(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            name = self.db.Column(self.db.String(80))

        class Person(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            name = self.db.Column(self.db.String(80))

        api = SQLA2api([Entry, Person], self.db)
        api.append_blueprints(app)

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

    def test_get_one(self):
        self.client.post('/entry', data=GOOD_ENTRY)
        res = self.client.get('/entry/1')
        json_res = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertEqual(GOOD_ENTRY, json_res)

    def test_get_one_not_found(self):
        res = self.client.get('/entry/2')
        self.assertEqual(404, res.status_code)

    def test_post(self):
        res = self.client.post('/entry', data=GOOD_ENTRY)
        json_res = json.loads(res.data)

        self.assertEqual(201, res.status_code)
        self.assertEqual(GOOD_ENTRY, json_res)

    def test_put(self):
        self.client.post('/entry', data=GOOD_ENTRY)
        modified_entry = GOOD_ENTRY
        modified_entry['name'] = 'modified'
        res = self.client.put('/entry/1', data=modified_entry)
        json_res = json.loads(res.data)

        self.assertEqual(201, res.status_code)
        self.assertEqual(modified_entry, json_res)

    def test_put_not_found(self):
        res = self.client.put('/entry/2', data=GOOD_ENTRY)
        self.assertEqual(404, res.status_code)

    def test_delete(self):
        self.client.post('/entry', data=GOOD_ENTRY)
        res = self.client.delete('/entry/1')

        self.assertEqual(204, res.status_code)
        self.assertEqual(b'', res.data)

    def test_delete_not_found(self):
        res = self.client.delete('/entry/2')
        self.assertEqual(404, res.status_code)
