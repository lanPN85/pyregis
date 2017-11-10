import sys
sys.path.append('.')
import logging

from pyregis.engines import TopsisEngine
from pyregis.models import Student, School, Major

logging.basicConfig(level=logging.DEBUG, format='%(name)s:[%(levelname)s] %(message)s')

e = TopsisEngine()
m = Major.query.filter_by(name='CNTT-TT').first()
s1 = School.query.filter_by(name='Đại học Bách Khoa Hà Nội').first()
s2 = School.query.filter_by(name='Học Viện Công Nghệ Bưu Chính Viễn Thông').first()

s = Student({
    'math': 10, 'phys': 8, 'chem': 7,
    'lit': 6.75, 'eng': 8.25
}, m, [s1, s2])

e.make_decision(s)
