# activity_service.py

from ganttly.excel_repository import ExcelRepository
from ganttly.dto import ActivityDTO
from typing import List, Optional


class ActivityService:
    def __init__(self, repository: ExcelRepository):
        self.repository = repository

    def get_all_activities(self) -> List[ActivityDTO]:
        return self.repository.load_activities()

    def get_activities(self, sub_stream_filter: Optional[List[str]] = None) -> List[ActivityDTO]:
        return self.repository.load_activities(sub_stream_filter=sub_stream_filter)
