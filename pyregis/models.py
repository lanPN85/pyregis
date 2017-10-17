from sqlalchemy import BigInteger, String, Column

from .db import Model


"""
Sử dụng SqlAlchemy để mapping đến SQLite.
Tất cả các class subclass theo Model, vd: class Student(Model).
"""


class Student(Model):
    __tablename__ = 'students'
    sid = Column(BigInteger, primary_key=True)
    firstname = Column(String(50, convert_unicode=True))
    lastname = Column(String(70, convert_unicode=True))

    def __init__(self, sid=None, firstname=None, lastname=None):
        self.sid = sid
        self.firstname = firstname
        self.lastname = lastname
