# gantt_chart_generator.py

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from ganttly.dto import ActivityDTO, ActivityTypeEnum
from typing import List


class GanttChartGenerator:
    def __init__(self, activities: List[ActivityDTO]):
        self.activities = activities

    def draw_chart(self):
        df = pd.DataFrame([{
            'Sub Stream': activity.sub_stream,
            'Activity': f"{activity.activity}-{activity.activity_category}",
            'Activity Category': activity.activity_category,
            'Activity Type': activity.activity_type,
            'Start Date': activity.start_date,
            'End Date': activity.end_date,
            'Owner': activity.owner,
            'State': activity.state,
            'Notes': activity.notes
        } for activity in self.activities])

        fig = px.timeline(df,
                          x_start="Start Date",
                          x_end="End Date",
                          y="Activity",
                          color="Activity Category",
                          title="Gantt Chart",
                          text="Activity")
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(xaxis_title="Date",
                          yaxis_title="Sub Stream",
                          showlegend=True)

        # Extract milestones
        milestones = df[df['Activity Type'] == ActivityTypeEnum.MILESTONE]

        # Add scatter plot for milestones
        if not milestones.empty:
            for _, milestone in milestones.iterrows():
                fig.add_trace(go.Scatter(
                    x=[milestone['Start Date']],
                    y=[milestone['Activity']],
                    mode='markers+text',
                    marker=dict(symbol='star', size=12, color='red'),
                    text=milestone['Activity'],
                    textposition='top center',
                    name='Milestone'
                ))

        fig.show()
