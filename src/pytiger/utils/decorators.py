# -*- coding: utf-8 -*-

# class cached_property is
# Copyright (c) Django Software Foundation and individual contributors.
# All rights reserved.
# License: BSD
# Source: django.utils.functional.cached_property
class cached_property(object):
    """
    .. versionadded:: 1.0.0

    Decorator that converts a method with a single self argument into a
    property cached on the instance.

    Optional ``name`` argument allows you to make cached properties of other
    methods. (e.g.  url = cached_property(get_absolute_url, name='url') )
    """
    # This entire class was obtained from Django (django/util/functional.py),
    # which is licensed under a 3-clause BSD license.
    # Copyright (c) Django Software Foundation and individual contributors.
    def __init__(self, func, name=None):
        self.func = func
        self.__doc__ = getattr(func, '__doc__')
        self.name = name or func.__name__

    def __get__(self, instance, type=None):
        if instance is None:
            return self
        res = instance.__dict__[self.name] = self.func(instance)
        return res
