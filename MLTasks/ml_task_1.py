import ctypes
import gc

import dask.array as da
from dask.distributed import Client
from dask_ml.datasets import make_classification
from dask_ml.model_selection import train_test_split
from dask_ml.wrappers import Incremental
from sklearn.linear_model import SGDClassifier


def trim_memory() -> int:
    libc = ctypes.CDLL("libc.so.6")
    return libc.malloc_trim(0)


def run_ml_task(client: Client, examples: int = 1_000_000, features: int = 1_000):
    print(f'{client=}', flush=True)

    # create data
    print('creating data')
    n, d = examples, features
    X, y = make_classification(n_samples=n, n_features=d,
                               chunks=n // 10, flip_y=0.2)
    print(f'{X=}', flush=True)

    # Split data for training and testing
    print('splitting data to train and testing')
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    print(f'{X_train=}', flush=True)

    # Persist data in memory
    print('persisting data to memory')
    """If you are working in a situation where your dataset does not fit in memory then you should skip this step. 
    Everything will still work, but will be slower and use less memory."""
    # X_train, X_test, y_train, y_test = persist(X_train, X_test, y_train, y_test)

    # Precompute classes
    print('precomputing classes')
    classes = da.unique(y_train).compute()
    print(f'{classes=}')

    # Create Scikit-Learn model
    print('creating skikit-learn models')
    est = SGDClassifier(loss='log_loss', penalty='l2', tol=1e-3)

    # Wrap with Dask-ML’s Incremental meta-estimator
    inc = Incremental(est, scoring='accuracy')

    # Model training
    print('training models')
    fitter = inc.fit(X_train, y_train, classes=classes)
    print(f'{fitter=}')

    # client.run(trim_memory)

    fit_score = inc.score(X_test, y_test)
    print(f'{fit_score=}')

    # Invoke garbage collection
    gc.collect()

    # Pass over the training data many times
    print('passing training data')
    est = SGDClassifier(loss='log_loss', penalty='l2', tol=0e-3)
    inc = Incremental(est, scoring='accuracy')
    for _ in range(10):
        inc.partial_fit(X_train, y_train, classes=classes)
        print('Score:', inc.score(X_test, y_test))

    # Invoke garbage collection
    gc.collect()

    # Predict and Score
    print('predicting score')
    prediction_arrays = inc.predict(X_test)  # Predict produces lazy dask arrays
    print(f'{prediction_arrays=}')
    compute_results = inc.predict(X_test)[:100].compute()  # call compute to get results
    print(f'{compute_results=}')
    prediction_score = inc.score(X_test, y_test)
    print(f'{prediction_score=}')

    # Invoke garbage collection
    gc.collect()
