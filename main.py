# main.py

from ganttly.excel_repository import ExcelRepository
from ganttly.activity_service import ActivityService
from ganttly.gantt_chart_aggregator import GanttChartAggregator
from ganttly.gantt_chart_generator import GanttChartGenerator
import argparse
import webbrowser


def main():
    parser = argparse.ArgumentParser(
        description="Generate a Gantt chart from an Excel file.")
    parser.add_argument('file_path', type=str,
                        help="Path to the Excel file containing the activity data.")
    parser.add_argument('--sheet', type=str, default='Sheet1',
                        help="Name of the sheet in the Excel file to load data from. Default is 'Sheet1'.")
    parser.add_argument('--filter', type=str, nargs='*',
                        help="List of sub-streams to filter activities by. If not provided, all sub-streams will be included.")
    parser.add_argument('--per-stream', '-ps', action='store_true',
                        help="Print a Gantt chart per sub-stream. Default is False.")
    parser.add_argument('--group-per-activity', '-a', action='store_true',
                        help="Make a separate bar in the chart for each activity")
    parser.add_argument('--output', type=str, default='gantt_charts.html',
                        help="Output HTML file to save the charts. Default is 'gantt_charts.html'.")
    args = parser.parse_args()

    # Initialize the repository with the given file path and sheet name
    repository = ExcelRepository(
        file_path=args.file_path, sheet_name=args.sheet)

    service = ActivityService(repository)
    figs = []
    try:
        if args.per_stream:
            activities_by_stream = service.get_activities_by_stream()
            for stream, activities in activities_by_stream.items():
                chart_generator = GanttChartGenerator(
                    activities, title=stream, by_category=args.group_per_activity)
                figs.append(chart_generator.draw_chart())
        else:
            activities = service.get_activities(args.filter)
            chart_generator = GanttChartGenerator(
                activities, by_category=args.group_per_activity)
            fig = chart_generator.draw_chart()
            figs.append(fig)
    except ValueError as e:
        print(f"Error: {e}")
        return

    aggregator = GanttChartAggregator()

    for fig in figs:
        aggregator.add_chart(fig)

    aggregator.save_to_file(args.output)

    webbrowser.open(args.output)


if __name__ == "__main__":
    main()
