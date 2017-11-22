from argparse import ArgumentParser
from flask import Flask
from logging import getLogger

import flask
from flask_cors import CORS
import logging

from pyregis import db
from pyregis.models import *
from pyregis.engines import TopsisEngine, ElectreEngine

app = Flask(__name__, template_folder='./dist', static_folder='./dist/static')


@app.route('/')
def index():
    return flask.render_template('index.html')


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('--port', dest='PORT', default=None)
    parser.add_argument('--host', dest='HOST', default=None)
    parser.add_argument('--debug', dest='DEBUG', action='store_true')
    return parser.parse_args()


def main(args):
    CORS(app, resources={r'/api/*': {'origins': '*'}})
    loglevel = logging.DEBUG if args.DEBUG else logging.INFO
    logging.basicConfig(level=loglevel, format='%(name)s:[%(levelname)s] %(message)s')

    try:
        init()
        app.run(host=args.HOST, port=args.PORT)
    finally:
        print()


_logger = None


def init():
    """
    Call this on server start
    """
    global _logger
    _logger = getLogger(__name__)
    _logger.debug('Initializing APIs...')
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
    except KeyError as e:
        _logger.error('Missing API argument', exc_info=True)
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
    'topsis': TopsisEngine(),
    'electre': ElectreEngine()
}


@app.route('/api/decide', methods=['POST'])
def get_decision():
    engine_name = flask.request.args.get('engine', 'topsis')
    if engine_name not in ENGINES.keys():
        flask.abort(404)

    engine = ENGINES[engine_name]
    st = flask.request.get_json()
    student = Student.from_dict(st)

    schools = engine.make_decision(student)
    # sdicts = list(map(lambda x: x.to_dict(include_majors=False), schools))
    sdicts = list(map(lambda x: x.to_dict(), schools))
    result = {
        'schools': sdicts,
    }

    return flask.jsonify(result)


if __name__ == '__main__':
    main(parse_arguments())
