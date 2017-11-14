from logging import getLogger

import numpy as np


class DecisionEngine:
    def __init__(self):
        np.set_printoptions(precision=4, suppress=True)
        self._logger = getLogger(__name__)

    def make_decision(self, student, **kwargs):
        pass
