from cffi import FFI
import pkgconfig

ffibuilder = FFI()
sfork = {key: list(value) for key, value in pkgconfig.parse('sfork').items()}

# We need a bunch of constants for proper usage of _clone and _execveat.
ffibuilder.set_source(
    "sfork._raw", """
#include <unistd.h>
#include <fcntl.h>
#include <sched.h>
#include "sfork.h"

""", **sfork)

ffibuilder.cdef("""

# define CSIGNAL              ... /* Signal mask to be sent at exit.  */
# define CLONE_VM             ... /* Set if VM shared between processes.  */
# define CLONE_FS             ... /* Set if fs info shared between processes.  */
# define CLONE_FILES          ... /* Set if open files shared between processes.  */
# define CLONE_SIGHAND        ... /* Set if signal handlers shared.  */
# define CLONE_PTRACE         ... /* Set if tracing continues on the child.  */
# define CLONE_VFORK          ... /* Set if the parent wants the child to
		               	     wake it up on mm_release.  */
# define CLONE_PARENT         ... /* Set if we want to have the same
		               	     parent as the cloner.  */
# define CLONE_THREAD         ... /* Set to add to same thread group.  */
# define CLONE_NEWNS          ... /* Set to create new namespace.  */
# define CLONE_SYSVSEM        ... /* Set to shared SVID SEM_UNDO semantics.  */
# define CLONE_SETTLS         ... /* Set TLS info.  */
# define CLONE_PARENT_SETTID  ... /* Store TID in userlevel buffer
					   before MM copy.  */
# define CLONE_CHILD_CLEARTID ... /* Register exit futex and memory
					    location to clear.  */
# define CLONE_DETACHED       ... /* Create clone detached.  */
# define CLONE_UNTRACED       ... /* Set if the tracing process can't
			                force CLONE_PTRACE on this clone.  */
# define CLONE_CHILD_SETTID   ... /* Store TID in userlevel buffer in
			          	  the child.  */
# define CLONE_NEWCGROUP      ... /* New cgroup namespace.  */
# define CLONE_NEWUTS	      ... /* New utsname group.  */
# define CLONE_NEWIPC	      ... /* New ipcs.  */
# define CLONE_NEWUSER	      ... /* New user namespace.  */
# define CLONE_NEWPID	      ... /* New pid namespace.  */
# define CLONE_NEWNET	      ... /* New network namespace.  */
# define CLONE_IO	      ... /* Clone I/O context.  */

#define AT_FDCWD		...     /* Special value used to indicate
                                           openat should use the current
                                           working directory. */
#define AT_SYMLINK_NOFOLLOW	...     /* Do not follow symbolic links.  */
#define AT_EMPTY_PATH		...	/* Allow empty relative pathname */

int sfork();
int sfork_exit(int status);
int sfork_clone(unsigned long flags, void *child_stack,
		int *ptid, int *ctid,
		unsigned long newtls);
int sfork_execveat(int dirfd, const char* pathname, char *const argv[],
                   char *const envp[], int flags);
""")
