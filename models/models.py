import logging

from mongoengine import connect, DynamicDocument, StringField, FloatField

try:
    db = connect(db='dask',
                 host='localhost' + ':' + '27017',
                 username='dask',
                 password='dask')
except Exception as e:
    logging.error(e)


class DaskTask(DynamicDocument):
    key = StringField(default=None, null=True)
    worker = StringField(default=None, null=True)

    started = StringField(default='')
    started_waiting = StringField(default='')
    became_ready = StringField(default='')
    started_execution = StringField(default='')
    to_memory = StringField(default='')
    released = StringField(default='')
    finished = StringField(default='')

    idle_time = FloatField(default=0.0)
    waiting_time = FloatField(default=0.0)
    execution_time = FloatField(default=0.0)

    meta = {'indexes': ['key']}


class IdleTime(DynamicDocument):
    timestamp = FloatField(default=0.0)  # timestamp
    value = FloatField(default=0.0)  # timestamp

    meta = {'max_documents': 1000, 'max_size': 10_000_000}


class WaitingTime(DynamicDocument):
    timestamp = FloatField(default=0.0)  # timestamp
    value = FloatField(default=0.0)  # timestamp

    meta = {'max_documents': 1000, 'max_size': 10_000_000}


class ExecutionTime(DynamicDocument):
    timestamp = FloatField(default=0.0)  # timestamp
    value = FloatField(default=0.0)  # timestamp

    meta = {'max_documents': 1000, 'max_size': 10_000_000}
