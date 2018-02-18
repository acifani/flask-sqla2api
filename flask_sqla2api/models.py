from flask import Blueprint, jsonify, request


class Model(object):
    def __init__(self, model=None, db=None):
        self.model = None
        self.db = None
        if model is not None:
            self.init_model(model)
        if db is not None:
            self.init_db(db)

    def init_db(self, db):
        self.db = db

    def init_model(self, model):
        if model is None:
            raise ValueError("Invalid value None for model init")
        self.model = model
        self.alias = str(model.__table__)
        self.fields = model.__table__.columns.keys()
        self.fields_type = {}
        for column in model.__table__.columns:
            self.fields_type[column.name] = column.type.python_type

    def make_blueprint(self):
        if self.model is None or self.db is None:
            raise ValueError("Model or db not initiated.")
        blueprint = Blueprint(self.alias, __name__)

        @blueprint.route(self.alias, methods=['GET', 'POST'])
        def collection_methods():
            if request.method == 'POST':
                data = self.get_data(request)
                if data is None:
                    return "Unsupported media type", 415
                return self.post(data)
            else:
                return self.get_all()

        @blueprint.route(self.alias + '/<item_id>', methods=['GET', 'PUT', 'DELETE'])
        def resource_methods(item_id):
            entry = self.model.query.get_or_404(item_id)
            if request.method == 'GET':
                return self.get(entry)
            elif request.method == 'PUT':
                data = self.get_data(request)
                if data is None:
                    return "Unsupported media type", 415
                return self.put(data, entry)
            else:
                return self.delete(entry)

        return blueprint

    def post(self, data):
        params = {}
        for field in self.fields:
            params[field] = self.cast(field, data[field])
        new_item = self.model(**params)
        # TODO: add try/except
        self.db.session.add(new_item)
        self.db.session.commit()

        return jsonify(params), 201

    def get_all(self):
        all_items = self.model.query.all()
        results = []
        for item in all_items:
            entry = {}
            for field in self.fields:
                entry[field] = getattr(item, field)
            results.append(entry)

        return jsonify(results), 200

    def get(self, entry):
        result = {}
        for field in self.fields:
            result[field] = getattr(entry, field)

        return jsonify(result), 200

    def put(self, data, entry):
        result = {}
        for field in self.fields:
            value = self.cast(field, data[field])
            setattr(entry, field, value)
            result[field] = value
        self.db.session.commit()

        return jsonify(result), 201

    def delete(self, entry):
        self.db.session.delete(entry)
        self.db.session.commit()
        return '', 204

    def cast(self, field, value):
        if not self.fields_type:
            raise ValueError("Model not initialized")
        if value is None:
            raise ValueError(
                "Expected value but found None for field: %s" % field)
        return (self.fields_type[field])(value)

    def get_data(self, request):
        if "multipart/form-data" in request.content_type:
            return request.form.to_dict()
        if request.content_type == "application/json":
            return request.get_json()
        return
