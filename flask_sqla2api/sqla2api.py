from flask import Blueprint, jsonify, request, abort

class SQLA2api(object):
    def __init__(self, app=None, model=None, db=None):
        if app is not None:
            self.init_app(app)
        if model is not None:
            self.init_model(model)
        if db is not None:
            self.init_db(db)

    def init_app(self, app):
        self._app = app

    def init_model(self, model):
        self._model = model
        self._model_alias = str(self._model.__table__)
        self._fields = self._model.__table__.columns._data.keys()
        self.blueprint = Blueprint(self._model_alias, __name__)

    def init_db(self, db):
        self._db = db

    def make_blueprint(self):
        if self._app is None or self._model is None or self._db is None:
            raise ValueError("App, Model or db not initiated.")

        @self.blueprint.route(self._model_alias, methods=['GET', 'POST'])
        def collection_methods():
            if request.method == 'POST':
                params = {}
                for field in self._fields:
                    params[field] = request.form[field]
                new_item = self._model(**params)

                # TODO: add try/except
                self._db.session.add(new_item)
                self._db.session.commit()

                response = jsonify(params)
                response.status_code = 201
                return response

            else:
                all_items = self._model.query.all()
                results = []
                for item in all_items:
                    entry = {}
                    for field in self._fields:
                        entry[field] = str(getattr(item, field)) # item[field]
                    results.append(entry)

                response = jsonify(results)
                response.status_code = 200
                return response

        return self.blueprint
