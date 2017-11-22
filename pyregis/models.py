from sqlalchemy import Integer, String, Column, ForeignKey, Float
from sqlalchemy.orm import relationship

from .db import Model


class Student:
    def __init__(self, scores, major, schools):
        self.scores = scores
        self.major = major
        self.schools = schools

    @classmethod
    def from_dict(cls, d):
        scores = d['scores']
        major = Major.query.filter_by(mid=d['mid']).first()
        schools = []
        for scid in d['scids']:
            schools.append(School.query.filter_by(scid=scid).first())

        s = Student(scores, major, schools)
        return s

    def __repr__(self):
        return 'Student(scores = %s, major = \'%s\', schools = %s)' % \
               (self.scores, self.major.name, list(map(lambda x: x.name, self.schools)))


class SchoolMajor(Model):
    __tablename__ = 'school_majors'
    scid = Column(Integer, ForeignKey('schools.scid'), primary_key=True)
    mid = Column(Integer, ForeignKey('majors.mid'), primary_key=True)
    cutoff = Column(Integer)
    score_2016 = Column(Float)
    score_2015 = Column(Float)
    double_subj = Column(String(8), nullable=True)

    school = relationship('School', back_populates='majors')
    major = relationship('Major', back_populates='schools')

    def diff_2015(self, student_scores):
        return self._score_diff(student_scores, self.score_2015)

    def diff_2016(self, student_scores):
        return self._score_diff(student_scores, self.score_2016)

    def _score_diff(self, student_scores, standard_score):
        if self.major.group == 'A':
            scores = [student_scores['math'], student_scores['phys'], student_scores['chem']]
        elif self.major.group == 'D':
            scores = [student_scores['math'], student_scores['lite'], student_scores['eng']]
        else:
            raise ValueError('Invalid group %s' % self.major.group)

        total = sum(scores)
        if self.double_subj is not None:
            total += student_scores[self.double_subj]

        return min([total - standard_score, 2])

    def __repr__(self):
        return "SchoolMajor(school = '%s', major = '%s')" % (self.school.name, self.major.name)


class Major(Model):
    __tablename__ = 'majors'
    mid = Column(Integer, primary_key=True)
    name = Column(String(128, convert_unicode=True))
    group = Column(String(2, convert_unicode=True))

    schools = relationship('SchoolMajor', back_populates='major')

    def to_dict(self, include_schools=True):
        d = {
            'mid': self.mid,
            'name': self.name,
            'group': self.group
        }

        if include_schools:
            d['schools'] = []
            slist = self.schools
            for s in slist:
                school = s.school
                d['schools'].append({
                    'scid': school.scid,
                    'name': school.name,
                    'rank_score': school.rank_score,
                    'cutoff': s.cutoff,
                    'score_2016': s.score_2016,
                    'score_2015': s.score_2015,
                    'double_subj': s.double_subj,
                    'ratio': school.ratio
                })

        return d


class School(Model):
    __tablename__ = 'schools'
    scid = Column(Integer, primary_key=True)
    name = Column(String(256, convert_unicode=True))
    ratio = Column(Float)
    fee = Column(Float)
    rank_score = Column(Float)

    majors = relationship('SchoolMajor', back_populates='school')

    def to_dict(self, include_majors=True):
        d = {
            'scid': self.scid,
            'name': self.name,
            'ratio': self.ratio,
            'fee': self.fee,
            'rank_score': self.rank_score
        }

        if include_majors:
            d['majors'] = []
            mlist = self.majors
            for m in mlist:
                major = m.major
                d['majors'].append({
                    'mid': major.mid,
                    'name': major.name,
                    'cutoff': m.cutoff,
                    'group': major.group,
                    'score_2016': m.score_2016,
                    'score_2015': m.score_2015,
                    'double_subj': m.double_subj
                })

        return d
