# gantt_chart_generator.py

from dataclasses import dataclass
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from ganttly.dto import ActivityCategoryEnum, ActivityDTO, ActivityTypeEnum
from typing import List


@dataclass
class GantRowDTO:
    sub_stream: str
    activity: str
    activity_label: str
    activity_category: str
    activity_type: str
    start_date: datetime
    end_date: datetime


def to_gantt_row(activity: ActivityDTO) -> GantRowDTO:
    return GantRowDTO(
        sub_stream=activity.sub_stream,
        activity=f"{activity.sub_stream}-{activity.activity}",
        activity_label=f"{activity.sub_stream}-{activity.activity}-{activity.activity_category}",
        activity_category=activity.activity_category,
        activity_type=activity.activity_type.value,
        start_date=activity.start_date,
        end_date=activity.end_date
    )


class GanttChartGenerator:
    def __init__(self, activities: List[ActivityDTO],
                 title="Gantt Chart",
                 by_category: bool = False):
        self.title = title
        self.activities = [activity for activity in map(
            to_gantt_row, activities)]
        self.by_category = by_category

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

    def draw_chart(self) -> go.Figure:
        self._validate_activities()

        df = pd.DataFrame([{
            'Sub Stream': activity.sub_stream,
            'Activity': activity.activity,
            'Activity Category': activity.activity_category,
            'Activity Type': activity.activity_type,
            'Start Date': activity.start_date,
            'End Date': activity.end_date,
        } for activity in self.activities])

        sub_streams = df['Sub Stream'].unique()
        show_key = 'Activity Category' if self.by_category else 'Activity'
        df = df.sort_values(by=[show_key, 'Start Date'], ascending=True)
        category_orders = {
            "Sub Stream": df['Sub Stream'],
            "Start Date": df['Start Date']
        }
        if self.by_category:
            category_orders = {"Activity Category": [
                e.value for e in ActivityCategoryEnum.get_ordered()]}
        fig = px.timeline(df,
                          x_start="Start Date",
                          x_end="End Date",
                          y=show_key,
                          color="Activity Category",
                          title=self.title,
                          # text="Activity",
                          category_orders=category_orders
                          )
        # fig.update_yaxes(categoryorder="total ascending")
        for shape in fig['data']:
            shape['opacity'] = 0.75

        # Extract milestones
        milestones = df[df['Activity Type'] ==
                        ActivityTypeEnum.MILESTONE.value]

        # Add scatter plot for milestones
        if not milestones.empty:
            for _, milestone in milestones.iterrows():
                fig.add_trace(go.Scatter(
                    x=[milestone['Start Date']],
                    y=[milestone[show_key]],
                    mode='markers',
                    marker=dict(symbol='star', size=12, color='red'),
                    text=milestone['Activity'],
                    textposition='top center',
                    name='Milestone'
                ))

        # Extract milestones
        dependencies = df[df['Activity Type'] ==
                          ActivityTypeEnum.DEPENDENCY.value]

        # Add scatter plot for milestones
        if not dependencies.empty:
            for _, dependency in dependencies.iterrows():
                fig.add_trace(go.Scatter(
                    x=[dependency['Start Date']],
                    y=[dependency[show_key]],
                    mode='markers',
                    marker=dict(symbol='diamond', size=12, color='blue'),
                    text=dependency['Activity'],
                    textposition='top center',
                    name='Dependency'
                ))

        fig.update_layout(xaxis_title="Date",
                          yaxis_title="Sub Stream",
                          showlegend=True)
        # fig.show()
        return fig
