from flask import request
from .models import Model


class SQLA2api(object):
    def __init__(self, models=None, db=None):
        self.db = None
        self.models = []
        if db is not None:
            self.init_db(db)
        if models is not None:
            self.init_models(models)

    def init_models(self, models):
        self.models = []
        for model in models:
            self.models.append(Model(model, self.db))

    def init_db(self, db):
        self.db = db

    def append_blueprints(self, app):
        if app is None:
            raise ValueError("Cannot append to null app.")
        for model in self.models:
            app.register_blueprint(model.make_blueprint(), url_prefix='/')


def generate_blueprint(model, db):
    model = Model(model, db)
    return model.make_blueprint()
