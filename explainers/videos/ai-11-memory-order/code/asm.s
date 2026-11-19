	.file	"asm.cpp"
	.text
	.section	.text._ZN7RingSeqI5QuoteLm1024EE8try_pushERKS0_,"axG",@progbits,_ZN7RingSeqI5QuoteLm1024EE8try_pushERKS0_,comdat
	.align 2
	.p2align 4
	.weak	_ZN7RingSeqI5QuoteLm1024EE8try_pushERKS0_
	.type	_ZN7RingSeqI5QuoteLm1024EE8try_pushERKS0_, @function
_ZN7RingSeqI5QuoteLm1024EE8try_pushERKS0_:
.LFB741:
	.cfi_startproc
	endbr64
	movq	(%rdi), %rax
	movq	%rax, %rdx
	subq	8(%rdi), %rdx
	cmpq	$1024, %rdx
	je	.L2
.L4:
	movq	%rax, %rdx
	movdqu	(%rsi), %xmm0
	addq	$1, %rax
	andl	$1023, %edx
	salq	$4, %rdx
	movaps	%xmm0, 128(%rdx,%rdi)
	xchgq	(%rdi), %rax
	movl	$1, %eax
	ret
	.p2align 4,,10
	.p2align 3
.L2:
	movq	%rax, %rcx
	movq	64(%rdi), %rdx
	subq	%rdx, %rcx
	movq	%rdx, 8(%rdi)
	cmpq	$1024, %rcx
	jne	.L4
	xorl	%eax, %eax
	ret
	.cfi_endproc
.LFE741:
	.size	_ZN7RingSeqI5QuoteLm1024EE8try_pushERKS0_, .-_ZN7RingSeqI5QuoteLm1024EE8try_pushERKS0_
	.section	.text._ZN7RingSeqI5QuoteLm1024EE7try_popERS0_,"axG",@progbits,_ZN7RingSeqI5QuoteLm1024EE7try_popERS0_,comdat
	.align 2
	.p2align 4
	.weak	_ZN7RingSeqI5QuoteLm1024EE7try_popERS0_
	.type	_ZN7RingSeqI5QuoteLm1024EE7try_popERS0_, @function
_ZN7RingSeqI5QuoteLm1024EE7try_popERS0_:
.LFB742:
	.cfi_startproc
	endbr64
	leaq	64(%rdi), %rcx
	movq	64(%rdi), %rax
	cmpq	%rax, 72(%rdi)
	je	.L7
.L9:
	movq	%rax, %rdx
	addq	$1, %rax
	andl	$1023, %edx
	salq	$4, %rdx
	movdqa	128(%rdx,%rdi), %xmm0
	movups	%xmm0, (%rsi)
	xchgq	(%rcx), %rax
	movl	$1, %eax
	ret
	.p2align 4,,10
	.p2align 3
.L7:
	movq	(%rdi), %rdx
	movq	%rdx, 72(%rdi)
	cmpq	%rdx, %rax
	jne	.L9
	xorl	%eax, %eax
	ret
	.cfi_endproc
.LFE742:
	.size	_ZN7RingSeqI5QuoteLm1024EE7try_popERS0_, .-_ZN7RingSeqI5QuoteLm1024EE7try_popERS0_
	.section	.text._ZN6RingARI5QuoteLm1024EE8try_pushERKS0_,"axG",@progbits,_ZN6RingARI5QuoteLm1024EE8try_pushERKS0_,comdat
	.align 2
	.p2align 4
	.weak	_ZN6RingARI5QuoteLm1024EE8try_pushERKS0_
	.type	_ZN6RingARI5QuoteLm1024EE8try_pushERKS0_, @function
_ZN6RingARI5QuoteLm1024EE8try_pushERKS0_:
.LFB743:
	.cfi_startproc
	endbr64
	movq	(%rdi), %rax
	movq	%rax, %rdx
	subq	8(%rdi), %rdx
	cmpq	$1024, %rdx
	je	.L11
.L13:
	movq	%rax, %rdx
	movdqu	(%rsi), %xmm0
	addq	$1, %rax
	andl	$1023, %edx
	salq	$4, %rdx
	movaps	%xmm0, 128(%rdx,%rdi)
	movq	%rax, (%rdi)
	movl	$1, %eax
	ret
	.p2align 4,,10
	.p2align 3
.L11:
	movq	64(%rdi), %rdx
	movq	%rax, %rcx
	subq	%rdx, %rcx
	movq	%rdx, 8(%rdi)
	cmpq	$1024, %rcx
	jne	.L13
	xorl	%eax, %eax
	ret
	.cfi_endproc
.LFE743:
	.size	_ZN6RingARI5QuoteLm1024EE8try_pushERKS0_, .-_ZN6RingARI5QuoteLm1024EE8try_pushERKS0_
	.section	.text._ZN6RingARI5QuoteLm1024EE7try_popERS0_,"axG",@progbits,_ZN6RingARI5QuoteLm1024EE7try_popERS0_,comdat
	.align 2
	.p2align 4
	.weak	_ZN6RingARI5QuoteLm1024EE7try_popERS0_
	.type	_ZN6RingARI5QuoteLm1024EE7try_popERS0_, @function
_ZN6RingARI5QuoteLm1024EE7try_popERS0_:
.LFB744:
	.cfi_startproc
	endbr64
	movq	64(%rdi), %rax
	cmpq	%rax, 72(%rdi)
	je	.L15
.L17:
	movq	%rax, %rdx
	addq	$1, %rax
	andl	$1023, %edx
	salq	$4, %rdx
	movdqa	128(%rdx,%rdi), %xmm0
	movups	%xmm0, (%rsi)
	movq	%rax, 64(%rdi)
	movl	$1, %eax
	ret
	.p2align 4,,10
	.p2align 3
.L15:
	movq	(%rdi), %rdx
	movq	%rdx, 72(%rdi)
	cmpq	%rdx, %rax
	jne	.L17
	xorl	%eax, %eax
	ret
	.cfi_endproc
.LFE744:
	.size	_ZN6RingARI5QuoteLm1024EE7try_popERS0_, .-_ZN6RingARI5QuoteLm1024EE7try_popERS0_
	.ident	"GCC: (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	1f - 0f
	.long	4f - 1f
	.long	5
0:
	.string	"GNU"
1:
	.align 8
	.long	0xc0000002
	.long	3f - 2f
2:
	.long	0x3
3:
	.align 8
4:
