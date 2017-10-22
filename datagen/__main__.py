from argparse import ArgumentParser
from pyregis import db
from pyregis.models import *

import random
import numpy as np

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
    parser.add_argument('--score-loc', dest='LOC', default=17.0, type=float,
                        help='The mean for exam score distribution.')
    parser.add_argument('--score-scale', dest='SCALE', default=6.0, type=float,
                        help='The standard deviation for exam score distribution.')

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
        db.db_session.add(m_major)

    db.db_session.commit()

    print('\nInserting %d schools...' % len(names.SCHOOLS))
    for i, school in enumerate(names.SCHOOLS):
        print('[%d] %s' % (i+1, school['name']))
        m_school = School(name=school['name'])
        db.db_session.add(m_school)
        for major in school['majors']:
            m_major = Major.query.filter_by(name=major['name']).first()
            cutoff = major['cutoff']
            m_sm = SchoolMajor(cutoff=cutoff)
            m_sm.major = m_major
            m_sm.school = m_school
            db.db_session.add(m_sm)

    db.db_session.commit()

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
        firstname = random.choice(tuple(first_cands))
        print('[%d] %s %s %s' % (i+1, lastname, middlename, firstname))

        # Random score drawn from normal distribution
        a_score = min(30.0, max(1.0, np.random.normal(args.LOC, args.SCALE)))
        d_score = min(30.0, max(1.0, np.random.normal(args.LOC, args.SCALE)))
        print('\tGroup A score: %.2f' % a_score)
        print('\tGroup D score: %.2f' % d_score)

        m_student = Student(firstname=firstname, lastname='%s %s' % (lastname, middlename),
                            a_score=a_score, d_score=d_score)
        db.db_session.add(m_student)

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
            m_school = School.query.filter_by(name=r['school']).first()
            m_major = Major.query.filter_by(name=r['major']).first()

            scid = m_school.scid
            mid = m_major.mid

            m_sm = SchoolMajor.query.filter_by(scid=scid, mid=mid).first()
            m_reg = Registration(school_major=m_sm, student=m_student)
            db.db_session.add(m_reg)

    db.db_session.commit()


if __name__ == '__main__':
    main(parse_arguments())
