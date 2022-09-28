import numpy as np
from numpy import ndarray


class BasicData:

    def __init__(self, ch: int, y: ndarray, sweep_number: int = -1, visible: bool = True):
        self.ch: int = ch
        self.y: ndarray = y
        self.visible: bool = visible
        self.sweep_number: int = sweep_number
        if sweep_number == -1:
            self.name = "ch " + str(ch)
        else:
            self.name = "ch " + str(ch) + " s " + str(sweep_number)

    def __hash__(self):
        return hash((self.ch, str(self.y), self.sweep_number, self.visible))

    def __eq__(self, other):
        return self.ch == other.ch and np.array_equal(self.y, other.y) and self.visible == other.visible and self.sweep_number == other.sweep_number
