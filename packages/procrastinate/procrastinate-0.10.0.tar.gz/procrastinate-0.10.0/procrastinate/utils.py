import asyncio
import functools
import importlib
import logging
import types
from typing import Any, Awaitable, Iterable, Optional, Type, TypeVar

from procrastinate import exceptions

T = TypeVar("T")

logger = logging.getLogger(__name__)


def load_from_path(path: str, allowed_type: Type[T]) -> T:
    """
    Import and return then object at the given full python path.
    """
    if "." not in path:
        raise exceptions.LoadFromPathError(f"{path} is not a valid path")
    module_path, name = path.rsplit(".", 1)
    try:
        module = importlib.import_module(module_path)
    except ImportError as exc:
        raise exceptions.LoadFromPathError(str(exc)) from exc

    try:
        imported = getattr(module, name)
    except AttributeError as exc:
        raise exceptions.LoadFromPathError(str(exc)) from exc

    if not isinstance(imported, allowed_type):
        raise exceptions.LoadFromPathError(
            f"Object at {path} is not of type {allowed_type.__name__} "
            f"but {type(imported).__name__}"
        )

    return imported


def import_all(import_paths: Iterable[str]) -> None:
    """
    Given a list of paths, just import them all
    """
    for import_path in import_paths:
        logger.debug(
            f"Importing module {import_path}",
            extra={"action": "import_module", "module_name": import_path},
        )
        importlib.import_module(import_path)


def add_sync_api(cls: Type) -> Type:
    """
    Applying this decorator to a class with async methods named "<name>_async"
    will create a sync version named "<name>" of these methods that performs the same
    thing but synchronously.
    """
    # Iterate on all class attributes
    for attribute_name in dir(cls):
        wrap_one(cls=cls, attribute_name=attribute_name)

    return cls


# https://github.com/sphinx-doc/sphinx/issues/7559
SYNC_ADDENDUM = """

        This method is the synchronous counterpart of `{}`.
        Because of a slight issue in automatic doc generation, it
        is shown here as "async", but this function is synchronous.
"""

ASYNC_ADDENDUM = """

        This method is the asynchronous counterpart of `{}`.
"""


def wrap_one(cls: Type, attribute_name: str):
    suffix = "_async"
    if attribute_name.startswith("_") or not attribute_name.endswith(suffix):
        return

    # Methods are descriptors so using getattr here will not give us the real method
    cls_vars = vars(cls)
    attribute = cls_vars[attribute_name]

    # If method is a classmethod or staticmethod, its real function, that may be
    # async, is stored in __func__.
    wrapped = getattr(attribute, "__func__", attribute)

    # Keep only async def methods
    if not asyncio.iscoroutinefunction(wrapped):
        return

    attribute.__doc__ = attribute.__doc__ or ""

    # Create a wrapper that will call the method in a run_until_complete
    @functools.wraps(wrapped)
    def wrapper(*args, **kwargs):
        awaitable = wrapped(*args, **kwargs)
        return sync_await(awaitable=awaitable)

    sync_name = attribute_name[: -len(suffix)]
    attribute.__doc__ += ASYNC_ADDENDUM.format(sync_name)

    final_wrapper: Any
    if isinstance(attribute, types.FunctionType):  # classic method
        final_wrapper = wrapper
    elif isinstance(attribute, classmethod):
        final_wrapper = classmethod(wrapper)
    elif isinstance(attribute, staticmethod):
        final_wrapper = staticmethod(wrapper)
    else:
        raise ValueError(f"Invalid object of type {type(attribute)}")

    # Save this new method on the class
    name = wrapper.__name__ = sync_name
    final_wrapper.__doc__ += SYNC_ADDENDUM.format(attribute_name)
    setattr(cls, name, final_wrapper)


def sync_await(awaitable: Awaitable[T]) -> T:
    """
    Given an awaitable, awaits it synchronously. Returns the result after it's done.
    """

    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(awaitable)


def causes(exc: Optional[BaseException]):
    """
    From a single exception with a chain of causes and contexts, make an iterable
    going through every exception in the chain.
    """
    while exc:
        yield exc
        exc = exc.__cause__ or exc.__context__
