# main.py

from ganttly.gantly_command import GanttlyCommandFactory, GanttlyConfiguration
import argparse
import webbrowser


def args_to_cofnig_mapper(args) -> GanttlyConfiguration:
    return GanttlyConfiguration(args.group_per_activity, args.per_stream, args.output, args.sheet, args.filter)


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
                        help="""Make a separate bar in the chart for each activity. 
                        The activities are: 
                        - afu
                        - ate
                        - development
                        - integration test
                        - system_test
                        - uat
                        - release
                        - post go live
                        """)
    parser.add_argument('--output', type=str, default='gantt_charts.html',
                        help="Output HTML file to save the charts. Default is 'gantt_charts.html'.")
    args = parser.parse_args()
    config = args_to_cofnig_mapper(args)
    command = GanttlyCommandFactory(args.file_path, config).create()
    try:
        command.execute()
    except ValueError as e:
        print(f"Error: {e}")
        return

    webbrowser.open(config.output)


if __name__ == "__main__":
    main()
