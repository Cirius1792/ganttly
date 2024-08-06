from datetime import datetime
from ganttly.dto import ActivityDTO, ActivityTypeEnum


def build_activity_dto():
    return ActivityDTO(
        sub_stream="Stream1",
        activity="Activity1",
        activity_category="Category1",
        activity_type=ActivityTypeEnum.TASK,
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2023, 1, 10),
        owner="Owner1",
        state="State1",
        notes="Some notes"
    )
