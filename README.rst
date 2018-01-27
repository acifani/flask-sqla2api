Flask-sqla2api
==============

.. image:: https://travis-ci.org/acifani/flask-sqla2api.svg?branch=master
    :target: https://travis-ci.org/acifani/flask-sqla2api


Flask middleware that creates a simple Flask API CRUD REST endpoint
based on a SQLAlchemy model definition.

Basic usage
-----------

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

    # Init Flask-sqla2api
    api = SQLA2api([Entry], self.db)
    api.append_blueprints(app)

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

Generate single blueprint
-------------------------

If you want more control over your blueprints you can generate it
and append it yourself to your app.

.. code-block:: python

    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_sqla2api import generate_blueprint

    # Init app and DB
    app = Flask(__name__)
    db = SQLAlchemy(app)

    # Setup a simple SQLAlchemy model
    class Entry(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(80))

    # Generate and register blueprint
    blueprint = generate_blueprint(Entry, db)
    app.register_blueprint(blueprint, url_endpoint='/')

To-Do
-----

- Input validation
- API docs generation
