from utils.storage import Storage #responsible for persistent storage and retrieval of data for users, projects, and tasks

class Task:
    ALL_TASKS = [] #keeps track of all task instances for in-memory management and persistence

    def __init__(self, title: str, assigned_to: int, project_id: int, status: str = "Pending", id: int = None):
        self.id = id if id is not None else self._generate_next_id()
        self.title = title
        self.status = status
        self.assigned_to = assigned_to  
        self.project_id = project_id    
        Task.ALL_TASKS.append(self)

    def _generate_next_id(self) -> int:
        return max([t.id for t in Task.ALL_TASKS], default=0) + 1

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        valid_states = {"Pending", "In Progress", "Completed"}
        if value not in valid_states:
            raise ValueError(f"State mutation assertion failure: Status must align to one of {valid_states}.")
        self._status = value

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "project_id": self.project_id
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            title=data["title"],
            assigned_to=data["assigned_to"],
            project_id=data["project_id"],
            status=data.get("status", "Pending"),
            id=data["id"]
        )

    @classmethod
    def load_collection(cls):
        cls.ALL_TASKS.clear()
        records = Storage.load_records("tasks.json")
        for r in records:
            cls.from_dict(r)

    @classmethod
    def save_collection(cls):
        records = [t.to_dict() for t in cls.ALL_TASKS]
        Storage.save_records("tasks.json", records)

    def __repr__(self) -> str:
        return f"Task(ID: {self.id}, Title: '{self.title}', Status: '{self.status}')"
