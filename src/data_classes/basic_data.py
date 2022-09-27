from numpy import ndarray


class BasicData:

    def __init__(self, ch: int, y: ndarray, path: str, sweep_number: int = -1, visible: bool = True):
        self.ch: int = ch
        self.y: ndarray = y
        self.visible: bool = visible
        self.path = path
        if sweep_number == -1:
            self.name = "ch " + str(ch)
        else:
            self.name = "ch " + str(ch) + " s " + str(sweep_number)

