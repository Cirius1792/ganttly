from typing import List
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from ganttly.activity_service import ActivityService
from ganttly.excel_repository import ExcelRepository
from ganttly.gantt_chart_aggregator import GanttChartAggregator
from ganttly.gantt_chart_generator import GanttChartActivityGenerator, GanttChartSubStreamGenerator


@dataclass
class GanttlyConfiguration:
    group_per_activity: bool = False
    per_stream: bool = False
    output: str = "gantt_charts.html"
    sheet: str = "Sheet1"
    filter: List[str] = field(default_factory=list)


class GanttlyCommand(ABC):
    def __init__(self, file_path: str, config: GanttlyConfiguration):
        self.file_path = file_path
        self.config = config
        self.repository = ExcelRepository(
            file_path=file_path, sheet_name=self.config.sheet)
        self.service = ActivityService(self.repository)
        self.aggregator = GanttChartAggregator()

    @abstractmethod
    def execute(self):
        pass


class CreateActivityGanttCommand(GanttlyCommand):
    """ Creates a gantt chart where the activities are groupped by type. 
    For example, all the tasks of type "developmentE are grouped together
    """

    def execute(self):
        activities = self.service.get_activities(self.config.filter)
        chart_generator = GanttChartActivityGenerator(activities)
        fig = chart_generator.draw_chart()
        self.aggregator.add_chart(fig)
        self.aggregator.save_to_file(self.config.output)


class CreateSubStreamGanttCommand(GanttlyCommand):
    """ Creates a series of gantt chart where the activities are grouped by substream.
    Therefore a gantt per substream is created"""

    def execute(self):
        activities_by_stream = self.service.get_activities_by_stream()
        figs = []
        for stream, activities in activities_by_stream.items():
            chart_generator = GanttChartSubStreamGenerator(
                activities, title=stream)
            figs.append(chart_generator.draw_chart())

        for fig in figs:
            self.aggregator.add_chart(fig)
        self.aggregator.save_to_file(self.config.output)

class CreateSubStreamPerActivityGanttCommand(GanttlyCommand):
    """ Creates a series of gantt chart where the activities are grouped by substream.
    The activities are groupped by type.

    Therefore a gantt per substream is created and all the tasks of the same category are groupped"""
    def execute(self):
        activities_by_stream = self.service.get_activities_by_stream()
        figs = []
        for stream, activities in activities_by_stream.items():
            chart_generator = GanttChartActivityGenerator(
                activities, title=stream)
            figs.append(chart_generator.draw_chart())

        for fig in figs:
            self.aggregator.add_chart(fig)
        self.aggregator.save_to_file(self.config.output)

class CreateGanttCommand(GanttlyCommand):
    """ Creates a gantt chart."""
    def execute(self):
        activities = self.service.get_activities(self.config.filter)
        chart_generator = GanttChartSubStreamGenerator(activities)
        fig = chart_generator.draw_chart()
        self.aggregator.add_chart(fig)
        self.aggregator.save_to_file(self.config.output)


class GanttlyCommandFactory:
    def __init__(self, file_path: str, config: GanttlyConfiguration):
        self.file_path = file_path
        self.config = config

    def create(self) -> GanttlyCommand:
        """ Translates the configuration into a command"""
        if self.config.per_stream and not self.config.group_per_activity:
            return CreateSubStreamGanttCommand(self.file_path, self.config)
        if self.config.per_stream and self.config.group_per_activity:
            return CreateSubStreamPerActivityGanttCommand(self.file_path, self.config)
        if self.config.group_per_activity:
            return CreateActivityGanttCommand(self.file_path, self.config)
        return CreateGanttCommand(self.file_path, self.config)
