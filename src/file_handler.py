from os.path import exists
import pyabf


def open_abf(path_to_file: str):
    if not exists(path_to_file):
        return None
    if path_to_file.endswith(".abf"):
        return pyabf.ABF(path_to_file)

