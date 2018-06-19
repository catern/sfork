import unittest
import sfork
from sfork._raw import lib
from pathlib import Path

sh = Path("/bin/sh")

class TestException(Exception):
    pass

class TestSfork(unittest.TestCase):
    def test_nocontext(self):
        lib.sfork()
        self.assertTrue(lib.sfork_exit(0))

    def test_exit(self):
        with sfork.subprocess() as subproc:
            subproc.exit(0)
        self.assertIsNotNone(subproc.pid)

    def test_exit_forced(self):
        with sfork.subprocess() as subproc:
            pass
        self.assertIsNotNone(subproc.pid)

    def test_exit_exception(self):
        with self.assertRaises(TestException):
            with sfork.subprocess() as subproc1:
                with sfork.subprocess() as subproc2:
                    raise TestException
        self.assertIsNotNone(subproc1.pid)
        self.assertIsNotNone(subproc2.pid)

    def test_nested_exit(self):
        with sfork.subprocess() as subproc1:
            with sfork.subprocess() as subproc2:
                subproc2.exit(0)
            subproc1.exit(0)
        self.assertIsNotNone(subproc1.pid)
        self.assertIsNotNone(subproc2.pid)

    def test_exec(self):
        with sfork.subprocess() as subproc:
            subproc.exec(sh, ["sh", "-c", "true"])
        self.assertIsNotNone(subproc.pid)

    def test_nested_exec(self):
        with sfork.subprocess() as subproc1:
            with sfork.subprocess() as subproc2:
                subproc2.exec(sh, ["sh", "-c", "true"])
            subproc1.exec(sh, ["sh", "-c", "true"])
        self.assertIsNotNone(subproc1.pid)
        self.assertIsNotNone(subproc2.pid)

    # We can't do much more testing than this, because sfork doesn't
    # provide a clean interface for waiting on subprocesses, and I
    # don't want to use waitpid. We use supervise to do waiting on
    # subprocesses, and further test this in that package.
