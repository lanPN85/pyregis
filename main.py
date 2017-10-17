from argparse import ArgumentParser
from flask import Flask

import flask

from pyregis import api

app = Flask(__name__)


@app.route('/')
def index():
    return flask.render_template('index.html')


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('--port', dest='PORT', default=None)
    parser.add_argument('--host', dest='HOST', default=None)
    return parser.parse_args()


def main(args):
    app.run(host=args.HOST, port=args.PORT)


if __name__ == '__main__':
    main(parse_arguments())
