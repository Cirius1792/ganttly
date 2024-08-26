# main.py

from ganttly.gantly_command import GanttlyCommandFactory, GanttlyConfiguration
import click
import webbrowser


def args_to_config_mapper(
    group_per_activity,
    per_stream,
    output,
    sheet,
    filter,
    hide_legend,
    hide_title,
) -> GanttlyConfiguration:
    return GanttlyConfiguration(
        group_per_activity=group_per_activity,
        per_stream=per_stream,
        output=output,
        sheet=sheet,
        filter=filter,
        hide_legend=hide_legend,
        hide_title=hide_title,
    )


@click.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--sheet', type=str, default='Sheet1',
              help="Name of the sheet in the Excel file to load data from. Default is 'Sheet1'.")
@click.option('--filter', type=str, multiple=True,
              help="List of sub-streams to filter activities by. If not provided, all sub-streams will be included.")
@click.option('--per-stream', '-ps', is_flag=True,
              help="Print a Gantt chart per sub-stream. Default is False.")
@click.option('--hide-legend', '-l', is_flag=True, default=False,
              help="Enable or disable legend. Default is True.")
@click.option('--hide-title', '-t', is_flag=True, default=False,
              help="Enable or disable gantt graph title. Default is True.")
@click.option('--group-per-activity', '-a', is_flag=True,
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
@click.option('--output', type=str, default='gantt_charts.html',
              help="Output HTML file to save the charts. Default is 'gantt_charts.html'.")
def cli(file_path, sheet, filter, per_stream, hide_legend, hide_title, group_per_activity, output):
    config = args_to_config_mapper(
        group_per_activity=group_per_activity,
        per_stream=per_stream,
        output=output,
        sheet=sheet,
        filter=filter,
        hide_legend=hide_legend,
        hide_title=hide_title,
    )
    command = GanttlyCommandFactory(file_path, config).create()
    try:
        command.execute()
    except ValueError as e:
        click.echo(f"Error: {e}")
        return

    webbrowser.open(config.output)


if __name__ == "__main__":
    cli()
