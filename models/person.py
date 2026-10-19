import re #Regular expression module for pattern matching and validation

class Person:
    """Acts as abstract Base Class demonstrating implementation inheritance. You can refer it to as the blue print"""
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    @property #getter for the name property, allowing controlled access to the private _name attribute
    def name(self) -> str:
        return self._name

    @name.setter #setter for the name property, enforcing validation rules before setting the private _name attribute
    def name(self, value: str):
        if not value or not value.strip():
            raise ValueError("Name property constraint violation: Cannot be null or blank.")
        self._name = value.strip()

    @property #getter for the email property, allowing controlled access to the private _email attribute
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, value):
            raise ValueError(f"Malformed structural parameter: '{value}' is not a valid email.")
        self._email = value.strip()
