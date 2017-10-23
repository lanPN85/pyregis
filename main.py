from argparse import ArgumentParser

import flask

from pyregis import app
from pyregis import api


@app.route('/')
def index():
    return flask.render_template('index.html')


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('--port', dest='PORT', default=None)
    parser.add_argument('--host', dest='HOST', default=None)
    return parser.parse_args()


def main(args):
    api.init()
    app.run(host=args.HOST, port=args.PORT)


if __name__ == '__main__':
    main(parse_arguments())
