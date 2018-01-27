from flask import request
from .models import Model


class SQLA2api(object):
    def __init__(self, app=None, model=None, db=None):
        if app is not None:
            self.init_app(app)
        if db is not None:
            self.init_db(db)
        if model is not None:
            self.init_model(model)

    def init_app(self, app):
        self.app = app

    def init_model(self, model):
        self.model = Model(model, self.db)

    def init_db(self, db):
        self.db = db

    def make_blueprint(self):
        if self.model is None:
            raise ValueError("Model not initiated.")
        return self.model.make_blueprint()
