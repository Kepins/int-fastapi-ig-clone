import os
from typing import Union
from pathlib import Path

from fastapi import UploadFile

from .exceptions import WriteError


class FileRepository:
    def __init__(self, directory: Union[str, os.PathLike]):
        self.directory = directory

    def save_file(self, id: int, file: UploadFile):
        file_extension = Path(file.filename).suffix

        out_filepath = os.path.join(self.directory, f"{id}{file_extension}")
        try:
            with open(out_filepath, "wb") as output_file:
                # Move the cursor to the beginning of the SpooledTemporaryFile
                file.file.seek(0)

                # Write the contents to the output file
                output_file.write(file.file.read())
        except OSError as e:
            print(e)
            raise WriteError()



