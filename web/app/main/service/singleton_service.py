from __future__ import annotations

import pprint
from threading import Lock, Thread
from typing import Optional
from weakref import WeakValueDictionary

class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """

    _instance: Optional[Singleton] = WeakValueDictionary()

    _lock: Lock = Lock()
    """
    We now have a lock object that will be used to synchronize threads during
    first access to the Singleton.
    """

    def __call__(cls, *args, **kwargs):
        # Now, imagine that the program has just been launched. Since there's no
        # Singleton instance yet, multiple threads can simultaneously pass the
        # previous conditional and reach this point almost at the same time. The
        # first of them will acquire lock and will proceed further, while the
        # rest will wait here.
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if not cls._instance:
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Singleton(metaclass=SingletonMeta):
    value: str = None
    """
    We'll use this property to prove that our Singleton really works.
    """

    def __init__(self, value: str) -> None:
        self.value = value

    def some_business_logic(self):
        """
        Finally, any singleton should define some business logic, which can be
        executed on its instance.
        """


class SingletonIDS(metaclass=SingletonMeta):
    __singleton_ids: set = set()

    def add(self, singleton_id):
        self.__singleton_ids.add(singleton_id)

    @property
    def ids(self):
        return self.__singleton_ids

    def is_exists(self, singleton_id = None):
        return singleton_id in self.__singleton_ids


class SingletonWithIDMeta(type):
    """
    This is a thread-safe implementation of Singleton with ID.
    """

    _instance: Optional[Singleton] = None

    _lock: Lock = Lock()
    """
    We now have a lock object that will be used to synchronize threads during
    first access to the Singleton.
    """

    def __call__(cls, *args, **kwargs):
        # Now, imagine that the program has just been launched. Since there's no
        # Singleton instance yet, multiple threads can simultaneously pass the
        # previous conditional and reach this point almost at the same time. The
        # first of them will acquire lock and will proceed further, while the
        # rest will wait here.
        with cls._lock:
            # Get the singleton ids container
            singleton_ids = SingletonIDS()
            singleton_id = cls.__get_singleton_id(args, kwargs)
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if not cls._instance or not singleton_ids.is_exists(singleton_id):
                singleton_ids.add(singleton_id)
                cls._instance = super().__call__(*args, **kwargs)
                cls._instance.__dict__.update({"__id": singleton_id})
        return cls._instance

    def __get_singleton_id(self, *args, **kwargs):
        singleton_id = None
        # Check arguments if there is first arguments for singleton id
        if len(args[0]):
            singleton_id = args[0][0]
        elif 'singleton_id' in kwargs:
            singleton_id = kwargs.get('singleton_id')

        if not singleton_id:
            singleton_id = "id"
        return f"{self.__name__}_{singleton_id}"


class SingletonState(metaclass=SingletonWithIDMeta):
    __state: str = None

    def __init__(self, singleton_id = None, **kwargs):
        if 'state' in kwargs:
            self.__state = kwargs.pop('state')

    @property
    def state(self):
        return self.__state

    def set_state(self, state):
        self.__state = state
        return self

def test_singleton(name: str, state : str) -> None:
    singleton = SingletonState(name)
    if state:
        singleton.set_state(state)
        pass
    pprint.pprint((singleton, singleton.__dict__))

