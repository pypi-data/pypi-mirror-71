# Standard library
from contextvars import (
    ContextVar,
)
from typing import (
    Any,
    Callable,
    List,
    Tuple,
)

# Local libraries
from tracers.containers import (
    Frame,
    LoopSnapshot,
)

LEVEL: ContextVar[int] = \
    ContextVar('LEVEL', default=0)
LOOP_SNAPSHOTS: ContextVar[List[LoopSnapshot]] = \
    ContextVar('LOOP_SNAPSHOTS')
STACK: ContextVar[List[Frame]] = \
    ContextVar('STACK')
TRACING: ContextVar[bool] = \
    ContextVar('TRACING', default=True)

ALL: Tuple[Tuple[ContextVar, Callable[[], Any]], ...] = (
    (LEVEL, lambda: 0),
    (LOOP_SNAPSHOTS, lambda: []),
    (STACK, lambda: []),
    (TRACING, lambda: True),
)


def reset_all():
    for var, default_value_creator in ALL:
        reset_one(var, default_value_creator)


def reset_one(
    contextvar: ContextVar,
    default_value_creator: Callable[[], Any],
) -> None:
    obj = contextvar.get(None)

    if obj:
        if isinstance(obj, list):
            # Delete all elements
            obj.clear()
        elif isinstance(obj, (bool, int)):
            # This never leaks
            pass
        else:
            raise TypeError(f'Missing handler for type: {type(obj)}')

    # Delete reference
    del obj

    # Re-initialize to its default value
    contextvar.set(default_value_creator())
