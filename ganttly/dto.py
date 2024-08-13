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
    afu = "AFU"
    ate = "ATE"
    development = "Sviluppi"
    integration_test = "Integration Test"
    system_test = "System Test"
    uat = "UAT"
    release = "Rilascio in produzione"
    post_go_live = "Post Go Live"

    @staticmethod
    def get_ordered() -> List['ActivityCategoryEnum']:
        return [
            ActivityCategoryEnum.afu,
            ActivityCategoryEnum.ate,
            ActivityCategoryEnum.development,
            ActivityCategoryEnum.integration_test,
            ActivityCategoryEnum.system_test,
            ActivityCategoryEnum.uat,
            ActivityCategoryEnum.release,
            ActivityCategoryEnum.post_go_live,
        ]


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
