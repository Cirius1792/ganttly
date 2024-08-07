# gantt_chart_generator.py

from dataclasses import dataclass
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from ganttly.dto import ActivityDTO, ActivityTypeEnum
from typing import List


@dataclass
class GantRowDTO:
    sub_stream: str
    activity: str
    activity_category: str
    activity_type: str
    start_date: datetime
    end_date: datetime


def to_gantt_row(activity: ActivityDTO) -> GantRowDTO:
    return GantRowDTO(
        sub_stream=activity.sub_stream,
        activity=f"{activity.sub_stream}-{activity.activity}-{activity.activity_category}",
        activity_category=activity.activity_category,
        activity_type=activity.activity_type.value,
        start_date=activity.start_date,
        end_date=activity.end_date
    )


class GanttChartGenerator:
    def __init__(self, activities: List[ActivityDTO]):
        self.activities = activities

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

    def draw_chart(self):
        self._validate_activities()

        df = pd.DataFrame([{
            'Sub Stream': activity.sub_stream,
            'Activity': activity.activity,
            'Activity Category': activity.activity_category,
            'Activity Type': activity.activity_type,
            'Start Date': activity.start_date,
            'End Date': activity.end_date,
        } for activity in map(to_gantt_row, self.activities)])

        sub_streams = df['Sub Stream'].unique()
        df = df.sort_values(by=['Sub Stream', 'Start Date'])
        fig = px.timeline(df,
                          x_start="Start Date",
                          x_end="End Date",
                          y="Activity",
                          color="Activity Category",
                          title="Gantt Chart",
                          text="Activity",
                          category_orders={"Sub Stream": df['Sub Stream']}
                          )
        fig.update_yaxes(categoryorder="total ascending")

        # Add group labels for sub streams
        for sub_stream in sub_streams:
            sub_stream_activities = df[df['Sub Stream'] == sub_stream]
            for _, row in sub_stream_activities.iterrows():
                fig.add_trace(go.Scatter(
                    x=[row['Start Date'], row['End Date']],
                    y=[row['Activity'], row['Activity']],
                    mode='lines',
                    line=dict(color='rgba(0,0,0,0)'),
                    showlegend=False
                ))

        # Extract milestones
        milestones = df[df['Activity Type'] ==
                        ActivityTypeEnum.MILESTONE.value]

        # Add scatter plot for milestones
        if not milestones.empty:
            for _, milestone in milestones.iterrows():
                fig.add_trace(go.Scatter(
                    x=[milestone['Start Date']],
                    y=[milestone['Activity']],
                    mode='markers',
                    marker=dict(symbol='star', size=12, color='red'),
                    text=milestone['Activity'],
                    textposition='top center',
                    name='Milestone'
                ))

        fig.update_layout(xaxis_title="Date",
                          yaxis_title="Sub Stream",
                          showlegend=True)
        fig.show()
