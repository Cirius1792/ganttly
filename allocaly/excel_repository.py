
from dataclasses import dataclass
import pandas as pd
from typing import List, Optional

DATE_FORMAT = "%d-%b-%y"


@dataclass
class AllocationDto:
    employee: str
    activity: str
    stream: str
    activity_category: str
    mds: float


PERSON_HEADER = "Persone"
ACTIVITY_HEADER = "Attività"
ACTIVITY_CATEGORY_HEADER = "Activity Type"
STREAM_HEADER = "Stream"
DATE_HEADER = "Mese-Anno"
MDS_HEADER = "Giornate"


class ExcelRepository:
    EXPECTED_COLUMNS = [
        PERSON_HEADER,
        ACTIVITY_HEADER,
        STREAM_HEADER,
        DATE_HEADER,
        MDS_HEADER,
        # Anno
        # Note
        # Check Allocazione Nel Piano
        # Start Date
        # End Date
    ]

    def __init__(self, file_path: str, sheet_name: str = "Sheet1"):
        self.file_path = file_path
        self.sheet_name = sheet_name

    def validate_columns(self, df: pd.DataFrame):
        missing_columns = [
            col for col in self.EXPECTED_COLUMNS if col not in df.columns]
        if missing_columns:
            raise ValueError(
                f"Missing columns in the Excel sheet: {', '.join(missing_columns)}")

    def load_allocation(self, stream_filter: Optional[List[str]] = None) -> List[AllocationDto]:
        df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
        activities = []

        # Validate the columns
        self.validate_columns(df)

        if stream_filter:
            df = df[df[STREAM_HEADER].isin(stream_filter)]

        for _, row in df.iterrows():
            activity = AllocationDto(
                stream=row[STREAM_HEADER],
                activity=row[ACTIVITY_HEADER],
                activity_category=row[ACTIVITY_CATEGORY_HEADER],
                employee=row[PERSON_HEADER],
                mds=row[MDS_HEADER],
            )
            activities.append(activity)

        return activities
