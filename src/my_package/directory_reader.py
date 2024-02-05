import re
import os
from glob import glob
from typing import NamedTuple
from result import Result, Ok, Err
from src.my_package import input_error, error_logger


class FileData(NamedTuple):
    full_path: str
    document_type: str
    employee_number: str


class DirectoryReader():
    def __init__(
        self,
        pickup_files_path: str,
        pickup_archive_path: str,
        dropoff_index_path: str,
        dropoff_files_path: str,
        target_file_extensions: list[str],
        error_logger: error_logger.ErrorLogger,
    ):
        self.files: list[str] = []
        self.file_data: list[FileData] = []
        self.pickup_files_path = pickup_files_path
        self.pickup_archive_path = pickup_archive_path
        self.dropoff_index_path = dropoff_index_path
        self.dropoff_files_path = dropoff_files_path
        self.target_file_extensions = target_file_extensions
        error_logger = error_logger

    def read_files(self) -> Result[bool, Exception]:
        """Collects filenames from pickup_files_path
        matching target_file_extensions"""
        try:
            for extention in self.target_file_extensions:
                self.files.extend(glob(os.path.join(
                    self.pickup_files_path,
                    "*." + extention
                )))
            return Ok(bool(len(self.files)))
        except Exception as e:
            return Err(e)

    def parse_file_name(self, full_path) -> Result[FileData, Exception]:
        file_name = full_path.split("/")[-1]
        if file_name.count('_') != 2:
            return Err(input_error.InputError(
                Exception(
                    f"""Not enough underscores. Found {
                        file_name.count('_')
                    }, expected 2
                    """
                ),
                full_path,
            ))
        pattern = re.compile(
            r"[A-Z,a-z]{1,3}_[0-9]{1,6}_[A-Z,a-z]{2}\.[A-Z,a-z]{1,4}"
        )
        if not pattern.match(file_name):
            return Err(input_error.InputError(
                Exception(
                    f"""File name did not conform to convention.
                    Found {file_name}. Expected
                    DOCTYPE_EMPLOEENUMBER_INITIALS.EXTENSION
                    doctype:alpha:1-3
                    employeenumber:numeric:1-6
                    initials:alpha:2
                    extension:alphanumeric:1-4
                    """
                ),
                full_path,
            ))
        try:
            file_data = FileData(
                full_path,
                *file_name.split("_")[:2]
            )
            return Ok(file_data)
        except Exception as e:
            return Err(input_error.InputError(
                e, full_path
            ))

    def parse_file_names(self) -> Result[bool, Exception]:
        for full_path in self.files:
            match self.parse_file_name(full_path):
                case Ok(value):
                    self.file_data.append(value)
                case Err(e):
                    if isinstance(e, input_error.InputError):
                        error_logger.error_list.append(e)
                        continue
        return Ok(bool(len(self.file_data)))
