from argparse import ArgumentParser

import flask
import logging

from pyregis import app
from pyregis import api


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
    loglevel = logging.DEBUG if args.DEBUG else logging.INFO
    logging.basicConfig(level=loglevel, format='%(name)s:[%(levelname)s] %(message)s')

    try:
        api.init()
        app.run(host=args.HOST, port=args.PORT)
    finally:
        print()


if __name__ == '__main__':
    main(parse_arguments())
