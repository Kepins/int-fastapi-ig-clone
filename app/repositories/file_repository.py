import os
from typing import Union
from pathlib import Path

from fastapi import UploadFile

from .exceptions import WriteError, DeleteError, ReadError


class FileRepository:
    def __init__(self, directory: Union[str, os.PathLike]):
        self.directory = directory

    def _get_file_path(self, id, filename):
        return os.path.join(self.directory, f"{id}{Path(filename).suffix}")

    def save_file(self, id: int, file: UploadFile):
        out_filepath = self._get_file_path(id, file.filename)
        try:
            with open(out_filepath, "wb") as output_file:
                # Move the cursor to the beginning of the SpooledTemporaryFile
                file.file.seek(0)

                # Write the contents to the output file
                output_file.write(file.file.read())
        except OSError as e:
            print(e)
            raise WriteError()

    def get_file_path(self, id: int):
        path = Path(self.directory)
        for file_path in path.glob("*"):
            if file_path.stem == str(id):
                return file_path
        raise ReadError()

    def delete_file(self, id: int):
        path = Path(self.directory)
        for file_path in path.glob("*"):
            if file_path.stem == str(id):
                try:
                    os.remove(file_path)
                except OSError as e:
                    raise DeleteError()
                return
        raise DeleteError()
