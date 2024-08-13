# activity_service.py

from collections import defaultdict
from ganttly.excel_repository import ExcelRepository
from ganttly.dto import ActivityDTO
from typing import Dict, List, Optional


class ActivityService:
    def __init__(self, repository: ExcelRepository):
        self.repository = repository

    def get_all_activities(self) -> List[ActivityDTO]:
        return self.repository.load_activities()

    def get_activities(self, sub_stream_filter: Optional[List[str]] = None) -> List[ActivityDTO]:
        return self.repository.load_activities(sub_stream_filter=sub_stream_filter)

    def get_activities_by_stream(self) -> Dict[str, List[ActivityDTO]]:
        grouped_activities = defaultdict(list)
        activities = self.repository.load_activities()
        for activity in activities:
            grouped_activities[activity.sub_stream].append(activity)
        return {k: v for k, v in grouped_activities.items()}
