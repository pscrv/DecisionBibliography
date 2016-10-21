from datetime import datetime
from abc import ABC

class TimestampBase(ABC):

    def __init__(self):
        self.Timestamp = datetime.now()

        
    @property
    def Age(self):
        return datetime.now() - self.Timestamp

    @property
    def IsValid(self):
        return True

    
class OutdatedAnalysis(TimestampBase):

    def __init__(self):
        super(OutdatedAnalysis, self).__init__()
        self.Timestamp = datetime.min
        
    def __eq__(self, other):
        if isinstance(other, OutdatedAnalysis):
            return True
        return False

