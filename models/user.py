from models.person import Person
from utils.storage import Storage

class User(Person):
    ALL_USERS = []
    
    def __init__(self, name: str, email: str, id: int = None):
        super().__init__(name, email)
        self.id = id if id is not None else self._generate_next_id()
        User.ALL_USERS.append(self)

    def _generate_next_id(self) -> int:
        return max([u.id for u in User.ALL_USERS], default=0) + 1

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "email": self.email}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(name=data["name"], email=data["email"], id=data["id"])

    @classmethod
    def load_collection(cls):
        cls.ALL_USERS.clear()
        records = Storage.load_records("users.json")
        for r in records:
            cls.from_dict(r)

    @classmethod
    def save_collection(cls):
        records = [u.to_dict() for u in cls.ALL_USERS]
        Storage.save_records("users.json", records)

    def __repr__(self) -> str:
        return f"User(ID: {self.id}, Name: '{self.name}')"
