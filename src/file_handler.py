from src.data_classes.meta_data import MetaData
from src.handlers import abf_handler, edh_handler


def extract_data(f: str, metadata: MetaData):
    if metadata.already_opened(f):
        return
    if f.endswith(".abf"):
        abf_handler.extract_meta_data_from_abf(f, metadata)
        # case f.endswith(".edh"):
        #     edh_handler.extract_meta_data_from_edh(f, metadata)

