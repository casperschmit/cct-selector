import itertools


def zip_with_scalar(l, o):
    return zip(l, itertools.repeat(o))
