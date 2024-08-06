import pandas as pd
from ganttly.dto import ActivityDTO, ActivityTypeEnum
from typing import List

DATE_FORMAT = "%d-%b-%y"


class ExcelRepository:
    def __init__(self, file_path: str, sheet_name: str):
        self.file_path = file_path
        self.sheet_name = sheet_name

    def load_activities(self) -> List[ActivityDTO]:
        df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
        activities = []

        for _, row in df.iterrows():
            activity = ActivityDTO(
                sub_stream=row['Sub Stream'],
                activity=row['Activity'],
                activity_category=row['Activity Category'],
                activity_type=ActivityTypeEnum.from_string(
                    row['Activity Type']),
                start_date=row['Start Date'],
                end_date=row['End Date'] if row['Activity Type'] == 'Task' else None,
                owner=row['Owner'],
                state=row['State'],
                notes=row.get('Notes')
            )
            activities.append(activity)

        return activities
