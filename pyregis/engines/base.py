from logging import getLogger

import numpy as np


class DecisionEngine:
    def __init__(self):
        np.set_printoptions(precision=4, suppress=True)
        self._logger = getLogger(__name__)

    def make_decision(self, student, **kwargs):
        pass


class TableBasedEngine(DecisionEngine):
    # Selected | 2016 diff | 2015 diff | Tuition fee | Ratio | Ranking score | Cutoff
    _WEIGHTS = [0.15, 0.2, 0.15, 0.1, 0.1, 0.25, 0.05]

    def __init__(self):
        super().__init__()

    @property
    def weights(self):
        return self._WEIGHTS

    def get_feature_table(self, student, choices):
        major = student.major
        selected = student.schools

        table = np.zeros((len(choices), len(self._WEIGHTS)))

        # Fill out table values
        for i, sm in enumerate(choices):
            # sm = list(filter(lambda m: m.mid == major.mid, sc.majors))[0]
            sc = sm.school

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
            table[i, 5] = sc.rank_score
            # Cutoff
            table[i, 6] = sm.cutoff
        self._logger.debug('Initial state:\n%s' % table)

        # Reverse low properties
        table[:, 3] = np.max(table[:, 3]) - table[:, 3]
        table[:, 4] = np.max(table[:, 4]) - table[:, 4]

        # Vector normalize
        _divisor = np.clip(np.sqrt(np.sum(table ** 2, axis=0, keepdims=True)),
                           a_min=np.finfo(float).eps, a_max=float('inf'))
        table = table / _divisor
        del _divisor
        self._logger.debug('Normalized:\n%s' % table)

        # Factor weights
        table = table * self._WEIGHTS
        self._logger.debug('Weighted:\n%s' % table)
        return table
