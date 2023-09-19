import datetime
import time
from multiprocessing import freeze_support

from flask import Flask

from MLTasks.ml_task_1 import run_ml_task
from utils.dask_wrapper import DaskWrapper

app = Flask('manousos')


def main():
    with DaskWrapper().dask_client() as client:
        start_time = time.monotonic()

        run_ml_task(client=client, examples=2_000_000, features=1_000)
        end_time = time.monotonic()
        print(datetime.timedelta(seconds=end_time - start_time))


if __name__ == '__main__':
    freeze_support()
    main()
