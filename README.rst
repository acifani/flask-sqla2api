[WIP] Flask-sqla2api
=======================

Flask middleware that creates a simple Flask API CRUD REST endpoint
based on a SQLAlchemy model definition.

Basic usage
-------------

.. code-block:: python
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_sqla2api import SQLA2api

    # Init app and DB
    app = Flask(__name__)
    db = SQLAlchemy(app)

    # Setup a simple SQLAlchemy model
    class Entry(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(80))

    # Init Flask-sqla2api and register its blueprint
    api = SQLA2api(app, Entry, db)
    app.register_blueprint(api.make_blueprint(), url_prefix='/')

The previous tiny app will create the following endpoints

===============  =========== =======================
URL              HTTP Method Action
===============  =========== =======================
``/entry``       GET         Get all entries
``/entry``       POST        Create new entry
``/entry/<id>``  GET         Get a single entry
``/entry/<id>``  PUT         Edit existing entry
``/entry/<id>``  DELETE      Delete existing entry
===============  =========== =======================
