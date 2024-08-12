from datetime import datetime
from ganttly.dto import ActivityDTO, ActivityTypeEnum


def build_activity_dto(
        sub_stream,
        activity,
        activity_category="Category1",
        activity_type=ActivityTypeEnum.TASK,
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2023, 1, 10),
        owner="Owner1",
        state="State1",
        notes="Some notes"
        ):
    return ActivityDTO(
        sub_stream=sub_stream,
        activity=activity,
        activity_category=activity_category,
        activity_type=activity_type,
        start_date=start_date,
        end_date=end_date, 
        owner=owner,
        state=state,
        notes=notes
    )
