from unittest import TestCase

from allocaly.excel_repository import ExcelRepository


class TestExcelRepository(TestCase):
    def test_load_activities(self):
        repository = ExcelRepository(
            './tests/resources/test_plan.xlsx', 'Allocations')
        allocations = repository.load_allocation()
        self.assertEqual(3, len(allocations))
        allocation_1 = allocations[0]
        self.assertEqual('Mario', allocation_1.employee)
        self.assertEqual(
            'Requisiti di Accesso - M_Mutui_ATE_Task', allocation_1.activity)
        self.assertEqual('Requisiti di Accesso - M', allocation_1.stream)
        self.assertEqual('ATE', allocation_1.activity_category)
        self.assertEqual(5.0, allocation_1.mds)

    def test_load_activities_with_sub_stream_filter(self):
        repository = ExcelRepository(
            './tests/resources/test_plan.xlsx', 'Allocations')
        allocations = repository.load_allocation(stream_filter=["Stream 2"])
        self.assertEqual(1, len(allocations))
        allocation_1 = allocations[0]
        self.assertEqual('Emanuelo', allocation_1.employee)
        self.assertEqual(
            'Stream 2 - Sviluppi', allocation_1.activity)
        self.assertEqual('Stream 2', allocation_1.stream)
        self.assertEqual('Sviluppi', allocation_1.activity_category)
        self.assertEqual(10.0, allocation_1.mds)
