from datetime import datetime
from abc import ABC

class TimestampBase(ABC):

    def __init__(self):
        self.Timestamp = datetime.now()

        
    @property
    def Age(self):
        return datetime.now() - self.Timestamp

