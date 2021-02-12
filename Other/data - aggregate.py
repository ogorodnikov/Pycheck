# https://py.checkio.org/mission/reverse-every-ascending/publications/veky/python-3/lion-in-cairo/?ordering=most_voted&filtering=all

# Of course it can be in one line and unreadable but first, I want to see its magnificence.
# I didn't thought about a general "*my_args, **my_kwargs" before tonight.

# Since we are doing the best decorator ever, we have to make it right! Even with documentation.
import collections
from functools import wraps


def aggregate(function, *my_args, **my_kwargs):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            res = f(*args, **kwargs)
            return function(res, *my_args, **my_kwargs)

        return wrapper

    return decorator


# Examples:
@aggregate(''.join)  # and not some @join('')
@aggregate(sorted, key=len, reverse=True)
@aggregate(next, None)
@aggregate(sum, [])  # to sum lists or ...
@aggregate(max, key=sum, default=0)
@aggregate(collections.Counter)
@aggregate(list.count, 0)  # count 0 in result
@aggregate(lambda res: set(map(len, res)))
# A test:
@aggregate(sorted, key=len)
def func(m, n, L, a, b):
    """ A random function """
    import random
    for _ in range(random.randint(m, n)):
        yield [random.choice(L) for _ in range(random.randint(a, b))]

# >>> func(3, 7, range(1,15), 2, 10)
# [[5, 11], [14, 12, 1, 7, 1, 2], [13, 9, 10, 4, 8, 14], [3, 11, 3, 13, 3, 8, 5], [5, 3, 13, 10, 11, 5, 5]]
