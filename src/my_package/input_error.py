
class InputError(Exception):
    """The value from an outside source was found to be invalid"""

    def __init__(self, ex: Exception, file_name: str):
        super().__init__(ex)
        self.file_name: str = file_name
