from enum import Enum
from enum import auto

# * DEBUG ----------------------------------------------------------------------

__DEBUG_ENABLED__: bool = True

# * ENUMS ----------------------------------------------------------------------

class TimeBlockTypes(Enum):
    PROCESSING_DELAY = auto()
    TRANSMISSION_DELAY = auto()
    PROPAGATION_DELAY = auto()
    QUEUING_DELAY = auto()