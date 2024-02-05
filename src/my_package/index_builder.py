from result import Result, Ok, Err
from src.my_package import (
    record,
    directory_reader,
    input_error,
    error_logger,
)


class IndexBuilder():
    def __init__(self, error_logger: error_logger.ErrorLogger):
        self.index_header: str = "<INDEX>"
        self.index_body: list[record.Record] = []
        self.index_footer: str = "</INDEX>"
        error_logger = error_logger

    def add_records(
        self,
        file_data: list[directory_reader.FileData],
    ) -> Result[bool, Exception]:
        for file in file_data:
            try:
                rec = record.Record(file)
                self.index_body.append(rec)
            except input_error.InputError as e:
                error_logger.error_list.append(e)
                continue
            except Exception as e:
                return Err(e)
        return Ok(True)

    def save_index(self):
        ...
