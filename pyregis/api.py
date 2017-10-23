import flask

from . import db
from . import app


def init():
    """
    Call this on server start
    """
    db.init_db()


@app.route('/api/students/search', methods=['GET'])
def search_students():
    try:
        query = flask.request.args['query']
    except KeyError:
        return flask.abort(400)


@app.route('/api/students/idsearch', methods=['GET'])
def student_by_id():
    try:
        sid = flask.request.args['id']
    except KeyError:
        return flask.abort(400)


@app.route('/api/schools/search', methods=['GET'])
def search_schools():
    try:
        query = flask.request.args['query']
    except KeyError:
        return flask.abort(400)


@app.route('/api/majors/search', methods=['GET'])
def search_majors():
    try:
        query = flask.request.args['query']
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
