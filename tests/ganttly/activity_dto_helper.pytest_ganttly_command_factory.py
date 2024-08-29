from unittest import TestCase


from parameterized import parameterized

from ganttly.gantly_command import *

class TestCopilotCommandFactory(TestCase):

    @parameterized.expand( [
        (GanttlyConfiguration(), CreateGanttCommand),
        (GanttlyConfiguration(per_stream=True), CreateSubStreamGanttCommand),
        (GanttlyConfiguration(group_per_activity=True), CreateActivityGanttCommand),
        (GanttlyConfiguration(per_stream=True, group_per_activity=True), CreateSubStreamPerActivityGanttCommand),
        ])
    def test_create_command(self, configuration, expected_command):
        command_factory = GanttlyCommandFactory("file_path", configuration)
        self.assertIsInstance(command_factory.create(), expected_command)
