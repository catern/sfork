#ifndef	_SFORK_H
#define	_SFORK_H	1

int sfork();
int sfork_clone(unsigned long flags, void *child_stack,
		int *ptid, int *ctid,
		unsigned long newtls);
int sfork_exit(int status);
int sfork_execveat(int dirfd, const char* pathname, char *const argv[],
                   char *const envp[], int flags);

#endif /* sfork.h */
