from result import Result, Ok, Err
from my_package import input_error
from src.my_package import directory_reader


class Record():
    def __init__(self, file_data: directory_reader.FileData):
        self.path: str = file_data.full_path
        match self.get_report_id(file_data):
            case Ok(value):
                self.report_id: str = value
            case Err(e):
                raise e
        match self.get_employee_number(file_data):
            case Ok(value):
                self.employee: str = value
            case Err(e):
                raise e

    def __repr__(self):
        return f"""<record="{self.path}>
        <meta="report_id" value="{self.report_id}"/>
        <meta="employee" value="{self.employee}"/>
        </record>
        """

    def get_report_id(
        self,
        file_data: directory_reader.FileData
    ) -> Result[str, Exception]:
        match file_data.document_type:
            case "OTH":
                return Ok("HR_OTHER")
            case _:
                return Err(input_error.InputError(
                    Exception(
                       """Document Type was not recognized.
                        No cooresponding report_id"""
                    ),
                    file_data.full_path
                ))

    def lookup_employee_number_in_database(
        self,
        employee_number: str,
    ) -> Result[bool, Exception]:
        try:
            # simulate a database call and return
            return Ok(employee_number in ["203958", "432224", "624994"])
        except Exception as e:
            return Err(e)

    def get_employee_number(
        self,
        file_data: directory_reader.FileData,
    ) -> Result[str, Exception]:
        match self.lookup_employee_number_in_database(
            file_data.employee_number
        ):
            case Ok(is_valid):
                if is_valid:
                    return Ok(file_data.employee_number)
                return Err(input_error.InputError(
                    Exception("Employee number was not found in database"),
                    file_data.full_path
                ))
            case Err(e):
                return Err(input_error.InputError(
                    e,
                    file_data.full_path,
                ))
