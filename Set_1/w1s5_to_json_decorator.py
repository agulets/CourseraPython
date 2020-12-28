import functools
import json


def to_json(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        return json.dumps(func(*args, **kwargs))
    return wrapped


@to_json
def r():
    return {'test': 42}


if __name__ == '__main__':
    print(r.__name__)
    print(r())
