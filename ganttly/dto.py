# dto.py

from enum import Enum
from typing import Optional
from datetime import datetime
from dataclasses import dataclass


class ActivityTypeEnum(Enum):
    TASK = "Task"
    MILESTONE = "Milestone"
    DEPENDENCY = "Dependency"
    DELIVERABLE = "Deliverable"
    MISC = "Misc"
    UNKNOWN = "Unknown"

    @staticmethod
    def from_string(value: str) -> 'ActivityTypeEnum':
        for item in ActivityTypeEnum:
            if item.value == value:
                return item
        return ActivityTypeEnum.UNKNOWN


@dataclass
class ActivityDTO:
    sub_stream: str
    activity: str
    activity_category: str
    activity_type: ActivityTypeEnum
    start_date: datetime
    end_date: datetime
    owner: str
    state: str
    notes: Optional[str] = None
