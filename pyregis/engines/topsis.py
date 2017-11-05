import numpy as np

from .base import DecisionEngine


class TopsisEngine(DecisionEngine):
    _WEIGHTS = [0.1, 0.2, 0.1, 0.1, 0.1, 0.2]

    def __init__(self):
        super().__init__()

    def make_decision(self, student, **kwargs):
        major = student.major
        choices = major.schools
        selected = student.schools

        table = np.zeros((len(choices), len(self._WEIGHTS)))

        # Fill out table values
        for i, sc in enumerate(choices):
            sm = list(filter(lambda m: m.mid == major.mid, sc.majors))[0]

            # Whether school was already selected
            if sc in selected:
                table[i, 0] = 1.0
            # 2016 difference
            table[i, 1] = sm.diff_2016(student.scores)
            # 2015 difference
            table[i, 2] = sm.diff_2015(student.scores)
            # Tuition fee
            table[i, 3] = sc.fee
            # Compete ratio
            table[i, 4] = sc.ratio
            # School ranking score
            table[i, 5] = sc.rank

        # Reverse low properties
        table[:, 3] = np.max(table[:, 3]) - table[:, 3]
        table[:, 4] = np.max(table[:, 4]) - table[:, 4]

        # Vector normalize
        table = table / np.sqrt(np.sum(table ** 2, axis=0, keepdims=True))

        # Factor weights
        table = table * self._WEIGHTS

        # Summarize best/worst
        astar = np.max(table, axis=0)
        aminus = np.max(table, axis=0)

        # Calculate distance
        _astar = np.stack([astar] * np.size(table, 0))
        _aminus = np.stack([aminus] * np.size(table, 0))
        sstar = np.sqrt(np.sum(table ** 2 - _astar ** 2, axis=-1))
        sminus = np.sqrt(np.sum(table ** 2 - _aminus ** 2, axis=-1))

        # Calculate similarity index
        C = sminus / (sstar + sminus)

        print(sstar)
        print(sminus)
        print(C)
