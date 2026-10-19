from utils.storage import Storage #responsible for persistent storage and retrieval of data for users, projects, and tasks
from datetime import datetime #required for date parsing and validation of due_date attributes in projects

class Project:
    ALL_PROJECTS = [] #keeps track of all project instances for in-memory management and persistence

        #attributes include title, description, due_date, user_id, and an optional id for unique identification
    def __init__(self, title: str, description: str, due_date: str, user_id: int, id: int = None): 
        self.id = id if id is not None else self._generate_next_id()
        self.title = title
        self.description = description
        self.due_date = due_date
        self.user_id = user_id  
        Project.ALL_PROJECTS.append(self)

    def _generate_next_id(self) -> int:
        return max([p.id for p in Project.ALL_PROJECTS], default=0) + 1

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value or not value.strip():
            raise ValueError("Project title validation boundary failure: Empty titles forbidden.")
        self._title = value.strip()

    @property
    def due_date(self) -> str:
        return self._due_date

    @due_date.setter
    def due_date(self, value: str):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Temporal parse error: Target due_date parameter must strictly follow YYYY-MM-DD standard format.")
        self._due_date = value

    def to_dict(self) -> dict: #converts the Project instance into a dictionary format for serialization and storage
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "user_id": self.user_id
        }

    @classmethod
    #creates a Project instance from a dictionary, facilitating deserialization and reconstruction of project objects from stored data
    def from_dict(cls, data: dict): 
        return cls(
            title=data["title"],
            description=data["description"],
            due_date=data["due_date"],
            user_id=data["user_id"],
            id=data["id"]
        )

    @classmethod
    #wipes the current in-memory project collection and repopulates it from the persistent storage, ensuring data consistency across sessions
    def load_collection(cls): 
        cls.ALL_PROJECTS.clear()
        records = Storage.load_records("projects.json")
        for r in records:
            cls.from_dict(r)

    @classmethod
    #saves the current in-memory project collection to persistent storage, ensuring that all changes are retained across sessions
    def save_collection(cls): 
        records = [p.to_dict() for p in cls.ALL_PROJECTS]
        Storage.save_records("projects.json", records)
    #returns a string representation of the Project instance, useful for debugging and logging purposes
    def __repr__(self) -> str: 
        return f"Project(ID: {self.id}, Title: '{self.title}')"
