from argparse import ArgumentParser

from . import names


def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('-c', '--count', type=int, default=10000, dest='COUNT',
                        help='The number of students to generate. Defaults to 10000.')
    parser.add_argument('--test', action='store_true', dest='TEST',
                        help='Toggles test mode, which only prints out data without affecting any database. '
                             'Overrides --clean.')
    parser.add_argument('--clean', action='store_true', dest='CLEAN',
                        help='Whether to delete all data before generating.')

    return parser.parse_args()


def main(args):
    print('Generating %d students ...' % args.COUNT)


if __name__ == '__main__':
    main(parse_arguments())
