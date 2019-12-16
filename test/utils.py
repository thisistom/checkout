"""
Module providing some helpful utility functions.
"""
import sys
from contextlib import contextmanager
from StringIO import StringIO


@contextmanager
def captureOutput():
    """
    Context manager to temporarily override stdout + stderr, to capture output.

    Use like this:

        with captureOutput() as (out, err):
            foo()

        output = out.getvalue().strip()
        self.assertEqual(output, 'my expected output')
    """
    newOut, newErr = StringIO(), StringIO()
    oldOut, oldErr = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = newOut, newErr
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = oldOut, oldErr


