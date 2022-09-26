from numpy import ndarray


class BasicData:

    def __init__(self, ch: int, y: ndarray, visible: bool = True):
        self.ch: int = ch
        self.y: ndarray = y
        self.visible: bool = visible
