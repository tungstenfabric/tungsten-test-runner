"""
Tungsten Test Scheduler

This class represents an asynchronous task scheduler and executor model
used for running tests in parallel.

ScheduledTask represents a unit of work - it encapsulates the execution
of the test, as well as post-processing results - writing console output
to the file, generating reports, processing any core dumps from crashed
programs.

ScheduledTaskGroup wraps a set of ScheduledTasks, abstracting grouping
of the tests - that allows us to run some tests in succession instead
of in parallel, either by disabling parallel run in the driver configuration
for the module, or by grouping them in the underlying test runner.

AsyncWorker abstracts the actual execution of the task itself, running each
one of its scheduled tasks in succession.

Scheduler is responsible for high-level test scheduling, controlling a number
of currently running tasks based on its configuration.
"""

import asyncio
import uuid


class TaskResult(object):
    stdout : bytes = None
    stderr : bytes = None
    return_code : int = None


class Task(object):
    pass


class TaskGroup(object):
    """A group of asynchronous tasks

    This is used to abstract parallel and sequential tasks.
    """
    pass


class AsyncWorker(object):
    """Executes tasks asynchronously"""
    pass


class Scheduler(object):
    """Handles task execution scheduling and result processing"""
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.queues = {}
        self.finished_tasks = []

    def schedule_task_group(self, task_group: TaskGroup) -> uuid.UUID:
        """Schedule a given TaskGroup.

        Schedules the given task group for execution, returning an associated
        UUID that can be used to query status, or cancel the task.
        """
        pass

    def unschedule_task_group(self, task_group_id: uuid.UUID) -> None:
        pass

    def execute_tasks(self) -> None:
        pass

    async def get_task_result(self, task_uuid) -> TaskResult:
        """Wait until task completes and return its details"""
