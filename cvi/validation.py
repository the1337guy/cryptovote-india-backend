from addict import Dict


def make_error(err):
    return {'errored': True, 'errors': [err]}


def make_success(val):
    return {'errored': False, 'goahead': True, 'obj': val}


def ensure_valid(schema):
    def tmpfun(func):
        def tfun(obj):
            if not isinstance(obj, dict):
                return 'Go fuck yourself'
            s = schema()
            res, errs = s.load(obj)
            print('Response: {}, Errors: {}'.format(res, errs))
            if len(errs) != 0:
                return {'errored': True, 'errors': errs}
            else:
                return func(Dict(res))
            pass

        return tfun
        pass

    return tmpfun
    pass
