# -*- coding: utf-8 -*-

from .decorators import cached_property, singleton
import unittest


class TestCachedProperty(unittest.TestCase):
    # Adapted from Django
    # Copyright (c) Django Software Foundation and individual contributors.
    # All rights reserved.
    # License: BSD
    # Source: tests/utils_tests/test_functional.py
    def test_cached_property(self):
        """
        Test that cached_property caches its value,
        and that it behaves like a property
        """

        class A(object):

            @cached_property
            def value(self):
                """Here is the docstring..."""
                return 1, object()

            def other_value(self):
                return 1

            other = cached_property(other_value, name='other')

        # docstring should be preserved
        self.assertEqual(A.value.__doc__, "Here is the docstring...")

        a = A()

        # check that it is cached
        self.assertEqual(a.value, a.value)

        # check that it returns the right thing
        self.assertEqual(a.value[0], 1)

        # check that state isn't shared between instances
        a2 = A()
        self.assertNotEqual(a.value, a2.value)

        # check that it behaves like a property when there's no instance
        self.assertTrue(isinstance(A.value, cached_property))

        # check that overriding name works
        self.assertEqual(a.other, 1)
        self.assertTrue(callable(a.other_value))


class TestSingleton(unittest.TestCase):
    """
    Test that objects decorated singleton are
    indeed singletons.

    This is a very basic function test, but could
    probably be more intelligent.
    """

    @singleton
    class TestSingletonObject():
        def __init__(self, test_string=""):
            self.test_string = test_string

    def test_singleton_object(self):
        self.TestSingletonObject("my test string")
        B = self.TestSingletonObject("otherstring")
        self.assertTrue(B.test_string, "my test string")
