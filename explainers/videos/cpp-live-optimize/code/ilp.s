	.file	"ilp.cpp"
	.text
	.p2align 4
	.globl	_Z9one_chainPK1T
	.type	_Z9one_chainPK1T, @function
_Z9one_chainPK1T:
.LFB12738:
	.cfi_startproc
	endbr64
	leaq	512(%rdi), %rdx
	pxor	%xmm1, %xmm1
	.p2align 4,,10
	.p2align 3
.L4:
	movl	8(%rdi), %eax
	pxor	%xmm0, %xmm0
	pxor	%xmm2, %xmm2
	addq	$16, %rdi
	cvtsi2sdq	-16(%rdi), %xmm0
	cvtsi2sdq	%rax, %xmm2
	mulsd	%xmm2, %xmm0
	addsd	%xmm0, %xmm1
	cmpq	%rdi, %rdx
	jne	.L4
	movapd	%xmm1, %xmm0
	ret
	.cfi_endproc
.LFE12738:
	.size	_Z9one_chainPK1T, .-_Z9one_chainPK1T
	.p2align 4
	.globl	_Z11four_chainsPK1T
	.type	_Z11four_chainsPK1T, @function
_Z11four_chainsPK1T:
.LFB12739:
	.cfi_startproc
	endbr64
	pxor	%xmm3, %xmm3
	leaq	512(%rdi), %rdx
	movapd	%xmm3, %xmm2
	movapd	%xmm3, %xmm4
	movapd	%xmm3, %xmm0
	.p2align 4,,10
	.p2align 3
.L16:
	movl	8(%rdi), %eax
	pxor	%xmm1, %xmm1
	pxor	%xmm5, %xmm5
	addq	$64, %rdi
	cvtsi2sdq	-64(%rdi), %xmm1
	cvtsi2sdq	%rax, %xmm5
	movl	-40(%rdi), %eax
	mulsd	%xmm5, %xmm1
	pxor	%xmm5, %xmm5
	cvtsi2sdq	%rax, %xmm5
	movl	-24(%rdi), %eax
	addsd	%xmm1, %xmm0
	pxor	%xmm1, %xmm1
	cvtsi2sdq	-48(%rdi), %xmm1
	mulsd	%xmm5, %xmm1
	pxor	%xmm5, %xmm5
	cvtsi2sdq	%rax, %xmm5
	movl	-8(%rdi), %eax
	addsd	%xmm1, %xmm4
	pxor	%xmm1, %xmm1
	cvtsi2sdq	-32(%rdi), %xmm1
	mulsd	%xmm5, %xmm1
	pxor	%xmm5, %xmm5
	cvtsi2sdq	%rax, %xmm5
	addsd	%xmm1, %xmm2
	pxor	%xmm1, %xmm1
	cvtsi2sdq	-16(%rdi), %xmm1
	mulsd	%xmm5, %xmm1
	addsd	%xmm1, %xmm3
	cmpq	%rdi, %rdx
	jne	.L16
	addsd	%xmm4, %xmm0
	addsd	%xmm3, %xmm2
	addsd	%xmm2, %xmm0
	ret
	.cfi_endproc
.LFE12739:
	.size	_Z11four_chainsPK1T, .-_Z11four_chainsPK1T
	.p2align 4
	.globl	_Z7sig_divdlll
	.type	_Z7sig_divdlll, @function
_Z7sig_divdlll:
.LFB12740:
	.cfi_startproc
	endbr64
	pxor	%xmm2, %xmm2
	movapd	%xmm0, %xmm1
	leaq	(%rsi,%rdx), %rax
	subq	%rsi, %rdx
	cvtsi2sdq	%rdi, %xmm2
	pxor	%xmm0, %xmm0
	cvtsi2sdq	%rax, %xmm0
	mulsd	.LC1(%rip), %xmm0
	xorl	%eax, %eax
	divsd	%xmm2, %xmm1
	subsd	%xmm1, %xmm0
	pxor	%xmm1, %xmm1
	cvtsi2sdq	%rdx, %xmm1
	divsd	%xmm1, %xmm0
	movsd	.LC3(%rip), %xmm1
	comisd	.LC2(%rip), %xmm0
	seta	%al
	xorl	%edx, %edx
	comisd	%xmm0, %xmm1
	seta	%dl
	subl	%edx, %eax
	ret
	.cfi_endproc
.LFE12740:
	.size	_Z7sig_divdlll, .-_Z7sig_divdlll
	.p2align 4
	.globl	_Z7sig_mulllll
	.type	_Z7sig_mulllll, @function
_Z7sig_mulllll:
.LFB12741:
	.cfi_startproc
	endbr64
	movq	%rdi, %rax
	leaq	(%rdx,%rcx), %rdi
	subq	%rdx, %rcx
	imulq	%rsi, %rdi
	addq	%rax, %rax
	imulq	%rsi, %rcx
	subq	%rax, %rdi
	xorl	%eax, %eax
	addq	%rdi, %rdi
	cmpq	%rcx, %rdi
	setg	%al
	negq	%rcx
	xorl	%edx, %edx
	cmpq	%rdi, %rcx
	setg	%dl
	subl	%edx, %eax
	ret
	.cfi_endproc
.LFE12741:
	.size	_Z7sig_mulllll, .-_Z7sig_mulllll
	.section	.rodata.str1.8,"aMS",@progbits,1
	.align 8
.LC7:
	.string	"loop: 1 chain %.1f ns (%.0f cyc)  4 chains %.1f ns (%.0f cyc)   signal: divide %.1f ns (%.0f cyc)  cross-mul %.1f ns (%.0f cyc)  [%g %d %d]\n"
	.section	.text.startup,"ax",@progbits
	.p2align 4
	.globl	main
	.type	main, @function
main:
.LFB12742:
	.cfi_startproc
	endbr64
	pushq	%r15
	.cfi_def_cfa_offset 16
	.cfi_offset 15, -16
	movl	$15, %ecx
	pushq	%r14
	.cfi_def_cfa_offset 24
	.cfi_offset 14, -24
	pushq	%r13
	.cfi_def_cfa_offset 32
	.cfi_offset 13, -32
	pushq	%r12
	.cfi_def_cfa_offset 40
	.cfi_offset 12, -40
	pushq	%rbp
	.cfi_def_cfa_offset 48
	.cfi_offset 6, -48
	pushq	%rbx
	.cfi_def_cfa_offset 56
	.cfi_offset 3, -56
	subq	$680, %rsp
	.cfi_def_cfa_offset 736
	movq	%fs:40, %rax
	movq	%rax, 664(%rsp)
	xorl	%eax, %eax
	leaq	24(%rsp), %rdx
	leaq	16(%rsp), %rbx
	movq	$4, 16(%rsp)
	movq	%rdx, %rdi
	rep stosq
	call	pthread_self@PLT
	movq	%rbx, %rdx
	movl	$128, %esi
	movq	%rax, %rdi
	call	pthread_setaffinity_np@PLT
	call	_ZNSt6chrono3_V212steady_clock3nowEv@PLT
	movq	%rax, %rbx
	rdtsc
	movq	%rax, %rbp
	salq	$32, %rdx
	orq	%rdx, %rbp
	.p2align 4,,10
	.p2align 3
.L21:
	call	_ZNSt6chrono3_V212steady_clock3nowEv@PLT
	subq	%rbx, %rax
	cmpq	$199999999, %rax
	jle	.L21
	call	_ZNSt6chrono3_V212steady_clock3nowEv@PLT
	movq	%rax, %rcx
	rdtsc
	salq	$32, %rdx
	orq	%rdx, %rax
	subq	%rbp, %rax
	js	.L22
	pxor	%xmm0, %xmm0
	cvtsi2sdq	%rax, %xmm0
.L23:
	subq	%rbx, %rcx
	pxor	%xmm1, %xmm1
	leaq	144(%rsp), %rbx
	movabsq	$2361183241434822607, %rdi
	cvtsi2sdq	%rcx, %xmm1
	movq	%rbx, %rsi
	movl	$7, %ecx
	leaq	656(%rsp), %r8
	divsd	%xmm1, %xmm0
	movsd	%xmm0, 8(%rsp)
	.p2align 4,,10
	.p2align 3
.L24:
	movq	%rcx, %rdx
	addq	$16, %rsi
	salq	$13, %rdx
	xorq	%rcx, %rdx
	movq	%rdx, %rax
	shrq	$7, %rax
	xorq	%rdx, %rax
	movq	%rax, %rcx
	salq	$17, %rcx
	xorq	%rax, %rcx
	movq	%rcx, %rdx
	shrq	$3, %rdx
	movq	%rdx, %rax
	mulq	%rdi
	movq	%rcx, %rax
	shrq	$4, %rdx
	imulq	$1000, %rdx, %rdx
	subq	%rdx, %rax
	movq	%rcx, %rdx
	salq	$13, %rdx
	addq	$1000000, %rax
	xorq	%rcx, %rdx
	movq	%rax, -16(%rsi)
	movq	%rdx, %rax
	shrq	$7, %rax
	xorq	%rdx, %rax
	movq	%rax, %rcx
	salq	$17, %rcx
	xorq	%rax, %rcx
	movq	%rcx, %rdx
	shrq	$3, %rdx
	movq	%rdx, %rax
	mulq	%rdi
	movq	%rcx, %rax
	shrq	$4, %rdx
	imulq	$1000, %rdx, %rdx
	subq	%rdx, %rax
	addl	$1, %eax
	movl	%eax, -8(%rsi)
	cmpq	%rsi, %r8
	jne	.L24
	movl	$3, %r12d
	leaq	.LC7(%rip), %r13
	movabsq	$16000000000, %rbp
.L39:
	rdtsc
	xorl	%ecx, %ecx
	pxor	%xmm6, %xmm6
	movq	%rax, %r15
	salq	$32, %rdx
	orq	%rdx, %r15
	.p2align 4,,10
	.p2align 3
.L25:
	movq	%rbx, %rdi
	call	_Z9one_chainPK1T
	movl	%ecx, %eax
	addl	$1, %ecx
	andl	$31, %eax
	addsd	%xmm0, %xmm6
	salq	$4, %rax
	xorl	$1, 152(%rsp,%rax)
	cmpl	$2000000, %ecx
	jne	.L25
	rdtsc
	xorl	%ecx, %ecx
	movq	%rax, %r10
	salq	$32, %rdx
	orq	%rdx, %r10
	.p2align 4,,10
	.p2align 3
.L26:
	movq	%rbx, %rdi
	call	_Z11four_chainsPK1T
	movl	%ecx, %eax
	addl	$1, %ecx
	andl	$31, %eax
	addsd	%xmm0, %xmm6
	salq	$4, %rax
	xorl	$1, 152(%rsp,%rax)
	cmpl	$2000000, %ecx
	jne	.L26
	rdtsc
	xorl	%r8d, %r8d
	movq	%rax, %r11
	salq	$32, %rdx
	orq	%rdx, %r11
	.p2align 4,,10
	.p2align 3
.L27:
	pxor	%xmm0, %xmm0
	movl	%r8d, %eax
	movl	$999900, %esi
	movl	$16000, %edi
	cvtsi2sdl	%r8d, %xmm0
	addsd	.LC5(%rip), %xmm0
	andl	$1, %eax
	leaq	1000100(%rax), %rdx
	call	_Z7sig_divdlll
	movl	%eax, %r8d
	subl	$1, %ecx
	jne	.L27
	rdtsc
	movl	$2000000, %r9d
	xorl	%ecx, %ecx
	movq	%rax, %r14
	salq	$32, %rdx
	orq	%rdx, %r14
	.p2align 4,,10
	.p2align 3
.L28:
	movl	%ecx, %eax
	leaq	(%rcx,%rbp), %rdi
	movl	$999900, %edx
	movl	$16000, %esi
	andl	$1, %eax
	addq	$1000100, %rax
	movq	%rax, %rcx
	call	_Z7sig_mulllll
	movslq	%eax, %rcx
	subl	$1, %r9d
	jne	.L28
	rdtsc
	pxor	%xmm8, %xmm8
	movsd	.LC4(%rip), %xmm3
	cmpltsd	%xmm6, %xmm8
	salq	$32, %rdx
	orq	%rdx, %rax
	andpd	%xmm3, %xmm8
	subq	%r14, %rax
	js	.L31
	pxor	%xmm7, %xmm7
	cvtsi2sdq	%rax, %xmm7
.L32:
	subq	%r11, %r14
	js	.L33
	pxor	%xmm5, %xmm5
	cvtsi2sdq	%r14, %xmm5
.L34:
	subq	%r10, %r11
	js	.L35
	pxor	%xmm3, %xmm3
	cvtsi2sdq	%r11, %xmm3
.L36:
	subq	%r15, %r10
	js	.L37
	pxor	%xmm1, %xmm1
	cvtsi2sdq	%r10, %xmm1
.L38:
	movapd	%xmm7, %xmm6
	movapd	%xmm5, %xmm4
	movapd	%xmm3, %xmm2
	subq	$16, %rsp
	.cfi_def_cfa_offset 752
	movapd	%xmm1, %xmm0
	movl	%r8d, %edx
	movq	%r13, %rsi
	movl	$2, %edi
	movsd	24(%rsp), %xmm9
	movl	$8, %eax
	movsd	%xmm8, (%rsp)
	divsd	.LC6(%rip), %xmm7
	divsd	.LC6(%rip), %xmm5
	divsd	.LC6(%rip), %xmm3
	divsd	.LC6(%rip), %xmm1
	divsd	%xmm9, %xmm6
	divsd	%xmm9, %xmm4
	divsd	.LC6(%rip), %xmm6
	divsd	%xmm9, %xmm2
	divsd	.LC6(%rip), %xmm4
	divsd	%xmm9, %xmm0
	divsd	.LC6(%rip), %xmm2
	divsd	.LC6(%rip), %xmm0
	call	__printf_chk@PLT
	popq	%rax
	.cfi_def_cfa_offset 744
	popq	%rdx
	.cfi_def_cfa_offset 736
	subl	$1, %r12d
	jne	.L39
	movq	664(%rsp), %rax
	subq	%fs:40, %rax
	jne	.L51
	addq	$680, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 56
	xorl	%eax, %eax
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%rbp
	.cfi_def_cfa_offset 40
	popq	%r12
	.cfi_def_cfa_offset 32
	popq	%r13
	.cfi_def_cfa_offset 24
	popq	%r14
	.cfi_def_cfa_offset 16
	popq	%r15
	.cfi_def_cfa_offset 8
	ret
.L37:
	.cfi_restore_state
	movq	%r10, %rax
	andl	$1, %r10d
	pxor	%xmm1, %xmm1
	shrq	%rax
	orq	%r10, %rax
	cvtsi2sdq	%rax, %xmm1
	addsd	%xmm1, %xmm1
	jmp	.L38
.L35:
	movq	%r11, %rax
	andl	$1, %r11d
	pxor	%xmm3, %xmm3
	shrq	%rax
	orq	%r11, %rax
	cvtsi2sdq	%rax, %xmm3
	addsd	%xmm3, %xmm3
	jmp	.L36
.L33:
	movq	%r14, %rax
	andl	$1, %r14d
	pxor	%xmm5, %xmm5
	shrq	%rax
	orq	%r14, %rax
	cvtsi2sdq	%rax, %xmm5
	addsd	%xmm5, %xmm5
	jmp	.L34
.L31:
	movq	%rax, %rdx
	andl	$1, %eax
	pxor	%xmm7, %xmm7
	shrq	%rdx
	orq	%rax, %rdx
	cvtsi2sdq	%rdx, %xmm7
	addsd	%xmm7, %xmm7
	jmp	.L32
.L22:
	movq	%rax, %rdx
	andl	$1, %eax
	pxor	%xmm0, %xmm0
	shrq	%rdx
	orq	%rax, %rdx
	cvtsi2sdq	%rdx, %xmm0
	addsd	%xmm0, %xmm0
	jmp	.L23
.L51:
	call	__stack_chk_fail@PLT
	.cfi_endproc
.LFE12742:
	.size	main, .-main
	.section	.rodata.cst8,"aM",@progbits,8
	.align 8
.LC1:
	.long	0
	.long	1071644672
	.align 8
.LC2:
	.long	0
	.long	1070596096
	.align 8
.LC3:
	.long	0
	.long	-1076887552
	.align 8
.LC4:
	.long	0
	.long	1072693248
	.align 8
.LC5:
	.long	0
	.long	1108200805
	.align 8
.LC6:
	.long	0
	.long	1094616192
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
