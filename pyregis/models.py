from sqlalchemy import Integer, String, Column, ForeignKey, Float
from sqlalchemy.orm import relationship

from .db import Model


class Student:
    def __init__(self, score, school_majors):
        self.score = score
        self.school_majors = school_majors


class SchoolMajor(Model):
    __tablename__ = 'school_majors'
    scid = Column(Integer, ForeignKey('schools.scid'), primary_key=True)
    mid = Column(Integer, ForeignKey('majors.mid'), primary_key=True)
    cutoff = Column(Integer)
    score_2016 = Column(Float)
    score_2014 = Column(Float)

    school = relationship('School', back_populates='majors')
    major = relationship('Major', back_populates='schools')


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
