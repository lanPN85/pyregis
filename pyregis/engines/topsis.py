import numpy as np

from .base import TableBasedEngine
from . import utils


class TopsisEngine(TableBasedEngine):
    def __init__(self):
        super().__init__()

    def make_decision(self, student, candidates=None, **kwargs):
        major = student.major
        selected = student.schools
        choices = major.schools if candidates is None else candidates

        table = self.get_feature_table(student, choices)

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
        _divisor = np.clip(sstar + sminus, a_min=np.finfo(float).eps,
                           a_max=float('inf'))
        C = sminus / _divisor
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

        # schools = list(map(lambda x: x.school, best_c))
        schools = best_c

        return schools
