# test_activity_service.py

import unittest
from unittest.mock import Mock
from ganttly.activity_service import ActivityService
from ganttly.dto import ActivityTypeEnum

from tests.activity_dto_helper import build_activity_dto


class TestActivityService(unittest.TestCase):
    def test_get_all_activities(self):
        mock_repository = Mock()
        stream = "Stream1"
        activity_name = "Activity1"
        category = "Category1"
        owner = "Owner1"
        state = "State1"
        notes = "Some notes"
        mock_repository.load_activities.return_value = [
            build_activity_dto(sub_stream=stream, activity=activity_name,
                               activity_category=category, owner=owner, state=state, notes=notes)
        ]

        service = ActivityService(mock_repository)
        activities = service.get_all_activities()

        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertEqual(activity.sub_stream, stream)
        self.assertEqual(activity.activity, activity_name)
        self.assertEqual(activity.activity_category, category)
        self.assertEqual(activity.activity_type, ActivityTypeEnum.TASK)
        self.assertIsNotNone(activity.start_date)
        self.assertIsNotNone(activity.end_date)
        self.assertEqual(activity.owner, owner)
        self.assertEqual(activity.state, state)
        self.assertEqual(activity.notes, notes)

    def test_get_activities_with_sub_stream_filter(self):
        # Mock the repository
        mock_repository = Mock()

        # Initialize the service with the mocked repository
        service = ActivityService(mock_repository)

        # Define the filter to use
        sub_stream_filter = ["Stream1", "Stream3"]

        # Call the service method
        activities = service.get_activities(
            sub_stream_filter=sub_stream_filter)

        # Assert that the repository's load_activities method was called with the correct filter
        mock_repository.load_activities.assert_called_once_with(
            sub_stream_filter=sub_stream_filter)

        # Since we're testing the interaction, no need to assert on the returned activities,
        # as the mock is not returning actual data.
