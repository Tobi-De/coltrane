import logging
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from typing import Dict, List


logger = logging.getLogger(__name__)


def dict_merge(
    source: Dict,
    destination: Dict,
    destination_overrides_source=False,
    path: List[str] = None,
) -> Dict:
    """
    Deep merge two dictionaries.

    Shamelessly swiped from https://stackoverflow.com/a/7205107.
    """

    if path is None:
        path = []

    for key in destination:
        if key in source:
            if isinstance(source[key], dict) and isinstance(destination[key], dict):
                dict_merge(
                    source=source[key],
                    destination=destination[key],
                    destination_overrides_source=destination_overrides_source,
                    path=path + [str(key)],
                )
            elif source[key] == destination[key]:
                pass  # same leaf value
            else:
                if destination_overrides_source:
                    source[key] = destination[key]
                else:
                    raise Exception("Conflict at %s" % ".".join(path + [str(key)]))
        else:
            source[key] = destination[key]

    return source


def threadpool(f, executor=None):
    """
    A decorator to convert a regular function so that it gets run in another thread.

    ```python
    # does not block, returns Future object
    future = some_long_running_process()

    # this blocks, waiting for the result
    result = future.result()
    ```

    More details: https://stackoverflow.com/a/14331755
    """

    @wraps(f)
    def wrap(*args, **kwargs):
        return (executor or ThreadPoolExecutor()).submit(f, *args, **kwargs)

    return wrap
