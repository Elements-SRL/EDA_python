from typing import List
from src.metadata.meta_data import MetaData
from src.file_handlers.specific_handlers import abf_handler, edh_handler


def extract_data(files: List[str], metadata: MetaData):
    if metadata.already_opened(files):
        return
    if all(f.endswith(".abf") for f in files):
        if len(files) == 1:
            abf_handler.extract_meta_data_from_abf(files[0], metadata)
        else:
            abf_handler.extract_meta_data_from_multiple_abf(files, metadata)
    elif files[0].endswith(".edh"):
        edh_handler.extract_meta_data_from_edh(files[0], metadata)
    # TODO Remove this
    metadata.add_paths(files)

