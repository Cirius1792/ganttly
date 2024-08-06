# main.py

from ganttly.excel_repository import ExcelRepository
from ganttly.activity_service import ActivityService
from ganttly.gantt_chart_generator import GanttChartGenerator


def main():
    # file_path = r'C:\Users\c.tecce\OneDrive - Reply\Documents - CORE-FFit New Price\Planning\WIP Piano Overall.xlsx'
    # sheet = "Promozioni-Canoni"

    file_path = r'./tests/resources/test_plan.xlsx'
    sheet = "MyPlan"
    repository = ExcelRepository(file_path, sheet)
    service = ActivityService(repository)

    activities = service.get_all_activities()
    chart_generator = GanttChartGenerator(activities)

    chart_generator.draw_chart()


if __name__ == "__main__":
    main()
