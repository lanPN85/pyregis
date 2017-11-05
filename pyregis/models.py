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
        pass


class SchoolMajor(Model):
    __tablename__ = 'school_majors'
    scid = Column(Integer, ForeignKey('schools.scid'), primary_key=True)
    mid = Column(Integer, ForeignKey('majors.mid'), primary_key=True)
    cutoff = Column(Integer)
    score_2016 = Column(Float)
    score_2015 = Column(Float)
    double_subj = Column(String(8))

    school = relationship('School', back_populates='majors')
    major = relationship('Major', back_populates='schools')

    def diff_2015(self, student_scores):
        return self._score_diff(student_scores, self.score_2015, self.major.group, double=self.double_subj)

    def diff_2016(self, student_scores):
        return self._score_diff(student_scores, self.score_2016, self.major.group, double=self.double_subj)

    @staticmethod
    def _score_diff(student_scores, standard_score, group, double=None):
        if group == 'A':
            scores = [student_scores['math'], student_scores['phys'], student_scores['chem']]
        elif group == 'D':
            scores = [student_scores['math'], student_scores['lite'], student_scores['eng']]
        else:
            raise ValueError('Invalid group %s' % group)

        total = sum(scores)
        if double is not None:
            total += student_scores[double]

        return total - standard_score


class Major(Model):
    __tablename__ = 'majors'
    mid = Column(Integer, primary_key=True)
    name = Column(String(128, convert_unicode=True))
    group = Column(String(2, convert_unicode=True))

    schools = relationship('SchoolMajor', back_populates='major')

    def to_dict(self, include_schools=True):
        d = {
            'mid': self.mid,
            'name': self.name
        }

        if include_schools:
            d['schools'] = []
            slist = self.schools
            for s in slist:
                school = s.school
                d['schools'].append({
                    'scid': school.scid,
                    'name': school.name,
                    'cutoff': s.cutoff
                })

        return d


class School(Model):
    __tablename__ = 'schools'
    scid = Column(Integer, primary_key=True)
    name = Column(String(256, convert_unicode=True))
    ratio = Column(Float)

    majors = relationship('SchoolMajor', back_populates='school')

    def to_dict(self, include_majors=True):
        d = {
            'scid': self.scid,
            'name': self.name
        }

        if include_majors:
            d['majors'] = []
            mlist = self.majors
            for m in mlist:
                major = m.major
                d['majors'].append({
                    'mid': major.mid,
                    'name': major.name,
                    'cutoff': m.cutoff
                })

        return d
