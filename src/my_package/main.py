from my_package import (
    settings,
    directory_reader,
)


def main():
    dir_reader = directory_reader.DirectoryReader(
        settings.PICKUP_FILES_PATH,
        settings.PICKUP_ARCHIVE_PATH,
        settings.DROPOFF_INDEX_PATH,
        settings.DROPOFF_FILES_PATH,
        settings.TARGET_FILE_EXTENSIONS,
    )
    dir_reader.read_files()
    dir_reader.parse_file_names()


if __name__ == "__main__":
    main()
