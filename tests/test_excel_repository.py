# test_excel_repository.py

import unittest
import pandas as pd
from unittest.mock import patch
from ganttly.dto import ActivityTypeEnum
from ganttly.excel_repository import ExcelRepository
from datetime import datetime


class TestExcelRepository(unittest.TestCase):
    @patch('ganttly.excel_repository.pd.read_excel')
    def test_load_activities(self, mock_read_excel):
        mock_data = {
            'Sub Stream': ['Stream1'],
            'Activity': ['Activity1'],
            'Activity Category': ['Category1'],
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
        self.assertEqual(activity.activity_category, "Category1")
        self.assertEqual(activity.activity_type, ActivityTypeEnum.TASK)
        # self.assertEqual(activity.start_date, datetime(2023, 1, 1).date())
        # self.assertEqual(activity.end_date, datetime(2023, 1, 10).date())
        self.assertEqual(activity.owner, "Owner1")
        self.assertEqual(activity.state, "State1")
        self.assertEqual(activity.notes, "Some notes")
