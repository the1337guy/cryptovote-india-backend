# This code is explicitly in the public domain
from addict import Dict
from marshmallow import ValidationError


def make_error(code, err):
    return {'errored': True, 'code': code, 'errors': [err]}


def make_success(val):
    return {'errored': False, **val}


def ensure_valid(schema):
    def tmpfun(func):
        def tfun(obj):
            if not isinstance(obj, dict):
                return 'Go fuck yourself'
            s = schema()
            try:
                return func(Dict(s.load(obj)))
            except ValidationError as err:
                return {
                    'errored': True,
                    'errors': err.messages
                }
            pass

        return tfun
        pass

    return tmpfun
    pass
