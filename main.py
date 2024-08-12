# main.py

from ganttly.excel_repository import ExcelRepository
from ganttly.activity_service import ActivityService
from ganttly.gantt_chart_generator import GanttChartGenerator
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Generate a Gantt chart from an Excel file.")
    parser.add_argument('file_path', type=str,
                        help="Path to the Excel file containing the activity data.")
    parser.add_argument('--sheet', type=str, default='Sheet1',
                        help="Name of the sheet in the Excel file to load data from. Default is 'Sheet1'.")
    parser.add_argument('--filter', type=str, nargs='*',
                        help="List of sub-streams to filter activities by. If not provided, all sub-streams will be included.")

    args = parser.parse_args()

    # Initialize the repository with the given file path and sheet name
    repository = ExcelRepository(
        file_path=args.file_path, sheet_name=args.sheet)

    service = ActivityService(repository)

    activities = service.get_activities(args.filter)
    chart_generator = GanttChartGenerator(activities)

    chart_generator.draw_chart()


if __name__ == "__main__":
    main()
