import pandas as pd
from ganttly.dto import ActivityDTO, ActivityTypeEnum
from typing import List, Optional

DATE_FORMAT = "%d-%b-%y"


class ExcelRepository:
    EXPECTED_COLUMNS = [
        'Sub Stream',
        'Activity',
        'Activity Category',
        'Activity Type',
        'Start Date',
        'End Date',
    ]

    def __init__(self, file_path: str, sheet_name: str="Sheet1"):
        self.file_path = file_path
        self.sheet_name = sheet_name

    def validate_columns(self, df: pd.DataFrame):
        missing_columns = [
            col for col in self.EXPECTED_COLUMNS if col not in df.columns]
        if missing_columns:
            raise ValueError(
                f"Missing columns in the Excel sheet: {', '.join(missing_columns)}")

    def load_activities(self, sub_stream_filter: Optional[List[str]] = None) -> List[ActivityDTO]:
        df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
        activities = []
        # Validate the columns
        self.validate_columns(df)

        if sub_stream_filter:
            df = df[df['Sub Stream'].isin(sub_stream_filter)]

        for _, row in df.iterrows():
            activity = ActivityDTO(
                sub_stream=row['Sub Stream'],
                activity=row['Activity'],
                activity_category=row['Activity Category'],
                activity_type=ActivityTypeEnum.from_string(
                    row['Activity Type']),
                start_date=row['Start Date'],
                end_date=row['End Date'] if row['Activity Type'] == 'Task' else None,
                owner=row['Owner'] if 'Owner' in df.columns else None,
                state=row['State'] if 'State' in df.columns else None,
                notes=row['Notes'] if 'Notes' in df.columns else None
            )
            activities.append(activity)

        return activities
