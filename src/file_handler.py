from os.path import exists
import pyabf
from pyabf import ABF


def open_abf(path_to_file: str) -> ABF | None:
    if not exists(path_to_file):
        return None
    if path_to_file.endswith(".abf"):
        return pyabf.ABF(path_to_file)

