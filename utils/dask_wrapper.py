from contextlib import contextmanager

from distributed import LocalCluster, Client, PipInstall

from plugins.plugins import get_median_idle_time, get_median_waiting_time, get_median_execution_time, TaskStatusPlugin, DBPlugin

worker_plugin_1 = PipInstall(packages=["prometheus-client"])
task_status_plugin = TaskStatusPlugin()
db_sched_plugin = DBPlugin()


class DaskWrapper:
    client = None
    cluster = None

    def __init__(self):
        pass

    @contextmanager
    def dask_client(self):
        self.cluster = LocalCluster(
            scheduler_port=8787,
            # n_workers=int(0.9 * mp.cpu_count()),
            # n_workers=10,
            # processes=False,
            # threads_per_worker=2, memory_limit='3GB',
            # ip='tcp://localhost:5000'
        )
        self.client = Client(self.cluster)
        try:
            self.cluster.adapt(minimum=1, maximum=10)
            # self.cluster.adapt(maximum=10, maximum_memory='20GB')
            self.client.register_worker_plugin(worker_plugin_1)
            self.client.register_scheduler_plugin(db_sched_plugin)
            self.client.register_worker_plugin(task_status_plugin)

            yield self.client
        except Exception as e:
            print(e)
            raise
        finally:
            self.client.close()
            self.cluster.close()


def get_number_of_workers(self) -> dict:
    n = len(self.client.scheduler_info()['workers'])
    return {'workers': n}


def scale_cluster(self, workers: int) -> dict:
    self.cluster.scale(n=int(workers))
    return {'workers': workers}


def scale_plus_one(self):
    n = len(self.client.scheduler_info()['workers'])
    self.cluster.scale(n + 1)
    return {'workers': n + 1}


def scale_minus_one(self):
    n = len(self.client.scheduler_info()['workers'])
    self.cluster.scale(n - 1)
    return {'workers': n - 1}


def scale_times_two(self):
    n = len(self.client.scheduler_info()['workers'])
    self.cluster.scale(2 * n)
    return {'workers': 2 * n}


def scale_by_two(self):
    n = len(self.client.scheduler_info()['workers'])
    self.cluster.scale(int(n / 2))
    return {'workers': int(n / 2)}


def profile(self):
    print(self.client.profile())
    return {'key': 'value'}


@staticmethod
def idle_time():
    res = get_median_idle_time()
    return {'idle_time': res}


@staticmethod
def waiting_time():
    res = get_median_waiting_time()
    return {'waiting_time': res}


@staticmethod
def execution_time():
    res = get_median_execution_time()
    return {'execution_time': res}
