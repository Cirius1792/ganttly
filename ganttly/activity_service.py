# activity_service.py

from ganttly.excel_repository import ExcelRepository
from ganttly.dto import ActivityDTO
from typing import List

class ActivityService:
    def __init__(self, repository: ExcelRepository):
        self.repository = repository

    def get_all_activities(self) -> List[ActivityDTO]:
        return self.repository.load_activities()

