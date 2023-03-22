import numpy as np
from numpy import ndarray
import copy


class BasicData:

    def __init__(self, ch: int, y: ndarray, measuring_unit: str, file_path: str, name: str, axis: int,
                 sweep_number: int = 0, visible: bool = True):
        self.axis: int = axis
        self.ch: int = ch
        self.y: ndarray = y
        self.visible: bool = visible
        self.sweep_number: int = sweep_number
        self.measuring_unit = measuring_unit
        self.name = name
        self.filepath = file_path

    def set_ch(self, ch: int):
        self.ch = ch
        self.name = self.name + " ch " + str(self.ch)

    def __hash__(self):
        return hash(str(self.y))

    def __eq__(self, other):
        return np.array_equal(self.y, other.y)

    def __str__(self):
        return str(self.y) + " " + self.filepath


def copy_basic_data(bd: BasicData) -> BasicData:
    return copy.deepcopy(bd)
