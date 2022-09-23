import pyabf

from src.meta_data import MetaData
from abc import ABC, abstractmethod


class FileHandler(ABC):

    @abstractmethod
    def open(self, f: str) -> MetaData:
        match f:
            case f.endswith(".abf"):
                ABFHandler.open(f, self.incrementalID)
                self.incrementalID += 1
        pass


class ABFHandler(FileHandler):

    def open(self, f, id) -> MetaData:
        abf = pyabf.ABF(f)
        return MetaData()
