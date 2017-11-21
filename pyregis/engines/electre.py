import numpy as np

from .base import TableBasedEngine


class ElectreEngine(TableBasedEngine):
    # Selected | 2016 diff | 2015 diff | Tuition fee | Ratio | Ranking score | Cutoff
    _WEIGHTS = np.asarray([0.15, 0.2, 0.15, 0.1, 0.1, 0.25, 0.05])

    def __init__(self):
        super().__init__()

    def make_decision(self, student, candidates=None, **kwargs):
        major = student.major
        selected = student.schools
        choices = major.schools if candidates is None else candidates

        table = self.get_feature_table(student, choices)

        # Valid & invalid sets
        valids = [[]] * len(choices)
        invalids = [[]] * len(choices)
        for i in range(len(choices)):
            for j in range(len(choices)):
                valids[i] = valids[i].copy() + [[]]
                invalids[i] = invalids[i].copy() + [[]]
                if j == i:
                    continue
                for k in range(len(self._WEIGHTS)):
                    if table[i, k] >= table[j, k]:
                        valids[i][j] = valids[i][j].copy() + [k]
                        # self._logger.debug('%s' % valids)
                    else:
                        invalids[i][j] = invalids[i][j].copy() + [k]
        self._logger.debug('Valid sets:\n%s' % valids)
        self._logger.debug('Invalid sets:\n%s' % invalids)

        # Valid & invalid index
        valid_idx = np.zeros((len(choices), len(choices)))
        invalid_idx = np.zeros((len(choices), len(choices)))
        for i in range(len(choices)):
            for j in range(len(choices)):
                if j == i:
                    continue
                _valids = valids[i][j]
                valid_idx[i, j] = np.sum(self._WEIGHTS[_valids])

                _invalids = invalids[i][j]
                _total = np.sum(np.abs(table[i, :] - table[j, :]))
                if _total == 0:
                    _total = np.finfo(float).eps
                _intotal = np.sum(np.abs(table[i, _invalids] - table[j, _invalids]))
                invalid_idx[i, j] = _intotal / _total
        self._logger.debug('Valid indices:\n%s' % valid_idx)
        self._logger.debug('Invalid indices:\n%s' % invalid_idx)

        # Average
        valid_avg = np.sum(valid_idx) / (len(choices) ** 2 - len(choices))
        invalid_avg = np.sum(invalid_idx) / (len(choices) ** 2 - len(choices))
        self._logger.debug('Mean valid index:\n%s' % valid_avg)
        self._logger.debug('Mean invalid index:\n%s' % invalid_avg)

        # Select K
        adv = np.logical_and(valid_idx > valid_avg, invalid_idx < invalid_avg)
        is_adv = np.sum(adv, axis=0)
        K = []
        for i, val in enumerate(is_adv):
            if val == 0:
                K.append(i)
        self._logger.debug('Advantages:\n%s' % adv)

        notes = []
        schools = []
        sdb = []
        for k in K:
            schools.append(choices[k].school)
            sdb.append((k, choices[k]))
        self._logger.debug('Choices:\n%s' % sdb)

        return schools, notes
