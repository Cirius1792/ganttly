from unittest import TestCase

from ganttly.dto import ActivityTypeEnum
from ganttly.gantt_chart_generator import GanttChartActivityGenerator
from tests.ganttly.activity_dto_helper import build_activity_dto


class TestGanttChartGenerator(TestCase):

    def test_should_fail_for_task_with_no_end_date(self):
        activity = build_activity_dto("Stream 1", "Activity 1")
        activity.activity_type = ActivityTypeEnum.TASK
        activity.end_date = None
        activities = [
            activity
        ]
        gcg = GanttChartActivityGenerator(activities)
        with self.assertRaises(ValueError):
            gcg.draw_chart()

    def test_should_fail_for_task_with_no_start_date(self):
        activity = build_activity_dto("Stream 1", "Activity 1")
        activity.activity_type = ActivityTypeEnum.TASK
        activity.start_date = None
        activities = [
            activity
        ]
        gcg = GanttChartActivityGenerator(activities)
        with self.assertRaises(ValueError):
            gcg.draw_chart()

    def test_should_fail_for_milestone_with_no_start_date(self):
        activity = build_activity_dto("Stream 1", "Activity 1")
        activity.activity_type = ActivityTypeEnum.MILESTONE
        activity.start_date = None
        activities = [
            activity
        ]
        gcg = GanttChartActivityGenerator(activities)
        with self.assertRaises(ValueError):
            gcg.draw_chart()
