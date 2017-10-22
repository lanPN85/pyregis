import flask

from . import db
from . import app

db.init_db()


def search_students(query):
    pass


def search_schools(query):
    pass


__SEARCH_MAP = {
    'students': search_students,
    'schools': search_schools,
}


@app.route('/api/<target>/search')
def search(target):
    try:
        query = flask.request.args['query']
        fn = __SEARCH_MAP.get(target, lambda q: flask.abort(404))
        return fn(query)
    except KeyError:
        return flask.abort(400)


