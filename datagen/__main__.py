from argparse import ArgumentParser

import random

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
    print('Inserting %d majors...')
    for i, major in enumerate(names.MAJORS):
        print('[%d] %s' % (i+1, major['name']))
        print('\tGroup: %s' % major['group'])

    print('\nInserting %d schools...')
    for i, school in enumerate(names.SCHOOLS):
        print('[%d] %s' % (i+1, school['name']))

    print('\nGenerating %d students...' % args.COUNT)
    for i in range(args.COUNT):
        lastname = random.choice(tuple(names.LAST_NAMES))

        mid_cands = names.MIDDLE_NAMES.copy()
        if lastname in mid_cands:
            mid_cands.remove(lastname)
        middlename = random.choice(tuple(mid_cands))

        first_cands = mid_cands.copy()
        if middlename in first_cands:
            first_cands.remove(middlename)
        firsname = random.choice(tuple(first_cands))
        print('[%d] %s %s %s' % (i+1, lastname, middlename, firsname))

        reg_num = random.randint(1, 3)
        regs = []
        school_cand = names.SCHOOLS.copy()
        for j in range(reg_num):
            r = {}
            school = random.choice(school_cand)
            r['school'] = school['name']
            r['major'] = random.choice(school['majors'])['name']
            regs.append(r)
            school_cand.remove(school)

        for r in regs:
            print('\t%s: %s' % (r['school'], r['major']))


if __name__ == '__main__':
    main(parse_arguments())
