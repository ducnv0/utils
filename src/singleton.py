from threading import Lock


class SingletonMeta(type):

    _instances = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
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
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

# Double-checked locking could be used to reduce the overhead of acquiring a lock
# by testing the locking criterion before acquiring the lock
# But sometimes, it can be unsafe to use
# (https://www.wikiwand.com/en/Double-checked_locking)
# (https://www.cs.cornell.edu/courses/cs6120/2019fa/blog/double-checked-locking/)

# def __call__(cls, *args, **kwargs):
#     # checking the locking criterion before acquiring the lock
#     if cls not in cls._instances:
#         with cls._lock:
#             if cls not in cls._instances:
#                 instance = super().__call__(*args, **kwargs)
#                 cls._instances[cls] = instance
#     return cls._instances[cls]