import sys
sys.path.append('.')
import logging

from pyregis.engines import TopsisEngine
from pyregis.models import Student, School, Major

logging.basicConfig(level=logging.DEBUG, format='%(name)s:[%(levelname)s] %(message)s')

e = TopsisEngine()
m = Major.query.filter_by(name='CNTT-TT').first()
s1 = School.query.filter_by(name='Viện Đại học Mở Hà Nội').first()
s = Student({
    'math': 8, 'phys': 8, 'chem': 9.75,
    'lit': 6.75, 'eng': 8.25
}, m, [s1])
e.make_decision(s)
