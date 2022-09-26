from src.data_classes.meta_data import MetaData
from src.handlers import abf_handler


def extract_data(f: str, metadata: MetaData):
    match f:
        case f.endswith(".abf"):
            abf_handler.extract_meta_data_from_abf(f, metadata)
