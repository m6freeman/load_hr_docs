import shutil
import os
import pytest
from my_package.index_builder import IndexBuilder
from src.my_package import (
    settings,
    input_error,
    error_logger,
    directory_reader,
    index_builder,
    record
)


class TestMyModule:
    def setup_method(self):
        """Assemble common resources to be acted upon"""
        try:
            shutil.rmtree(
                "/home/matt/dev/python/tests/load_hr_docs/tests/mock/"
            )
        except Exception:
            pass
        shutil.copytree(
            "/home/matt/dev/python/tests/load_hr_docs/tests/.mock/",
            "/home/matt/dev/python/tests/load_hr_docs/tests/mock",
        )
        self.error_logger = error_logger.ErrorLogger()
        self.dir_reader = directory_reader.DirectoryReader(
            settings.PICKUP_FILES_PATH,
            settings.PICKUP_ARCHIVE_PATH,
            settings.DROPOFF_INDEX_PATH,
            settings.DROPOFF_FILES_PATH,
            settings.TARGET_FILE_EXTENSIONS,
            self.error_logger,
        )
        self.index_builder = index_builder.IndexBuilder(self.error_logger)

    def test_inputerror(self):
        with pytest.raises(input_error.InputError):
            raise input_error.InputError(Exception(), "/path/to/file.jpg")

    def test_connects_to_pickup_server(self):
        assert os.path.isdir(self.dir_reader.pickup_files_path)

    def test_connects_to_dropoff_server(self):
        assert os.path.isdir(self.dir_reader.dropoff_index_path)

    # directory reader
    def test_reads_in_files_from_directory(self):
        self.dir_reader.read_files()
        assert self.dir_reader.files

    def test_parses_correct_filename_structure(self):
        self.dir_reader.read_files()
        self.dir_reader.parse_file_names()
        assert self.dir_reader.file_data[0].document_type == "OTH"

    def test_raises_inputerror_on_incorrect_filename_structure(self):
        result = self.dir_reader.parse_file_name(
            "/test/OTH_423jl4_mf.jpg"
        )
        with pytest.raises(input_error.InputError):
            raise result.unwrap_err()

    # index builder
    def test_validates_data_against_database(self):
        self.dir_reader.read_files()
        self.dir_reader.parse_file_names()
        assert record.Record(self.dir_reader.file_data[0])

    def test_builds_index_file(self):
        self.dir_reader.read_files()
        self.dir_reader.parse_file_names()
        self.index_builder.add_records(self.dir_reader.file_data)
        self.dir_reader.build_index()

    # file mover
    def test_saves_index_file_on_dropoff_server(self):
        assert False
        self.dir_reader.read_files()
        self.dir_reader.parse_file_names()
        self.dir_reader.validate_data()
        self.dir_reader.build_index()
        self.dir_reader.save_index()
        assert "" in os.listdir(settings.DROPOFF_INDEX_PATH)

    def test_copies_files_to_dropoff_server(self):
        assert False

    def test_copies_files_to_pickup_server_archive(self):
        assert False

    def test_deletes_files_on_pickup_server(self):
        assert False

    # database reader
    def test_connects_to_database(self):
        assert False

    def test_validates_employee_number_exists(self):
        assert False

    def test_raises_inputerror_on_invalid_employee_number(self):
        assert False
