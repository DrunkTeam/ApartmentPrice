from dataclasses import asdict, dataclass

class CardsDB:
    def __init__(self, db_path):
        self._db_path = db_path

@dataclass
class Card:
    summary: str = None
    owner: str = None
    state: str = "todo"
    id: int = 0

    def from_dict(cls, d):
        return Card(**d)
    
    def to_dict(self):
        return asdict(self)
    
def sum(a, b):
    return a + b

def mul(a, b):
    return a * b