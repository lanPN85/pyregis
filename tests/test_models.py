import unittest

from pyregis.models import Student


class TestStudent(unittest.TestCase):
    def test_fromdict(self):
        d = {
            'scores': {'math': 8.0, 'phys': 7.5, 'chem': 8.5},
            'mid': 3,
            'scids': [4, 2, 1]
        }
        st = Student.from_dict(d)
        self.assertDictEqual(st.scores, {'math': 8.0, 'phys': 7.5, 'chem': 8.5})
        self.assertEqual(st.major.mid, 3)
        self.assertListEqual(list(map(lambda x: x.scid, st.schools)), [4, 2, 1])


if __name__ == '__main__':
    unittest.main()
