#include <asm/unistd.h>

.globl sfork_asm_clone
sfork_asm_clone:
	// Save our caller's %r12
	push %r12
	// Store sfork_stack_pointer in %r12 so it's preserved across the syscall
	movq %rdi, %r12
	// Prepare arguments and syscall "clone"
        movq $__NR_clone, %rax
        movq %rsi, %rdi
        movq %rdx, %rsi
        movq %rcx, %rdx
        movq %r8, %r10
        movq %r9, %r8
        movq $0, %r9
	syscall
	// Check the return value.
	cmp $0, %rax
	jg sfork_asm_clone_parent
	// We're in the child, restore our caller's %r12 and return.
	pop %r12
	ret

sfork_asm_clone_parent:
	// We've been resumed in the parent with our registers restored.
        // A pointer to sfork_stack_pointer is in %r12, where we put it before calling vfork.
        // Load sfork_stack_pointer from memory.
        movq (%r12), %r8
	// Test if it's null.
        cmp $0, %r8
        je sfork_asm_clone_parent_uninitialized
	// Zero-out sfork_stack_pointer so it can't be used a second time.
	movq $0, (%r12)
        // Switch our stack to the saved one.
        movq %r8, %rsp
        // Restore our registers from the stack
        pop %rbp
        pop %r15
        pop %r14
        pop %r13
        pop %r12
        pop %rbx
        // Return on the new stack
        ret

sfork_asm_clone_parent_uninitialized:
	// The stack pointer was null, which means the child segfaulted or called regular exit/exec.
	// We have nowhere to jump to, and we can't just return since the child trampled the stack.
	// TODO should print an error message and raise SIGABRT here
	ud2

.globl sfork_asm_exit
sfork_asm_exit:
	// Save our registers on the stack.
        push %rbx
        push %r12
        push %r13
        push %r14
        push %r15
        push %rbp
        // Store the stack pointer.
        movq %rsp, (%rdi)
	// Prepare arguments and syscall "exit"
        movq $__NR_exit, %rax
        movq %rsi, %rdi
        movq $0, %rsi
        movq $0, %rdx
        movq $0, %r10
        movq $0, %r8
        movq $0, %r9
	syscall
	ud2

.globl sfork_asm_execveat
sfork_asm_execveat:
	// Save our registers on the stack.
        push %rbx
        push %r12
        push %r13
        push %r14
        push %r15
        push %rbp
        // Store the stack pointer.
        movq %rsp, (%rdi)
	// Prepare arguments and syscall "execveat"
        movq $__NR_execveat, %rax
        movq %rsi, %rdi
        movq %rdx, %rsi
        movq %rcx, %rdx
        movq %r8, %r10
        movq %r9, %r8
        movq $0, %r9
	syscall
	// If we're still here, the execve failed, and we need to return
	subq $48, %rsp
	// Null out the stack pointer so we don't jump to it
	movq $0, (%rdi)
	ret
