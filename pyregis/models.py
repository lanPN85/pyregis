from sqlalchemy import Integer, String, Column, ForeignKey, Float
from sqlalchemy.orm import relationship

from .db import Model


class Student(Model):
    __tablename__ = 'students'
    sid = Column(Integer, primary_key=True)
    firstname = Column(String(64, convert_unicode=True))
    lastname = Column(String(128, convert_unicode=True))
    a_score = Column(Float)
    d_score = Column(Float)

    school_majors = relationship('Registration', back_populates='student')


class Registration(Model):
    __tablename__ = 'registrations'
    smid = Column(Integer, ForeignKey('school_majors.smid'), primary_key=True)
    sid = Column(Integer, ForeignKey('students.sid'), primary_key=True)

    school_major = relationship('SchoolMajor', back_populates='students')
    student = relationship('Student', back_populates='school_majors')


class SchoolMajor(Model):
    __tablename__ = 'school_majors'
    smid = Column(Integer, primary_key=True)
    scid = Column(Integer, ForeignKey('schools.scid'))
    mid = Column(Integer, ForeignKey('majors.mid'))
    cutoff = Column(Integer)

    students = relationship('Registration', back_populates='school_major')
    school = relationship('School', back_populates='majors')
    major = relationship('Major', back_populates='schools')


class Major(Model):
    __tablename__ = 'majors'
    mid = Column(Integer, primary_key=True)
    name = Column(String(128, convert_unicode=True))
    group = Column(String(2, convert_unicode=True))

    schools = relationship('SchoolMajor', back_populates='major')


class School(Model):
    __tablename__ = 'schools'
    scid = Column(Integer, primary_key=True)
    name = Column(String(256, convert_unicode=True))

    majors = relationship('SchoolMajor', back_populates='school')


