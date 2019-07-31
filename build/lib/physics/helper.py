"""
Some helpful functions for the Physics Package
"""
from physics.value import Value


def assert_value(test):
    """
    Asserts that the test input is a Value class

    Args:
        test: The unknown type

    Returns:

    """
    assert isinstance(test, Value), 'The object {0} is of type {1}, but should be type Value.'.format(test, type(test))
