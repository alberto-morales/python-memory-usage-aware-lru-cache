# python-memory-usage-aware-lru-cache

##Memory-usage-aware LRU Cache function decorator

A modification of the builtin ``functools.lru_cache`` decorator that takes an
additional keyword argument, ``used_memory_max_size``. The cache is considered full
if the cache memory size is higher than ``used_memory_max_size`` bytes of memory.
If ``used_memory_max_size`` is set, then ``maxsize`` has no effect.
Uses the ``sys.getsizeof`` function to get the object usage memory.

Derived from a previous [gist](https://gist.github.com/wmayner/0245b7d9c329e498d42b) from [William Mayner](http://www.willmayner.com/)