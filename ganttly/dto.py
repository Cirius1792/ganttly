# dto.py

from enum import Enum
from typing import Optional, List
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


class ActivityCategoryEnum(Enum):
    AFU = "AFU"
    ATE = "ATE"
    DEVELOPMENT = "Sviluppi"
    INTEGRATION_TEST = "Integration Test"
    SYSTEM_TEST = "System Test"
    UAT = "UAT"
    RELEASE = "Rilascio in produzione"
    POST_GO_LIVE = "Post Go Live"
    UNKNOWN = "N/A"

    @staticmethod
    def get_ordered() -> List['ActivityCategoryEnum']:
        return [
            ActivityCategoryEnum.AFU,
            ActivityCategoryEnum.ATE,
            ActivityCategoryEnum.DEVELOPMENT,
            ActivityCategoryEnum.INTEGRATION_TEST,
            ActivityCategoryEnum.SYSTEM_TEST,
            ActivityCategoryEnum.UAT,
            ActivityCategoryEnum.RELEASE,
            ActivityCategoryEnum.POST_GO_LIVE,
        ]

    @staticmethod
    def from_string(value: str) -> 'ActivityCategoryEnum':
        for item in ActivityCategoryEnum:
            if item.value == value:
                return item
        return ActivityCategoryEnum.UNKNOWN

@dataclass
class ActivityDTO:
    sub_stream: str
    activity: str
    activity_category: ActivityCategoryEnum
    activity_type: ActivityTypeEnum
    start_date: datetime
    end_date: datetime
    owner: str
    state: str
    notes: Optional[str] = None
