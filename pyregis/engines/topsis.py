import numpy as np

from .base import DecisionEngine


class TopsisEngine(DecisionEngine):
    _WEIGHTS = [0.15, 0.25, 0.15, 0.15, 0.1, 0.2]

    def __init__(self):
        super().__init__()

    def make_decision(self, student, candidates=None, **kwargs):
        major = student.major
        selected = student.schools
        choices = major.schools if candidates is None else candidates

        table = np.zeros((len(choices), len(self._WEIGHTS)))

        # Fill out table values
        for i, sm in enumerate(choices):
            # sm = list(filter(lambda m: m.mid == major.mid, sc.majors))[0]
            sc = sm.school

            # Whether school was already selected
            if sc in selected:
                table[i, 0] = 1.0
            # 2016 difference
            table[i, 1] = sm.diff_2015(student.scores)
            # 2015 difference
            table[i, 2] = sm.diff_2014(student.scores)
            # Tuition fee
            table[i, 3] = sc.fee
            # Compete ratio
            table[i, 4] = sc.ratio
            # School ranking score
            table[i, 5] = sc.rank_score

        self._logger.debug('Initial state:\n%s' % table)

        # Reverse low properties
        table[:, 3] = np.max(table[:, 3]) - table[:, 3]
        table[:, 4] = np.max(table[:, 4]) - table[:, 4]

        # Vector normalize
        _divisor = np.clip(np.sqrt(np.sum(table ** 2, axis=0, keepdims=True)),
                           a_min=np.finfo(float).eps, a_max=float('inf'))
        table = table / _divisor
        self._logger.debug('Normalized:\n%s' % table)

        # Factor weights
        table = table * self._WEIGHTS
        self._logger.debug('Weighted:\n%s' % table)

        # Summarize best/worst
        astar = np.max(table, axis=0)
        aminus = np.min(table, axis=0)
        self._logger.debug('A*\n%s' % astar)
        self._logger.debug('A-\n%s' % aminus)

        # Calculate distance
        _astar = np.stack([astar] * np.size(table, 0))
        _aminus = np.stack([aminus] * np.size(table, 0))
        sstar = np.sqrt(np.sum((table - _astar) ** 2, axis=-1))
        sminus = np.sqrt(np.sum((table - _aminus) ** 2, axis=-1))
        self._logger.debug('S*\n%s' % sstar)
        self._logger.debug('S-\n%s' % sminus)

        # Calculate similarity index
        C = sminus / (sstar + sminus)
        self._logger.debug('C\n%s' % C)

        best_sstar = choices[np.argmin(sstar)]
        best_sminus = choices[np.argmax(sminus)]
        best_c = choices[np.argmax(C)]
        self._logger.debug('Best S* [%d]\n%s' % (int(np.argmin(sstar)), best_sstar))
        self._logger.debug('Best S- [%d]\n%s' % (int(np.argmax(sminus)), best_sminus))
        self._logger.debug('Best C [%d]\n%s' % (int(np.argmax(C)), best_c))

