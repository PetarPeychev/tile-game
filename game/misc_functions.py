from sys import getrecursionlimit, setrecursionlimit
from contextlib import contextmanager

@contextmanager
def recursionlimit(n=1000):
	rec_limit = getrecursionlimit()
	setrecursionlimit(n)
	yield
	setrecursionlimit(rec_limit)
