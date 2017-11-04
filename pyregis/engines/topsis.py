from .base import DecisionEngine
from ..models import Student


class TopsisEngine(DecisionEngine):
    def __init__(self):
        super().__init__()

    def make_decision(self, student: Student, **kwargs):
        pass
