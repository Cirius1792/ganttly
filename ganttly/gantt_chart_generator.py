# gantt_chart_generator.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from ganttly.dto import ActivityCategoryEnum, ActivityDTO, ActivityTypeEnum
from typing import List, Dict

MILESTONE_SYMBOL = 'diamond'
DEPENDENCY_SYMBOL = 'diamond-wide'
COLOR_MAPPING = {
    ActivityCategoryEnum.AFU.value: '#c1ffc6',  # green
    ActivityCategoryEnum.ATE.value: '#7ac493',  # green
    ActivityCategoryEnum.DEVELOPMENT.value: '#b1d6ff',  # light blue
    ActivityCategoryEnum.INTEGRATION_TEST.value: '#bbbbbb',  # grey
    ActivityCategoryEnum.SYSTEM_TEST.value: '#e2a6b6',  # rose
    ActivityCategoryEnum.UAT.value: '#bd92de',  # violet
    ActivityCategoryEnum.RELEASE.value: '#ff7e79'  # light rose
}


@dataclass
class GantRowDTO:
    sub_stream: str
    activity: str
    activity_label: str
    activity_category: str
    activity_type: str
    start_date: datetime
    end_date: datetime


def color_from_activity_category() -> Dict[str, str]:
    return COLOR_MAPPING


def to_gantt_row(activity: ActivityDTO) -> GantRowDTO:
    return GantRowDTO(
        sub_stream=activity.sub_stream,
        activity=f"{activity.sub_stream}-{activity.activity}",
        activity_label=f"{activity.sub_stream}-{activity.activity}-{activity.activity_category}",
        activity_category=activity.activity_category.value,
        activity_type=activity.activity_type.value,
        start_date=activity.start_date,
        end_date=activity.end_date,
    )


class GanttChartGenerator(ABC):

    AXIS_TEXT_SIZE = 22
    LABEL_TEXT_SIZE = 28

    def __init__(self, activities: List[ActivityDTO],
                 title="Gantt Chart",
                 hide_title=False,
                 hide_legend=False,
                 **kwargs
                 ):
        self.title = title if not hide_title else None
        self.hide_title = hide_title
        self.activities = activities
        self.hide_legend = hide_legend

    def _validate_activities(self):
        """
        Perofrms the following checks depending on the activity type: 
            1. TASK: both start_date and end_date are set
            2. MILESTONE: start_date is set
            """
        for activity in self.activities:
            match activity.activity_type:
                case ActivityTypeEnum.TASK:
                    if not activity.start_date or not activity.end_date:
                        raise ValueError(
                            f"Activity {activity.activity} is missing start_date or end_date")
                case ActivityTypeEnum.MILESTONE:
                    if not activity.start_date:
                        raise ValueError(
                            f"Activity {activity.activity} is missing start_date")

    def _add_depenencies(self, dependencies, show_key: str, marker_symbol: str, fig: go.Figure, numerate=False) -> go.Figure:
        if not dependencies.empty:
            for _, dependency in dependencies.iterrows():
                fig.add_trace(go.Scatter(
                    x=[dependency['Start Date']],
                    y=[dependency[show_key]],
                    mode='markers',
                    marker=dict(
                        symbol=marker_symbol, size=GanttChartGenerator.LABEL_TEXT_SIZE, color='blue'),
                    text=dependency['Activity'],
                    textposition='top center',
                    name=dependency['Activity Category']
                ))
        return fig

    def draw_chart(self) -> go.Figure:
        self._validate_activities()
        fig = self._draw_chart()
        fig.update_yaxes(
            title_font=dict(size=GanttChartGenerator.AXIS_TEXT_SIZE),
        )
        fig.update_xaxes(
            title_font=dict(size=GanttChartGenerator.AXIS_TEXT_SIZE),
        )
        fig.update_layout(
            font=dict(
                size=GanttChartGenerator.LABEL_TEXT_SIZE,  # Set the font size here
            )
        )
        return fig

    @abstractmethod
    def _draw_chart(self) -> go.Figure:
        pass


class GanttChartSubStreamGenerator(GanttChartGenerator):
    def __init__(self, activities: List[ActivityDTO],
                 title="Gantt Chart",
                 **kwargs
                 ):
        super().__init__(activities, title, **kwargs)

    def _draw_chart(self) -> go.Figure:

        df = pd.DataFrame([{
            'Sub Stream': activity.sub_stream,
            'Activity': activity.activity,
            'Activity Category': activity.activity_category,
            'Activity Type': activity.activity_type,
            'Start Date': activity.start_date,
            'End Date': activity.end_date,
        } for activity in map(
            to_gantt_row, self.activities)])

        sub_streams = df['Sub Stream'].unique()
        show_key = 'Activity'
        df = df.sort_values(by=[show_key, 'Start Date'], ascending=True)
        category_orders = {
            "Sub Stream": sub_streams,
            "Activity Category": [
                e.value for e in ActivityCategoryEnum.get_ordered()]
        }
        fig = px.timeline(df,
                          x_start="Start Date",
                          x_end="End Date",
                          y=show_key,
                          color="Activity Category",
                          title=self.title,
                          text="Activity",
                          category_orders=category_orders,
                          color_discrete_map=color_from_activity_category()
                          )
        for shape in fig['data']:
            shape['opacity'] = 0.85

        # Extract milestones
        milestones = df[df['Activity Type'] ==
                        ActivityTypeEnum.MILESTONE.value]

        # Add scatter plot for milestones
        self._add_depenencies(milestones, show_key, MILESTONE_SYMBOL, fig)

        # Extract dependencies
        dependencies = df[df['Activity Type'] ==
                          ActivityTypeEnum.DEPENDENCY.value]

        # Add scatter plot for milestones
        self._add_depenencies(dependencies, show_key, DEPENDENCY_SYMBOL, fig)

        fig.update_layout(xaxis_title="Date",
                          yaxis_title="Sub Stream",
                          showlegend=not self.hide_legend)
        return fig


class GanttChartActivityGenerator(GanttChartGenerator):
    def __init__(self, activities: List[ActivityDTO],
                 title="Gantt Chart",
                 **kwargs
                 ):
        super().__init__(activities, title, **kwargs)

    def _draw_chart(self) -> go.Figure:

        df = pd.DataFrame([{
            'Sub Stream': activity.sub_stream,
            'Activity': activity.activity,
            'Activity Category': activity.activity_category,
            'Activity Type': activity.activity_type,
            'Start Date': activity.start_date,
            'End Date': activity.end_date,
        } for activity in map(to_gantt_row, self.activities)])

        sub_streams = df['Sub Stream'].unique()
        show_key = 'Activity Category'
        actual_activities = {e.activity_category for e in self.activities}
        df = df.sort_values(by=[show_key, 'Start Date'], ascending=True)
        category_orders = {
            "Sub Stream": sub_streams,
            "Activity Category": [
                e.value for e in ActivityCategoryEnum.get_ordered() if e in actual_activities]
        }
        fig = px.timeline(df,
                          x_start="Start Date",
                          x_end="End Date",
                          y=show_key,
                          color="Activity Category",
                          title=self.title,
                          # text="Activity",
                          category_orders=category_orders,
                          color_discrete_map=color_from_activity_category()
                          )

        # Extract milestones
        milestones = df[df['Activity Type'] ==
                        ActivityTypeEnum.MILESTONE.value]

        # Add scatter plot for milestones
        self._add_depenencies(milestones, show_key, MILESTONE_SYMBOL, fig)

        # Extract dependencies
        dependencies = df[df['Activity Type'] ==
                          ActivityTypeEnum.DEPENDENCY.value]

        # Add scatter plot for milestones
        self._add_depenencies(dependencies, show_key, DEPENDENCY_SYMBOL, fig)

        fig.update_layout(xaxis_title="Date",
                          yaxis_title="Activity",
                          showlegend=not self.hide_legend)
        return fig
