# test_excel_repository.py

import unittest
import pandas as pd
from unittest.mock import patch
from ganttly.dto import ActivityCategoryEnum, ActivityTypeEnum
from ganttly.excel_repository import ExcelRepository


class TestExcelRepository(unittest.TestCase):
    @patch('ganttly.excel_repository.pd.read_excel')
    def test_load_activities(self, mock_read_excel):
        mock_data = {
            'Sub Stream': ['Stream1'],
            'Activity': ['Activity1'],
            'Activity Category': ["Integration Test"],
            'Activity Type': ['Task'],
            'Start Date': ['2023-01-01'],
            'End Date': ['2023-01-10'],
            'Owner': ['Owner1'],
            'State': ['State1'],
            'Notes': ['Some notes']
        }
        mock_read_excel.return_value = pd.DataFrame(mock_data)

        repository = ExcelRepository('dummy_path.xlsx', 'Sheet1')
        activities = repository.load_activities()

        self.assertEqual(len(activities), 1)
        activity = activities[0]
        self.assertEqual(activity.sub_stream, "Stream1")
        self.assertEqual(activity.activity, "Activity1")
        self.assertEqual(activity.activity_category, ActivityCategoryEnum.INTEGRATION_TEST)
        self.assertEqual(activity.activity_type, ActivityTypeEnum.TASK)
        # self.assertEqual(activity.start_date, datetime(2023, 1, 1).date())
        # self.assertEqual(activity.end_date, datetime(2023, 1, 10).date())
        self.assertEqual(activity.owner, "Owner1")
        self.assertEqual(activity.state, "State1")
        self.assertEqual(activity.notes, "Some notes")

    @patch('ganttly.excel_repository.pd.read_excel')
    def test_load_activities_with_sub_stream_filter(self, mock_read_excel):
        mock_data = pd.DataFrame({
            'Sub Stream': ["Stream1", "Stream2", "Stream3"],
            'Activity': ["Activity1", "Activity2", "Activity3"],
            'Activity Category': ["Category1", "Category2", "Category3"],
            'Activity Type': ["Type1", "Type2", "Type3"],
            'Start Date': ["2023-01-01", "2023-02-01", "2023-03-01"],
            'End Date': ["2023-01-10", "2023-02-10", "2023-03-10"],
            'Owner': ["Owner1", "Owner2", "Owner3"],
            'State': ["State1", "State2", "State3"],
            'Notes': ["Notes1", "Notes2", "Notes3"]
        })
        mock_read_excel.return_value = mock_data

        repository = ExcelRepository(
            "path_to_your_excel_file.xlsx", sheet_name="Sheet1")
        activities = repository.load_activities(
            sub_stream_filter=["Stream1", "Stream3"])

        self.assertEqual(len(activities), 2)
        self.assertEqual(activities[0].sub_stream, "Stream1")
        self.assertEqual(activities[1].sub_stream, "Stream3")
