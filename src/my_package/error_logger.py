from src.my_package import input_error


class ErrorLogger():
    def __init__(self):
        self.error_list: list[input_error.InputError] = []
