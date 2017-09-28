from flask import Blueprint, jsonify, request

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
        self._fields = self._model.__table__.columns.keys()
        self._fields_type = {}
        for column in self._model.__table__.columns:
            self._fields_type[column.name] = column.type.python_type
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
                    params[field] = self._cast(field, request.form.get(field))
                new_item = self._model(**params)

                # TODO: add try/except
                self._db.session.add(new_item)
                self._db.session.commit()

                response = jsonify(params)
                return response, 201

            else:
                # GET
                all_items = self._model.query.all()
                results = []
                for item in all_items:
                    entry = {}
                    for field in self._fields:
                        entry[field] = getattr(item, field)
                    results.append(entry)

                response = jsonify(results)
                return response, 200

        @self.blueprint.route(self._model_alias + '/<item_id>', methods=['GET', 'PUT', 'DELETE'])
        def item_methods(item_id):
            entry = self._model.query.get_or_404(item_id)

            if request.method == 'GET':
                result = {}
                for field in self._fields:
                    result[field] = getattr(entry, field)

                response = jsonify(result)
                return response, 200

            elif request.method == 'PUT':
                result = {}
                for field in self._fields:
                    value = self._cast(field, request.form[field])
                    setattr(entry, field, value)
                    result[field] = value
                self._db.session.commit()

                response = jsonify(result)
                return response, 201

            else:
                # DELETE
                self._db.session.delete(entry)
                self._db.session.commit()

                return '', 204

        return self.blueprint

    def _cast(self, field, value):
        if not self._fields_type:
            raise ValueError("Model not initialized")
        return (self._fields_type[field])(value)
