import numpy as np

from .base import DecisionEngine
from . import utils


class TopsisEngine(DecisionEngine):
    # Selected | 2016 diff | 2015 diff | Tuition fee | Ratio | Ranking score | Cutoff
    _WEIGHTS = [0.15, 0.2, 0.15, 0.1, 0.1, 0.25, 0.05]

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

        best_sstar_idx = utils.k_argmin(sstar, len(selected))
        best_sminus_idx = utils.k_argmax(sminus, len(selected))
        best_c_idx = utils.k_argmax(C, len(selected))

        best_sstar, db_sstar = [], []
        best_sminus, db_sminus = [], []
        best_c, db_c = [], []

        for sstar_idx, sminus_idx, c_idx in zip(best_sstar_idx, best_sminus_idx, best_c_idx):
            best_sstar.append(choices[sstar_idx])
            db_sstar.append((sstar_idx, choices[sstar_idx]))

            best_sminus.append(choices[sminus_idx])
            db_sminus.append((sminus_idx, choices[sminus_idx]))

            best_c.append(choices[c_idx])
            db_c.append((c_idx, choices[c_idx]))

        self._logger.debug('Best S*\n%s' % db_sstar)
        self._logger.debug('Best S-\n%s' % db_sminus)
        self._logger.debug('Best C\n%s' % db_c)

        schools = list(map(lambda x: x.school, best_c))
        notes = []

        return schools, notes
