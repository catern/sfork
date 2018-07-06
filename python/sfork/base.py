from contextlib import contextmanager
from sfork._raw import lib, ffi # type: ignore
import os
import typing as t

AT_FDCWD = lib.AT_FDCWD

def throw_on_error(ret) -> int:
    if ret < 0:
        err = -ret
        raise OSError(err, os.strerror(err))
    else:
        return ret

def _to_null_terminated_string_array(args: t.List[bytes]) -> t.Any:
    """Both the strings in the array, and the array itself, are null terminated."""
    return ffi.new('char *const[]', [ffi.new('char[]', arg) for arg in args] + [ffi.NULL])

def to_bytes(arg: t.Union[str, bytes]) -> bytes:
    if isinstance(arg, str):
        return bytes(arg, 'utf8')
    else:
        return arg

def serialize_environ(**kwargs) -> t.List[bytes]:
    ret: t.List[bytes] = []
    for key, value in kwargs.items():
        ret.append(b''.join([to_bytes(key), b'=', to_bytes(value)]))
    return ret

def sfork() -> None:
    throw_on_error(lib.sfork())

def exit(status: int) -> int:
    return throw_on_error(lib.sfork_exit(status))

def execveat(dirfd: int, pathname: bytes, argv: t.List[bytes], envp: t.List[bytes], flags: int) -> int:
    # this null-terminated-array logic is tricky to extract out into a separate function due to lifetime issues
    null_terminated_args = [ffi.new('char[]', arg) for arg in argv]
    argv = ffi.new('char *const[]', null_terminated_args + [ffi.NULL])
    null_terminated_env_vars = [ffi.new('char[]', arg) for arg in envp]
    envp = ffi.new('char *const[]', null_terminated_env_vars + [ffi.NULL])
    return throw_on_error(lib.sfork_execveat(dirfd, ffi.new('char[]', pathname), argv, envp, flags))

def clone(flags: int) -> int:
    # most of these args are quite unsafe to call from Python directly :)
    return throw_on_error(lib.sfork_clone(flags, ffi.NULL, ffi.NULL, ffi.NULL, 0))

class ProcessContext:
    """A Linux process, as a context for threads to run inside."""
    pass

main_process = ProcessContext()
# TODO would be nice to use a contextvar for this
current_process = main_process

class SubprocessContext:
    def __init__(self, process: ProcessContext, parent_process: ProcessContext) -> None:
        self.process = process
        self.parent_process = parent_process
        self.pid: t.Optional[int] = None

    def _can_syscall(self) -> None:
        if current_process is not self.process:
            raise Exception("My syscall interface is not currently operating on my process, "
                            "did you fork again and call exit/exec out of order?")
        if self.pid is not None:
            raise Exception("Already left this process")

    def exit(self, status: int) -> None:
        self._can_syscall()
        self.pid = exit(status)
        global current_process
        current_process = self.parent_process

    def exec(self, pathname: os.PathLike, argv: t.List[t.Union[str, bytes]],
             *, envp: t.Optional[t.Dict[str, str]]=None) -> None:
        self._can_syscall()
        if envp is None:
            environ = serialize_environ(**os.environ)
        else:
            environ = serialize_environ(**envp)
        self.pid = execveat(AT_FDCWD,
                            to_bytes(os.fspath(pathname)), [to_bytes(arg) for arg in argv],
                            environ, flags=0)
        global current_process
        current_process = self.parent_process

@contextmanager
def subprocess():
    # this is really contextvar-ish. but I guess it's inside an
    # explicitly passed around object in the rsyscall case. but it's
    # still the same kind of behavior. by what name is this known?
    global current_process
    parent_process = current_process
    sfork()
    current_process = ProcessContext()
    context = SubprocessContext(current_process, parent_process)
    try:
        yield context
    finally:
        if context.pid is None:
            context.exit(0)
