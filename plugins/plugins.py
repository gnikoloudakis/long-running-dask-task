import datetime
import logging
from typing import List

from distributed import Worker, get_worker
from distributed.diagnostics.plugin import SchedulerPlugin, WorkerPlugin

from models.models import DaskTask, WaitingTime, ExecutionTime, IdleTime


class TaskStatusPlugin(WorkerPlugin):
    def __init__(self):
        self.worker = None

    def setup(self, worker):
        self.worker: Worker = worker

    def transition(self, key, start, finish, *args, **kwargs):
        try:
            dask_task = DaskTask.objects(key=key).first()
            persist_changes(key=key,
                            task_instance=dask_task,
                            changes=get_task_status_based_on_state(key=key,
                                                                   start=start,
                                                                   finish=finish, task_instance=dask_task)
                            )
        except Exception as e:
            logging.error(e)


def get_task_status_based_on_state(key: str, start: str, finish: str, task_instance: DaskTask):
    # print(f"key: {key}")
    # print(f"start: {start}")
    # print(f"finish: {finish}")
    changes = {}
    if start == 'released' and finish == 'waiting':
        changes = {
            'started': datetime.datetime.now().isoformat(),
            'released': datetime.datetime.now().isoformat()
        }
    elif start == 'waiting' and finish == 'ready':
        changes = {
            'started_waiting': datetime.datetime.now().isoformat(),
        }
    elif start == 'ready' and finish == 'executing':
        changes = {
            'became_ready': datetime.datetime.now().isoformat(),
        }
    elif start == 'executing' and finish == 'memory':
        changes = {
            'started_execution': datetime.datetime.now().isoformat(),
            'waiting_time': datetime.datetime.now().timestamp() - datetime.datetime.fromisoformat(task_instance.started_waiting).timestamp(),
            'idle_time': datetime.datetime.now().timestamp() - datetime.datetime.fromisoformat(task_instance.started).timestamp()
        }
        mean_waiting_time = WaitingTime(timestamp=datetime.datetime.now().timestamp(),
                                        value=get_median_waiting_time()).save()
        mean_idle_time = IdleTime(timestamp=datetime.datetime.now().timestamp(),
                                  value=get_median_idle_time()).save()

    elif start == 'memory' and finish == 'released':
        changes = {
            'to_memory': datetime.datetime.now().isoformat(),
            'execution_time': datetime.datetime.now().timestamp() - datetime.datetime.fromisoformat(task_instance.started_execution).timestamp()
        }
        mean_execution_time = ExecutionTime(timestamp=datetime.datetime.now().timestamp(),
                                            value=get_median_execution_time()).save()
    elif start == 'released' and finish == 'forgotten':
        changes = {
            'released': datetime.datetime.now().isoformat(),
            'finished': datetime.datetime.now().isoformat(),
        }

    elif finish == 'error':
        ts = get_worker().tasks[key]
        exc_info = (type(ts.exception), ts.exception, ts.traceback)
        logging.error(
            "Error during computation of '%s'.", key,
            exc_info=exc_info
        )
    else:
        # print(f"Task with key: {key} --> State is unknown. Start: {start}, Finish: {finish}", flush=True)
        pass

    return changes


def persist_changes(key: str, task_instance: DaskTask, changes: dict):
    try:
        if task_instance:
            task_instance.update(**changes) if changes else None
        else:
            DaskTask(key=key, **changes).save() if changes else None
    except Exception as e:
        logging.error(e)


class DBPlugin(SchedulerPlugin):
    def __init__(self):
        # DaskTask.drop_collection()
        # ExecutionTime.drop_collection()
        # WaitingTime.drop_collection()
        # IdleTime.drop_collection()
        pass

    # def transition(self, key, start, finish, *args, **kwargs):
    #     if start == 'processing' and finish == 'memory':
    #         self.counter += 1
    #
    # def restart(self, scheduler):
    #     self.counter = 0


def get_median_idle_time():
    try:
        tasks: List[DaskTask] = DaskTask.objects
        idle_times = [t.idle_time for t in tasks if t.idle_time]
        return sum(idle_times) / len(idle_times) if idle_times else None
    except Exception as e:
        print(e.__str__())


def get_median_waiting_time():
    try:
        tasks: List[DaskTask] = DaskTask.objects
        waiting_times = [t.waiting_time for t in tasks if t.waiting_time]
        return sum(waiting_times) / len(waiting_times) if waiting_times else None
    except Exception as e:
        print(e.__str__())


def get_median_execution_time():
    try:
        tasks: List[DaskTask] = DaskTask.objects
        execution_times = [t.execution_time for t in tasks if t.execution_time]
        return sum(execution_times) / len(execution_times) if execution_times else None
    except Exception as e:
        print(e.__str__())
