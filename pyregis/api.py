from sqlalchemy import text

import flask

from . import db
from . import app
from .models import *


def init():
    """
    Call this on server start
    """
    db.init_db()


@app.route('/api/students/search', methods=['GET'])
def search_students():
    try:
        query = flask.request.args['query'].strip()
        limit = flask.request.args.get('limit', None)

        dbq = db.db_session.query(Student).filter(text('lastname || " " || firstname like "%' + query + '%"'))
        if limit is not None:
            dbq.limit(int(limit))
        results = dbq.all()
        if limit is not None:
            results = results[:int(limit)]

        l = []
        for r in results:
            l.append(r.to_dict())
        return flask.jsonify(l)
    except KeyError:
        return flask.abort(400)


@app.route('/api/students/idsearch', methods=['GET'])
def student_by_id():
    try:
        sid = flask.request.args['id']
        result = Student.query.filter_by(sid=sid).first()

        if result is None:
            return flask.jsonify(None)
        else:
            return flask.jsonify(result.to_dict())
    except KeyError:
        return flask.abort(400)


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


@app.route('/api/students/all', methods=['GET'])
def get_all_students():
    start_id = flask.request.args.get('start', 1)
    count = flask.request.args.get('count', 20)


@app.route('/api/schools/all', methods=['GET'])
def get_all_schools():
    pass


@app.route('/api/majors/all', methods=['GET'])
def get_all_majors():
    pass
