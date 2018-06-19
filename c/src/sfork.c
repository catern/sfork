#define _GNU_SOURCE
#include <sys/types.h>
#include <sys/signal.h>
#include <unistd.h>
#include <stdint.h>
#include <sched.h>
#include <setjmp.h>

__thread void* sfork_stack_pointer = NULL;

/* Pass the stack pointer as an argument so we don't have to access
 * thread local storage from assembly */
int sfork_asm_clone(void **stack_pointer_p,
		    unsigned long flags, void *child_stack,
		    int *ptid, int *ctid,
		    unsigned long newtls);
int sfork_asm_exit(void **stack_pointer_p, int status);
int sfork_asm_execveat(void **stack_pointer_p,
                       int dirfd, const char* pathname, char *const argv[],
                       char *const envp[], int flags);

int sfork_clone(unsigned long flags, void *child_stack,
		int *ptid, int *ctid,
		unsigned long newtls) {
    /* calling sfork_asm_clone without CLONE_VFORK will break, so we force it on. */
    return sfork_asm_clone(&sfork_stack_pointer, flags|CLONE_VFORK, child_stack, ptid, ctid, newtls);
};

int sfork() {
    return sfork_clone(CLONE_VFORK|CLONE_VM|SIGCHLD, NULL, NULL, NULL, 0);
};

int sfork_exit(int status) {
    return sfork_asm_exit(&sfork_stack_pointer, status);
};

int sfork_execveat(int dirfd, const char* pathname, char *const argv[],
                   char *const envp[], int flags) {
    return sfork_asm_execveat(&sfork_stack_pointer, dirfd, pathname, argv,
                              envp, flags);
}
