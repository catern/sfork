#include "sfork.h"
#include "stdio.h"

int main() {
    printf("in the parent, pid: %d\n", getpid());
    sfork();
    printf("in the child, pid: %d\n", getpid());
    int ret = sfork_exit(0);
    printf("in the parent, pid: %d\n", getpid());
    printf("in the parent, child pid was: %d\n", ret);
}

/* Output:
in the parent, pid: 51250
in the child, pid: 51264
in the parent, pid: 51250
in the parent, child pid was: 51264
 */
