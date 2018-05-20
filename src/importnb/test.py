
# coding: utf-8

"""# Load and test notebooks

New ideas may include tests in a notebook.  The `importnb.test.Test` context will `doctest` and `unittest` a notebook.

    >>> from importnb import Test
    >>> assert Test
"""


try:
    from .loader import Notebook, export
except:
    from loader import Notebook, export

from unittest import TestProgram, TestCase
from doctest import DocTestSuite

__file__ = globals().get("__file__", "test.ipynb")


def testmod(
    module, extras="", doctest=True, exit=True, verbosity=1, failfast=None, catchbreak=None
):
    if doctest:
        attach_doctest(module)
    try:
        TestProgram(
            module,
            argv=" ".join(("discover", extras)).split(),
            exit=exit,
            verbosity=verbosity,
            failfast=failfast,
            catchbreak=catchbreak,
        )
    except SystemExit:
        ...
    return module


def attach_doctest(module):
    print(module)

    def load_tests(loader, tests, ignore):
        tests.addTests(DocTestSuite(module))
        return tests

    module.load_tests = load_tests
    return module


class Test(Notebook):

    def exec_module(self, module):
        super().exec_module(module)
        testmod(module)


class _test(TestCase):

    def test_importnb_test(self):
        assert True


if __name__ == "__main__":
    export("test.ipynb", "../importnb/test.py")
    __import__("doctest").testmod(Notebook.from_filename("loader.ipynb"))
    m = Test.from_filename(__file__)
    testmod(m, "-f")
