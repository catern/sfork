#include "stdlib.h"
#include "stdio.h"
#include "sfork.h"
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <unistd.h>
#include <err.h>

int sfork_fib(int n) {
    sfork();
    int ret;
    if (n == 0) {
        ret = 0;
    } else if (n == 1) {
        ret = 1;
    } else {
        ret = sfork_fib(n-1) + sfork_fib(n-2);
    }
    sfork_exit(0);
    return ret;
}

int fib(int n) {
    int ret;
    if (n == 0) {
        ret = 0;
    } else if (n == 1) {
        ret = 1;
    } else {
        ret = sfork_fib(n-1) + sfork_fib(n-2);
    }
    return ret;
}

void test_fib() {
    int const max = 10;
    for (int i = 0; i < max; i++) {
        int ret, sfork_ret;
        ret = fib(i);
        sfork_ret = fib(i);
        if (ret != sfork_ret) {
            printf("fib(%d) [%d] != sfork_fib(%d) [%d]\n", i, ret, i, sfork_ret);
            exit(1);
        }
    }
}

void test_exec() {
    sfork();
    char *args[4] = {"sh", "-c", "true", 0};
    int child_pid = sfork_execveat(AT_FDCWD, "/bin/sh", args, NULL, 0);
    if (child_pid < 0) {
        err(1, "sfork_execveat(AT_FDCWD, \"/bin/sh\", args, NULL, 0);");
    }
    int wstatus;
    if (waitpid(child_pid, &wstatus, 0) < 0) {
        err(1, "waitpid(child_pid, &wstatus, 0)");
    };
    if (!(WIFEXITED(wstatus) && WEXITSTATUS(wstatus) == 0)) {
        errx(1, "some kind of problem with /bin/sh or true or something");
    }
}

int main() {
    // test_fib();
    test_exec();
}
