from functools import wraps
from flask import request, jsonify
from marshmallow import ValidationError

def parse_with(schema, many=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = {}
            form_data = request.form
            if form_data:
                for key in form_data.keys():
                    if form_data.getlist(key) and len(form_data.getlist(key)) > 1:
                        data[key] = form_data.getlist(key)
                    else:
                        data[key] = form_data[key]
            else:
                data = request.get_json()
            try:
                entity = schema(many=many).load(data)
            except ValidationError as err:
                return jsonify(
                    error=True,
                    messages=err.messages
                ), 400
            return f(entity, *args, **kwargs)
        return decorated_function
    return decorator