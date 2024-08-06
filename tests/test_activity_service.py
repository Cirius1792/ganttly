# test_activity_service.py

import unittest
from unittest.mock import Mock
from ganttly.activity_service import ActivityService
from ganttly.dto import ActivityTypeEnum

from tests.activity_dto_helper import build_activity_dto


class TestActivityService(unittest.TestCase):
    def test_get_all_activities(self):
        mock_repository = Mock()
        mock_repository.load_activities.return_value = [
            build_activity_dto()
        ]

        service = ActivityService(mock_repository)
        activities = service.get_all_activities()

        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertEqual(activity.sub_stream, "Stream1")
        self.assertEqual(activity.activity, "Activity1")
        self.assertEqual(activity.activity_category, "Category1")
        self.assertEqual(activity.activity_type, ActivityTypeEnum.TASK)
        self.assertIsNotNone(activity.start_date)
        self.assertIsNotNone(activity.end_date)
        self.assertEqual(activity.owner, "Owner1")
        self.assertEqual(activity.state, "State1")
        self.assertEqual(activity.notes, "Some notes")
