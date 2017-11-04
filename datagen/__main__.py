from argparse import ArgumentParser
from pyregis import db
from pyregis.models import *

from . import names


def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('--test', action='store_true', dest='TEST',
                        help='Toggles test mode, which only prints out data without affecting any database. '
                             'Overrides --clean.')
    parser.add_argument('--clean', action='store_true', dest='CLEAN',
                        help='Whether to delete all data before generating.')

    return parser.parse_args()


def main(args):
    if not args.TEST and args.CLEAN:
        db.clear_db()
    elif not args.TEST:
        db.init_db()

    print('Inserting %d majors...' % len(names.MAJORS))
    for i, major in enumerate(names.MAJORS):
        print('[%d] %s' % (i+1, major['name']))
        print('\tGroup: %s' % major['group'])
        m_major = Major(name=major['name'], group=major['group'])
        if not args.TEST:
            db.db_session.add(m_major)

    if not args.TEST:
        db.db_session.commit()

    print('\nInserting %d schools...' % len(names.SCHOOLS))
    for i, school in enumerate(names.SCHOOLS):
        print('[%d] %s' % (i+1, school['name']))
        m_school = School(name=school['name'])
        if not args.TEST:
            db.db_session.add(m_school)
        for major in school['majors']:
            m_major = Major.query.filter_by(name=major['name']).first()
            cutoff = major['cutoff']
            m_sm = SchoolMajor(cutoff=cutoff)
            m_sm.major = m_major
            m_sm.school = m_school
            if not args.TEST:
                db.db_session.add(m_sm)

    if not args.TEST:
        db.db_session.commit()


if __name__ == '__main__':
    main(parse_arguments())
