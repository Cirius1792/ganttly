# gantt_chart_aggregator.py

import plotly.graph_objects as go


class GanttChartAggregator:
    def __init__(self):
        self.figures = []

    def add_chart(self, chart: go.Figure):
        self.figures.append(chart)

    def save_to_file(self, output_file: str):
        with open(output_file, 'w', encoding="utf-8") as f:
            f.write('<html><head><title>Gantt Charts</title></head><body>\n')
            for chart_html in self.figures:
                f.write(chart_html.to_html(full_html=False))
                f.write('<hr>\n')  # Separate each chart with a horizontal line
            f.write('</body></html>\n')
