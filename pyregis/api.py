import flask

from . import db
from . import app
from .models import *
from .engines import TopsisEngine


def init():
    """
    Call this on server start
    """
    db.init_db()


@app.route('/api/schools/search', methods=['GET'])
def search_schools():
    try:
        query = flask.request.args['query'].strip()
        limit = flask.request.args.get('limit', None)

        dbq = db.db_session.query(School).filter(School.name.like('%' + query + '%'))
        if limit is not None:
            dbq.limit(int(limit))
        results = dbq.all()

        l = []
        for r in results:
            l.append(r.to_dict())
        return flask.jsonify(l)
    except KeyError:
        return flask.abort(400)


@app.route('/api/majors/search', methods=['GET'])
def search_majors():
    try:
        query = flask.request.args['query'].strip()
        limit = flask.request.args.get('limit', None)

        dbq = db.db_session.query(Major).filter(Major.name.like('%' + query + '%'))
        if limit is not None:
            dbq.limit(int(limit))
        results = dbq.all()

        l = []
        for r in results:
            l.append(r.to_dict())
        return flask.jsonify(l)
    except KeyError:
        return flask.abort(400)


@app.route('/api/schools/all', methods=['GET'])
def get_all_schools():
    dbq = db.db_session.query(School)
    results = dbq.all()

    l = []
    for r in results:
        l.append(r.to_dict())
    return flask.jsonify(l)


@app.route('/api/majors/all', methods=['GET'])
def get_all_majors():
    dbq = db.db_session.query(Major)
    results = dbq.all()

    l = []
    for r in results:
        l.append(r.to_dict())
    return flask.jsonify(l)


ENGINES = {
    'topsis': TopsisEngine()
}


@app.route('/api/decide', methods=['POST'])
def get_decision():
    pass
