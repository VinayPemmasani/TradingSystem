	.file	"asm.cpp"
	.text
	.p2align 4
	.globl	_Z9on_msg_v4RN2v47HandlerERK3Msg
	.type	_Z9on_msg_v4RN2v47HandlerERK3Msg, @function
_Z9on_msg_v4RN2v47HandlerERK3Msg:
.LFB13222:
	.cfi_startproc
	endbr64
	movl	4(%rsi), %ecx
	movq	%rsi, %rdx
	movzbl	1(%rsi), %eax
	testl	%ecx, %ecx
	setne	%sil
	cmpq	$0, 8(%rdx)
	setg	%cl
	testb	%cl, %sil
	je	.L10
	cmpb	$66, %al
	sete	%cl
	cmpb	$83, %al
	sete	%al
	orb	%al, %cl
	je	.L10
	movzwl	2(%rdx), %ecx
	leaq	0(,%rcx,8), %rax
	subq	%rcx, %rax
	salq	$6, %rax
	addq	(%rdi), %rax
	addq	$1, 32(%rax)
	cmpb	$81, (%rdx)
	movq	16(%rax), %rdi
	movq	24(%rax), %rsi
	je	.L18
	movl	40(%rax), %ecx
	movq	8(%rdx), %r10
	leal	1(%rcx), %r8d
	movl	%r8d, 40(%rax)
	movl	4(%rdx), %r8d
	movl	%ecx, %edx
	andl	$31, %edx
	imulq	%r8, %r10
	movq	%r8, %r9
	movq	%r10, %rcx
	subq	48(%rax,%rdx,8), %rcx
	addq	%rcx, %rdi
	movl	304(%rax,%rdx,4), %ecx
	movq	%rdi, 16(%rax)
	subq	%rcx, %r8
	addq	%r8, %rsi
	movq	%rsi, 24(%rax)
	movq	%r10, 48(%rax,%rdx,8)
	movl	%r9d, 304(%rax,%rdx,4)
.L6:
	movq	(%rax), %rcx
	movq	8(%rax), %rax
	testq	%rcx, %rcx
	setg	%r8b
	cmpq	%rax, %rcx
	setl	%dl
	testb	%dl, %r8b
	je	.L4
	testq	%rsi, %rsi
	je	.L4
	leaq	(%rcx,%rax), %rdx
	subq	%rcx, %rax
	addq	%rdi, %rdi
	xorl	%ecx, %ecx
	imulq	%rsi, %rdx
	imulq	%rsi, %rax
	subq	%rdi, %rdx
	addq	%rdx, %rdx
	cmpq	%rax, %rdx
	setg	%cl
	negq	%rax
	cmpq	%rax, %rdx
	movl	%ecx, %eax
	setl	%dl
	movzbl	%dl, %edx
	subl	%edx, %eax
	ret
	.p2align 4,,10
	.p2align 3
.L10:
	addq	$1, 8(%rdi)
.L4:
	xorl	%eax, %eax
	ret
	.p2align 4,,10
	.p2align 3
.L18:
	cmpb	$83, 1(%rdx)
	movq	8(%rdx), %rcx
	sete	%dl
	movzbl	%dl, %edx
	movq	%rcx, (%rax,%rdx,8)
	jmp	.L6
	.cfi_endproc
.LFE13222:
	.size	_Z9on_msg_v4RN2v47HandlerERK3Msg, .-_Z9on_msg_v4RN2v47HandlerERK3Msg
	.section	.text._ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv,"axG",@progbits,_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv,comdat
	.align 2
	.p2align 4
	.weak	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	.type	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv, @function
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv:
.LFB13934:
	.cfi_startproc
	endbr64
	movq	(%rdi), %rax
	leaq	16(%rdi), %rdx
	cmpq	%rdx, %rax
	je	.L19
	movq	16(%rdi), %rsi
	movq	%rax, %rdi
	addq	$1, %rsi
	jmp	_ZdlPvm@PLT
	.p2align 4,,10
	.p2align 3
.L19:
	ret
	.cfi_endproc
.LFE13934:
	.size	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv, .-_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	.section	.rodata._ZN2v17Handler6on_msgERK3Msg.str1.1,"aMS",@progbits,1
.LC1:
	.string	"vector::_M_realloc_insert"
	.section	.text._ZN2v17Handler6on_msgERK3Msg,"axG",@progbits,_ZN2v17Handler6on_msgERK3Msg,comdat
	.align 2
	.p2align 4
	.weak	_ZN2v17Handler6on_msgERK3Msg
	.type	_ZN2v17Handler6on_msgERK3Msg, @function
_ZN2v17Handler6on_msgERK3Msg:
.LFB13167:
	.cfi_startproc
	.cfi_personality 0x9b,DW.ref.__gxx_personality_v0
	.cfi_lsda 0x1b,.LLSDA13167
	endbr64
	pushq	%r15
	.cfi_def_cfa_offset 16
	.cfi_offset 15, -16
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
	subq	$88, %rsp
	.cfi_def_cfa_offset 144
	movq	%fs:40, %rax
	movq	%rax, 72(%rsp)
	movl	4(%rsi), %eax
	testl	%eax, %eax
	je	.L24
	cmpq	$0, 8(%rsi)
	jle	.L24
	movzbl	1(%rsi), %edx
	cmpb	$66, %dl
	je	.L76
	cmpb	$83, %dl
	je	.L76
.L24:
	addq	$1, 48(%rdi)
.L23:
	xorl	%eax, %eax
.L21:
	movq	72(%rsp), %rdx
	subq	%fs:40, %rdx
	jne	.L95
	addq	$88, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 56
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
	.p2align 4,,10
	.p2align 3
.L76:
	.cfi_restore_state
	movzwl	2(%rsi), %ebx
	salq	$6, %rbx
	addq	(%rdi), %rbx
	addq	$1, 40(%rbx)
	cmpb	$81, (%rsi)
	jne	.L26
	cmpb	$66, 1(%rsi)
	movq	8(%rsi), %rdi
	je	.L96
	movq	%rdi, 8(%rbx)
	movq	(%rbx), %rdi
.L28:
	testq	%rdi, %rdi
	jle	.L23
	movq	8(%rbx), %r8
	cmpq	%rdi, %r8
	jle	.L23
	movq	24(%rbx), %rax
	movq	16(%rbx), %rsi
	cmpq	%rax, %rsi
	je	.L23
	subq	%rsi, %rax
	movq	%rax, %rcx
	movq	%rax, %rdx
	movabsq	$-6148914691236517205, %rax
	sarq	$4, %rcx
	imulq	%rax, %rcx
	movl	$32, %eax
	cmpq	%rax, %rcx
	cmovnb	%rcx, %rax
	leaq	-32(%rax), %r9
	cmpq	%rcx, %r9
	jnb	.L61
	leaq	(%rax,%rax,2), %rax
	xorl	%ecx, %ecx
	pxor	%xmm1, %xmm1
	salq	$4, %rax
	leaq	-1504(%rsi,%rax), %rax
	leaq	32(%rsi,%rdx), %rsi
	.p2align 4,,10
	.p2align 3
.L64:
	movl	8(%rax), %edx
	pxor	%xmm0, %xmm0
	pxor	%xmm2, %xmm2
	addq	$48, %rax
	cvtsi2sdq	-48(%rax), %xmm0
	cvtsi2sdq	%rdx, %xmm2
	addq	%rdx, %rcx
	mulsd	%xmm2, %xmm0
	addsd	%xmm0, %xmm1
	cmpq	%rsi, %rax
	jne	.L64
	leaq	(%r8,%rdi), %rax
	pxor	%xmm0, %xmm0
	cvtsi2sdq	%rax, %xmm0
	mulsd	.LC2(%rip), %xmm0
	testq	%rcx, %rcx
	js	.L65
	pxor	%xmm2, %xmm2
	cvtsi2sdq	%rcx, %xmm2
.L66:
	divsd	%xmm2, %xmm1
	subq	%rdi, %r8
	movl	$1, %eax
	subsd	%xmm1, %xmm0
	pxor	%xmm1, %xmm1
	cvtsi2sdq	%r8, %xmm1
	divsd	%xmm1, %xmm0
	comisd	.LC3(%rip), %xmm0
	ja	.L21
.L69:
	movsd	.LC4(%rip), %xmm1
	xorl	%eax, %eax
	comisd	%xmm0, %xmm1
	seta	%al
	negl	%eax
	jmp	.L21
	.p2align 4,,10
	.p2align 3
.L26:
	movq	16(%rsi), %rdx
	leaq	32(%rsp), %r12
	movb	$0, 40(%rsp)
	movq	%r12, 16(%rsp)
	movq	24(%rbx), %rbp
	movq	%rdx, 32(%rsp)
	movq	8(%rsi), %rdx
	movq	$8, 24(%rsp)
	movq	%rdx, 48(%rsp)
	movl	%eax, 56(%rsp)
	cmpq	32(%rbx), %rbp
	je	.L29
	leaq	16(%rbp), %rdx
	movq	%rdx, 0(%rbp)
	movq	16(%rsp), %rax
	cmpq	%r12, %rax
	je	.L30
	movq	%rax, 0(%rbp)
	movq	32(%rsp), %rax
	movq	%rax, 16(%rbp)
.L31:
	movq	$8, 8(%rbp)
	movq	48(%rsp), %rax
	movq	%rax, 32(%rbp)
	movl	56(%rsp), %eax
	movl	%eax, 40(%rbp)
	addq	$48, 24(%rbx)
.L32:
	movq	(%rbx), %rdi
	jmp	.L28
	.p2align 4,,10
	.p2align 3
.L96:
	movq	%rdi, (%rbx)
	jmp	.L28
	.p2align 4,,10
	.p2align 3
.L29:
	movq	16(%rbx), %r13
	movq	%rbp, %r14
	movabsq	$-6148914691236517205, %rsi
	subq	%r13, %r14
	movq	%r14, %rcx
	sarq	$4, %rcx
	imulq	%rsi, %rcx
	movabsq	$192153584101141162, %rsi
	cmpq	%rsi, %rcx
	je	.L97
	cmpq	%r13, %rbp
	je	.L98
	leaq	(%rcx,%rcx), %rsi
	cmpq	%rcx, %rsi
	jb	.L73
	testq	%rsi, %rsi
	jne	.L99
	leaq	16(%r14), %r8
	movl	$8, %esi
	movl	$48, %r15d
	xorl	%ecx, %ecx
	movq	%r8, (%r14)
	movq	$0, 8(%rsp)
.L70:
	leaq	1(%rsi), %rdi
	cmpl	$8, %edi
	jnb	.L41
	testb	$4, %dil
	jne	.L100
	testl	%edi, %edi
	je	.L47
	movzbl	32(%rsp), %r9d
	movb	%r9b, (%r8)
	testb	$2, %dil
	jne	.L101
	.p2align 4,,10
	.p2align 3
.L47:
	movq	%rsi, 8(%r14)
	movq	%r12, 16(%rsp)
	movq	$0, 24(%rsp)
	movb	$0, 32(%rsp)
	movq	%rdx, 32(%r14)
	movl	%eax, 40(%r14)
	cmpq	%r13, %rbp
	je	.L48
	movq	%r13, %rax
	movq	%rcx, %rdx
	jmp	.L57
	.p2align 4,,10
	.p2align 3
.L49:
	movq	%rsi, (%rdx)
	movq	16(%rax), %rsi
	movq	%rsi, 16(%rdx)
.L93:
	movq	8(%rax), %r8
.L56:
	movq	%r8, 8(%rdx)
	movq	32(%rax), %rsi
	addq	$48, %rax
	addq	$48, %rdx
	movq	%rsi, -16(%rdx)
	movl	-8(%rax), %esi
	movl	%esi, -8(%rdx)
	cmpq	%rax, %rbp
	je	.L102
.L57:
	leaq	16(%rdx), %rdi
	leaq	16(%rax), %r8
	movq	%rdi, (%rdx)
	movq	(%rax), %rsi
	cmpq	%r8, %rsi
	jne	.L49
	movq	8(%rax), %r8
	leaq	1(%r8), %r9
	cmpl	$8, %r9d
	jnb	.L50
	testb	$4, %r9b
	jne	.L103
	testl	%r9d, %r9d
	je	.L56
	movzbl	(%rsi), %r8d
	movb	%r8b, (%rdi)
	testb	$2, %r9b
	je	.L93
	movl	%r9d, %r9d
	movzwl	-2(%rsi,%r9), %esi
	movw	%si, -2(%rdi,%r9)
	movq	8(%rax), %r8
	jmp	.L56
	.p2align 4,,10
	.p2align 3
.L65:
	movq	%rcx, %rax
	andl	$1, %ecx
	pxor	%xmm2, %xmm2
	shrq	%rax
	orq	%rcx, %rax
	cvtsi2sdq	%rax, %xmm2
	addsd	%xmm2, %xmm2
	jmp	.L66
	.p2align 4,,10
	.p2align 3
.L102:
	subq	$48, %rbp
	subq	%r13, %rbp
	andq	$-16, %rbp
	leaq	96(%rcx,%rbp), %r15
.L48:
	testq	%r13, %r13
	je	.L58
	movq	32(%rbx), %rsi
	movq	%r13, %rdi
	movq	%rcx, (%rsp)
	subq	%r13, %rsi
	call	_ZdlPvm@PLT
	movq	(%rsp), %rcx
	movq	8(%rsp), %rax
	movq	%r15, 24(%rbx)
	movq	16(%rsp), %rdi
	movq	%rcx, 16(%rbx)
	movq	%rax, 32(%rbx)
	cmpq	%r12, %rdi
	je	.L32
	movq	32(%rsp), %rax
	leaq	1(%rax), %rsi
	call	_ZdlPvm@PLT
	jmp	.L32
	.p2align 4,,10
	.p2align 3
.L50:
	movq	(%rsi), %r8
	movq	%r8, (%rdi)
	movl	%r9d, %r8d
	movq	-8(%rsi,%r8), %r10
	movq	%r10, -8(%rdi,%r8)
	leaq	24(%rdx), %r8
	andq	$-8, %r8
	subq	%r8, %rdi
	addl	%edi, %r9d
	subq	%rdi, %rsi
	andl	$-8, %r9d
	cmpl	$8, %r9d
	jb	.L93
	andl	$-8, %r9d
	xorl	%edi, %edi
.L54:
	movl	%edi, %r10d
	addl	$8, %edi
	movq	(%rsi,%r10), %r11
	movq	%r11, (%r8,%r10)
	cmpl	%r9d, %edi
	jb	.L54
	jmp	.L93
	.p2align 4,,10
	.p2align 3
.L30:
	movq	(%rax), %rcx
	movq	%rcx, 16(%rbp)
	movzbl	8(%rax), %eax
	movb	%al, 8(%rdx)
	jmp	.L31
	.p2align 4,,10
	.p2align 3
.L98:
	addq	$1, %rcx
	jc	.L73
	movabsq	$192153584101141162, %rax
	cmpq	%rax, %rcx
	cmovbe	%rcx, %rax
	leaq	(%rax,%rax,2), %r15
	salq	$4, %r15
.L38:
	movq	%r15, %rdi
.LEHB0:
	call	_Znwm@PLT
	movq	%rax, %rcx
	movq	48(%rsp), %rdx
	movl	56(%rsp), %eax
	leaq	(%rcx,%r15), %rdi
	movq	24(%rsp), %rsi
	leaq	48(%rcx), %r15
	addq	%rcx, %r14
	movq	%rdi, 8(%rsp)
	movq	16(%rsp), %rdi
	cmpq	%r12, %rdi
	je	.L104
	movq	%rdi, (%r14)
	movq	32(%rsp), %rdi
	movq	%rdi, 16(%r14)
	jmp	.L47
	.p2align 4,,10
	.p2align 3
.L61:
	pxor	%xmm1, %xmm1
	leaq	(%r8,%rdi), %rax
	pxor	%xmm0, %xmm0
	subq	%rdi, %r8
	divsd	%xmm1, %xmm1
	cvtsi2sdq	%rax, %xmm0
	mulsd	.LC2(%rip), %xmm0
	subsd	%xmm1, %xmm0
	pxor	%xmm1, %xmm1
	cvtsi2sdq	%r8, %xmm1
	divsd	%xmm1, %xmm0
	jmp	.L69
.L73:
	movabsq	$9223372036854775776, %r15
	jmp	.L38
.L41:
	movq	32(%rsp), %r9
	movq	%r9, (%r8)
	movl	%edi, %r9d
	movq	-8(%r12,%r9), %r10
	movq	%r10, -8(%r8,%r9)
	leaq	8(%r8), %r9
	movq	%r12, %r10
	andq	$-8, %r9
	subq	%r9, %r8
	addl	%r8d, %edi
	subq	%r8, %r10
	andl	$-8, %edi
	cmpl	$8, %edi
	jb	.L47
	movl	%eax, (%rsp)
	andl	$-8, %edi
	movl	%edi, %r11d
	xorl	%edi, %edi
.L45:
	movl	%edi, %r8d
	addl	$8, %edi
	movq	(%r10,%r8), %rax
	movq	%rax, (%r9,%r8)
	cmpl	%r11d, %edi
	jb	.L45
	movl	(%rsp), %eax
	jmp	.L47
.L103:
	movl	(%rsi), %r8d
	movl	%r9d, %r9d
	movl	%r8d, (%rdi)
	movl	-4(%rsi,%r9), %esi
	movl	%esi, -4(%rdi,%r9)
	movq	8(%rax), %r8
	jmp	.L56
.L99:
	movabsq	$192153584101141162, %rax
	cmpq	%rax, %rsi
	cmova	%rax, %rsi
	imulq	$48, %rsi, %r15
	jmp	.L38
.L67:
	leaq	16(%rsp), %rdi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	movq	72(%rsp), %rax
	subq	%fs:40, %rax
	je	.L68
.L95:
	call	__stack_chk_fail@PLT
.L100:
	movl	32(%rsp), %r9d
	movl	%edi, %edi
	movl	%r9d, (%r8)
	movl	-4(%r12,%rdi), %r9d
	movl	%r9d, -4(%r8,%rdi)
	jmp	.L47
.L101:
	movl	%edi, %edi
	movzwl	-2(%r12,%rdi), %r9d
	movw	%r9w, -2(%r8,%rdi)
	jmp	.L47
.L58:
	movq	8(%rsp), %rax
	movq	%rcx, 16(%rbx)
	movq	%r15, 24(%rbx)
	movq	%rax, 32(%rbx)
	jmp	.L32
.L97:
	movq	72(%rsp), %rax
	subq	%fs:40, %rax
	jne	.L95
	leaq	.LC1(%rip), %rdi
	call	_ZSt20__throw_length_errorPKc@PLT
.LEHE0:
.L104:
	leaq	16(%r14), %r8
	movq	%r8, (%r14)
	jmp	.L70
.L75:
	endbr64
	movq	%rax, %rbx
	jmp	.L67
.L68:
	movq	%rbx, %rdi
.LEHB1:
	call	_Unwind_Resume@PLT
.LEHE1:
	.cfi_endproc
.LFE13167:
	.globl	__gxx_personality_v0
	.section	.gcc_except_table._ZN2v17Handler6on_msgERK3Msg,"aG",@progbits,_ZN2v17Handler6on_msgERK3Msg,comdat
.LLSDA13167:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE13167-.LLSDACSB13167
.LLSDACSB13167:
	.uleb128 .LEHB0-.LFB13167
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L75-.LFB13167
	.uleb128 0
	.uleb128 .LEHB1-.LFB13167
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE13167:
	.section	.text._ZN2v17Handler6on_msgERK3Msg,"axG",@progbits,_ZN2v17Handler6on_msgERK3Msg,comdat
	.size	_ZN2v17Handler6on_msgERK3Msg, .-_ZN2v17Handler6on_msgERK3Msg
	.text
	.p2align 4
	.globl	_Z9on_msg_v1RN2v17HandlerERK3Msg
	.type	_Z9on_msg_v1RN2v17HandlerERK3Msg, @function
_Z9on_msg_v1RN2v17HandlerERK3Msg:
.LFB13218:
	.cfi_startproc
	endbr64
	jmp	_ZN2v17Handler6on_msgERK3Msg
	.cfi_endproc
.LFE13218:
	.size	_Z9on_msg_v1RN2v17HandlerERK3Msg, .-_Z9on_msg_v1RN2v17HandlerERK3Msg
	.section	.text._ZN3v2a7Handler6on_msgERK3Msg,"axG",@progbits,_ZN3v2a7Handler6on_msgERK3Msg,comdat
	.align 2
	.p2align 4
	.weak	_ZN3v2a7Handler6on_msgERK3Msg
	.type	_ZN3v2a7Handler6on_msgERK3Msg, @function
_ZN3v2a7Handler6on_msgERK3Msg:
.LFB13176:
	.cfi_startproc
	.cfi_personality 0x9b,DW.ref.__gxx_personality_v0
	.cfi_lsda 0x1b,.LLSDA13176
	endbr64
	pushq	%r15
	.cfi_def_cfa_offset 16
	.cfi_offset 15, -16
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
	subq	$88, %rsp
	.cfi_def_cfa_offset 144
	movq	%fs:40, %rax
	movq	%rax, 72(%rsp)
	movl	4(%rsi), %eax
	testl	%eax, %eax
	je	.L109
	cmpq	$0, 8(%rsi)
	jle	.L109
	movzbl	1(%rsi), %edx
	cmpb	$66, %dl
	je	.L171
	cmpb	$83, %dl
	je	.L171
.L109:
	addq	$1, 24(%rdi)
.L108:
	xorl	%eax, %eax
.L106:
	movq	72(%rsp), %rdx
	subq	%fs:40, %rdx
	jne	.L191
	addq	$88, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 56
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
	.p2align 4,,10
	.p2align 3
.L171:
	.cfi_restore_state
	movzwl	2(%rsi), %ebx
	salq	$6, %rbx
	addq	(%rdi), %rbx
	addq	$1, 40(%rbx)
	cmpb	$81, (%rsi)
	jne	.L111
	cmpb	$66, 1(%rsi)
	movq	8(%rsi), %rdi
	je	.L192
	movq	%rdi, 8(%rbx)
	movq	(%rbx), %rdi
.L113:
	testq	%rdi, %rdi
	jle	.L108
	movq	8(%rbx), %r8
	cmpq	%rdi, %r8
	jle	.L108
	movq	24(%rbx), %r9
	movq	16(%rbx), %r10
	cmpq	%r9, %r10
	je	.L108
	subq	%r10, %r9
	movl	$32, %edx
	movabsq	$-6148914691236517205, %rax
	movq	%r9, %r11
	sarq	$4, %r11
	imulq	%rax, %r11
	cmpq	%rdx, %r11
	cmovnb	%r11, %rdx
	leaq	-28(%rdx), %rsi
	cmpq	%rsi, %r11
	jb	.L193
	leaq	(%rdx,%rdx,2), %rax
	pxor	%xmm4, %xmm4
	xorl	%ecx, %ecx
	movapd	%xmm4, %xmm2
	salq	$4, %rax
	movapd	%xmm4, %xmm3
	movapd	%xmm4, %xmm0
	leaq	-1504(%r10,%rax), %rax
	.p2align 4,,10
	.p2align 3
.L156:
	movl	8(%rax), %ebx
	pxor	%xmm1, %xmm1
	pxor	%xmm5, %xmm5
	movl	152(%rax), %r13d
	cvtsi2sdq	(%rax), %xmm1
	addq	$192, %rax
	cvtsi2sdq	%rbx, %xmm5
	movq	%rbx, %rdx
	movl	-136(%rax), %ebx
	movq	%rbx, %r12
	addl	%r12d, %edx
	mulsd	%xmm5, %xmm1
	pxor	%xmm5, %xmm5
	cvtsi2sdq	%rbx, %xmm5
	movl	-88(%rax), %ebx
	addl	%ebx, %edx
	addl	%r13d, %edx
	addsd	%xmm1, %xmm0
	pxor	%xmm1, %xmm1
	movl	%edx, %edx
	cvtsi2sdq	-144(%rax), %xmm1
	addq	%rdx, %rcx
	movq	%rsi, %rdx
	leaq	4(%rsi), %rsi
	mulsd	%xmm5, %xmm1
	pxor	%xmm5, %xmm5
	cvtsi2sdq	%rbx, %xmm5
	addsd	%xmm1, %xmm3
	pxor	%xmm1, %xmm1
	cvtsi2sdq	-96(%rax), %xmm1
	mulsd	%xmm5, %xmm1
	pxor	%xmm5, %xmm5
	cvtsi2sdq	%r13, %xmm5
	addsd	%xmm1, %xmm2
	pxor	%xmm1, %xmm1
	cvtsi2sdq	-48(%rax), %xmm1
	mulsd	%xmm5, %xmm1
	addsd	%xmm1, %xmm4
	cmpq	%rsi, %r11
	jnb	.L156
	addsd	%xmm4, %xmm2
.L147:
	cmpq	%r11, %rdx
	jnb	.L157
	leaq	(%rdx,%rdx,2), %rax
	leaq	32(%r10,%r9), %rsi
	salq	$4, %rax
	leaq	32(%r10,%rax), %rax
	.p2align 4,,10
	.p2align 3
.L160:
	movl	8(%rax), %edx
	pxor	%xmm1, %xmm1
	pxor	%xmm4, %xmm4
	addq	$48, %rax
	cvtsi2sdq	-48(%rax), %xmm1
	cvtsi2sdq	%rdx, %xmm4
	addq	%rdx, %rcx
	mulsd	%xmm4, %xmm1
	addsd	%xmm1, %xmm0
	cmpq	%rsi, %rax
	jne	.L160
.L157:
	addsd	%xmm3, %xmm0
	leaq	(%r8,%rdi), %rax
	pxor	%xmm1, %xmm1
	cvtsi2sdq	%rax, %xmm1
	mulsd	.LC2(%rip), %xmm1
	addsd	%xmm2, %xmm0
	testq	%rcx, %rcx
	js	.L161
	pxor	%xmm2, %xmm2
	cvtsi2sdq	%rcx, %xmm2
.L162:
	divsd	%xmm2, %xmm0
	subq	%rdi, %r8
	pxor	%xmm2, %xmm2
	movl	$1, %eax
	cvtsi2sdq	%r8, %xmm2
	subsd	%xmm0, %xmm1
	movapd	%xmm1, %xmm0
	divsd	%xmm2, %xmm0
	comisd	.LC3(%rip), %xmm0
	ja	.L106
	movsd	.LC4(%rip), %xmm1
	xorl	%eax, %eax
	comisd	%xmm0, %xmm1
	seta	%al
	negl	%eax
	jmp	.L106
	.p2align 4,,10
	.p2align 3
.L111:
	movq	16(%rsi), %rdx
	leaq	32(%rsp), %r12
	movb	$0, 40(%rsp)
	movq	%r12, 16(%rsp)
	movq	24(%rbx), %rbp
	movq	%rdx, 32(%rsp)
	movq	8(%rsi), %rdx
	movq	$8, 24(%rsp)
	movq	%rdx, 48(%rsp)
	movl	%eax, 56(%rsp)
	cmpq	32(%rbx), %rbp
	je	.L114
	leaq	16(%rbp), %rdx
	movq	%rdx, 0(%rbp)
	movq	16(%rsp), %rax
	cmpq	%r12, %rax
	je	.L115
	movq	%rax, 0(%rbp)
	movq	32(%rsp), %rax
	movq	%rax, 16(%rbp)
.L116:
	movq	$8, 8(%rbp)
	movq	48(%rsp), %rax
	movq	%rax, 32(%rbp)
	movl	56(%rsp), %eax
	movl	%eax, 40(%rbp)
	addq	$48, 24(%rbx)
.L117:
	movq	(%rbx), %rdi
	jmp	.L113
	.p2align 4,,10
	.p2align 3
.L192:
	movq	%rdi, (%rbx)
	jmp	.L113
	.p2align 4,,10
	.p2align 3
.L161:
	movq	%rcx, %rax
	andl	$1, %ecx
	pxor	%xmm2, %xmm2
	shrq	%rax
	orq	%rcx, %rax
	cvtsi2sdq	%rax, %xmm2
	addsd	%xmm2, %xmm2
	jmp	.L162
	.p2align 4,,10
	.p2align 3
.L114:
	movq	16(%rbx), %r13
	movq	%rbp, %r14
	movabsq	$-6148914691236517205, %rsi
	subq	%r13, %r14
	movq	%r14, %rcx
	sarq	$4, %rcx
	imulq	%rsi, %rcx
	movabsq	$192153584101141162, %rsi
	cmpq	%rsi, %rcx
	je	.L194
	cmpq	%r13, %rbp
	je	.L195
	leaq	(%rcx,%rcx), %rsi
	cmpq	%rcx, %rsi
	jb	.L168
	testq	%rsi, %rsi
	jne	.L196
	leaq	16(%r14), %r8
	xorl	%ecx, %ecx
	movl	$8, %esi
	movq	$0, 8(%rsp)
	movq	%r8, (%r14)
	movl	$48, %r15d
.L165:
	leaq	1(%rsi), %rdi
	cmpl	$8, %edi
	jnb	.L126
	testb	$4, %dil
	jne	.L197
	testl	%edi, %edi
	je	.L132
	movzbl	32(%rsp), %r9d
	movb	%r9b, (%r8)
	testb	$2, %dil
	jne	.L198
	.p2align 4,,10
	.p2align 3
.L132:
	movq	%rsi, 8(%r14)
	movq	%r12, 16(%rsp)
	movq	$0, 24(%rsp)
	movb	$0, 32(%rsp)
	movq	%rdx, 32(%r14)
	movl	%eax, 40(%r14)
	cmpq	%r13, %rbp
	je	.L133
	movq	%r13, %rax
	movq	%rcx, %rdx
	jmp	.L142
	.p2align 4,,10
	.p2align 3
.L134:
	movq	%rsi, (%rdx)
	movq	16(%rax), %rsi
	movq	%rsi, 16(%rdx)
.L189:
	movq	8(%rax), %r8
.L141:
	movq	%r8, 8(%rdx)
	movq	32(%rax), %rsi
	addq	$48, %rax
	addq	$48, %rdx
	movq	%rsi, -16(%rdx)
	movl	-8(%rax), %esi
	movl	%esi, -8(%rdx)
	cmpq	%rax, %rbp
	je	.L199
.L142:
	leaq	16(%rdx), %rdi
	leaq	16(%rax), %r8
	movq	%rdi, (%rdx)
	movq	(%rax), %rsi
	cmpq	%r8, %rsi
	jne	.L134
	movq	8(%rax), %r8
	leaq	1(%r8), %r9
	cmpl	$8, %r9d
	jnb	.L135
	testb	$4, %r9b
	jne	.L200
	testl	%r9d, %r9d
	je	.L141
	movzbl	(%rsi), %r8d
	movb	%r8b, (%rdi)
	testb	$2, %r9b
	je	.L189
	movl	%r9d, %r9d
	movzwl	-2(%rsi,%r9), %esi
	movw	%si, -2(%rdi,%r9)
	movq	8(%rax), %r8
	jmp	.L141
	.p2align 4,,10
	.p2align 3
.L199:
	subq	$48, %rbp
	subq	%r13, %rbp
	andq	$-16, %rbp
	leaq	96(%rcx,%rbp), %r15
.L133:
	testq	%r13, %r13
	je	.L143
	movq	32(%rbx), %rsi
	movq	%r13, %rdi
	movq	%rcx, (%rsp)
	subq	%r13, %rsi
	call	_ZdlPvm@PLT
	movq	(%rsp), %rcx
	movq	8(%rsp), %rax
	movq	%r15, 24(%rbx)
	movq	16(%rsp), %rdi
	movq	%rcx, 16(%rbx)
	movq	%rax, 32(%rbx)
	cmpq	%r12, %rdi
	je	.L117
	movq	32(%rsp), %rax
	leaq	1(%rax), %rsi
	call	_ZdlPvm@PLT
	jmp	.L117
	.p2align 4,,10
	.p2align 3
.L135:
	movq	(%rsi), %r8
	movq	%r8, (%rdi)
	movl	%r9d, %r8d
	movq	-8(%rsi,%r8), %r10
	movq	%r10, -8(%rdi,%r8)
	leaq	24(%rdx), %r8
	andq	$-8, %r8
	subq	%r8, %rdi
	addl	%edi, %r9d
	subq	%rdi, %rsi
	andl	$-8, %r9d
	cmpl	$8, %r9d
	jb	.L189
	andl	$-8, %r9d
	xorl	%edi, %edi
.L139:
	movl	%edi, %r10d
	addl	$8, %edi
	movq	(%rsi,%r10), %r11
	movq	%r11, (%r8,%r10)
	cmpl	%r9d, %edi
	jb	.L139
	jmp	.L189
	.p2align 4,,10
	.p2align 3
.L115:
	movq	(%rax), %rcx
	movq	%rcx, 16(%rbp)
	movzbl	8(%rax), %eax
	movb	%al, 8(%rdx)
	jmp	.L116
	.p2align 4,,10
	.p2align 3
.L195:
	addq	$1, %rcx
	jc	.L168
	movabsq	$192153584101141162, %rax
	cmpq	%rax, %rcx
	cmovbe	%rcx, %rax
	leaq	(%rax,%rax,2), %r15
	salq	$4, %r15
.L123:
	movq	%r15, %rdi
.LEHB2:
	call	_Znwm@PLT
	movq	%rax, %rcx
	movq	48(%rsp), %rdx
	movl	56(%rsp), %eax
	leaq	(%rcx,%r15), %rdi
	movq	24(%rsp), %rsi
	leaq	48(%rcx), %r15
	addq	%rcx, %r14
	movq	%rdi, 8(%rsp)
	movq	16(%rsp), %rdi
	cmpq	%r12, %rdi
	je	.L201
	movq	%rdi, (%r14)
	movq	32(%rsp), %rdi
	movq	%rdi, 16(%r14)
	jmp	.L132
	.p2align 4,,10
	.p2align 3
.L193:
	pxor	%xmm2, %xmm2
	subq	$32, %rdx
	xorl	%ecx, %ecx
	movapd	%xmm2, %xmm3
	movapd	%xmm2, %xmm0
	jmp	.L147
.L168:
	movabsq	$9223372036854775776, %r15
	jmp	.L123
.L126:
	movq	32(%rsp), %r9
	movq	%r9, (%r8)
	movl	%edi, %r9d
	movq	-8(%r12,%r9), %r10
	movq	%r10, -8(%r8,%r9)
	leaq	8(%r8), %r9
	movq	%r12, %r10
	andq	$-8, %r9
	subq	%r9, %r8
	addl	%r8d, %edi
	subq	%r8, %r10
	andl	$-8, %edi
	cmpl	$8, %edi
	jb	.L132
	movl	%eax, (%rsp)
	andl	$-8, %edi
	movl	%edi, %r11d
	xorl	%edi, %edi
.L130:
	movl	%edi, %r8d
	addl	$8, %edi
	movq	(%r10,%r8), %rax
	movq	%rax, (%r9,%r8)
	cmpl	%r11d, %edi
	jb	.L130
	movl	(%rsp), %eax
	jmp	.L132
.L200:
	movl	(%rsi), %r8d
	movl	%r9d, %r9d
	movl	%r8d, (%rdi)
	movl	-4(%rsi,%r9), %esi
	movl	%esi, -4(%rdi,%r9)
	movq	8(%rax), %r8
	jmp	.L141
.L196:
	movabsq	$192153584101141162, %rax
	cmpq	%rax, %rsi
	cmova	%rax, %rsi
	imulq	$48, %rsi, %r15
	jmp	.L123
.L163:
	leaq	16(%rsp), %rdi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	movq	72(%rsp), %rax
	subq	%fs:40, %rax
	je	.L164
.L191:
	call	__stack_chk_fail@PLT
.L197:
	movl	32(%rsp), %r9d
	movl	%edi, %edi
	movl	%r9d, (%r8)
	movl	-4(%r12,%rdi), %r9d
	movl	%r9d, -4(%r8,%rdi)
	jmp	.L132
.L198:
	movl	%edi, %edi
	movzwl	-2(%r12,%rdi), %r9d
	movw	%r9w, -2(%r8,%rdi)
	jmp	.L132
.L143:
	movq	8(%rsp), %rax
	movq	%rcx, 16(%rbx)
	movq	%r15, 24(%rbx)
	movq	%rax, 32(%rbx)
	jmp	.L117
.L194:
	movq	72(%rsp), %rax
	subq	%fs:40, %rax
	jne	.L191
	leaq	.LC1(%rip), %rdi
	call	_ZSt20__throw_length_errorPKc@PLT
.LEHE2:
.L201:
	leaq	16(%r14), %r8
	movq	%r8, (%r14)
	jmp	.L165
.L170:
	endbr64
	movq	%rax, %rbx
	jmp	.L163
.L164:
	movq	%rbx, %rdi
.LEHB3:
	call	_Unwind_Resume@PLT
.LEHE3:
	.cfi_endproc
.LFE13176:
	.section	.gcc_except_table._ZN3v2a7Handler6on_msgERK3Msg,"aG",@progbits,_ZN3v2a7Handler6on_msgERK3Msg,comdat
.LLSDA13176:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE13176-.LLSDACSB13176
.LLSDACSB13176:
	.uleb128 .LEHB2-.LFB13176
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L170-.LFB13176
	.uleb128 0
	.uleb128 .LEHB3-.LFB13176
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
.LLSDACSE13176:
	.section	.text._ZN3v2a7Handler6on_msgERK3Msg,"axG",@progbits,_ZN3v2a7Handler6on_msgERK3Msg,comdat
	.size	_ZN3v2a7Handler6on_msgERK3Msg, .-_ZN3v2a7Handler6on_msgERK3Msg
	.text
	.p2align 4
	.globl	_Z10on_msg_v2aRN3v2a7HandlerERK3Msg
	.type	_Z10on_msg_v2aRN3v2a7HandlerERK3Msg, @function
_Z10on_msg_v2aRN3v2a7HandlerERK3Msg:
.LFB13219:
	.cfi_startproc
	endbr64
	jmp	_ZN3v2a7Handler6on_msgERK3Msg
	.cfi_endproc
.LFE13219:
	.size	_Z10on_msg_v2aRN3v2a7HandlerERK3Msg, .-_Z10on_msg_v2aRN3v2a7HandlerERK3Msg
	.section	.text._ZN2v27Handler6on_msgERK3Msg,"axG",@progbits,_ZN2v27Handler6on_msgERK3Msg,comdat
	.align 2
	.p2align 4
	.weak	_ZN2v27Handler6on_msgERK3Msg
	.type	_ZN2v27Handler6on_msgERK3Msg, @function
_ZN2v27Handler6on_msgERK3Msg:
.LFB13185:
	.cfi_startproc
	.cfi_personality 0x9b,DW.ref.__gxx_personality_v0
	.cfi_lsda 0x1b,.LLSDA13185
	endbr64
	pushq	%r15
	.cfi_def_cfa_offset 16
	.cfi_offset 15, -16
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
	subq	$104, %rsp
	.cfi_def_cfa_offset 160
	movq	%fs:40, %rax
	movq	%rax, 88(%rsp)
	movl	4(%rsi), %eax
	testl	%eax, %eax
	je	.L206
	cmpq	$0, 8(%rsi)
	movq	%rsi, %rbx
	jle	.L206
	movzbl	1(%rsi), %edx
	cmpb	$66, %dl
	je	.L252
	cmpb	$83, %dl
	je	.L252
.L206:
	addq	$1, 24(%rdi)
.L205:
	xorl	%eax, %eax
.L203:
	movq	88(%rsp), %rdx
	subq	%fs:40, %rdx
	jne	.L274
	addq	$104, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 56
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
	.p2align 4,,10
	.p2align 3
.L252:
	.cfi_restore_state
	movzwl	2(%rbx), %ebp
	salq	$6, %rbp
	addq	(%rdi), %rbp
	addq	$1, 56(%rbp)
	cmpb	$81, (%rbx)
	jne	.L208
	cmpb	$66, 1(%rbx)
	movq	8(%rbx), %rax
	je	.L275
	movq	%rax, 8(%rbp)
	movq	0(%rbp), %rax
.L210:
	testq	%rax, %rax
	jle	.L205
	movq	8(%rbp), %rdx
	cmpq	%rax, %rdx
	jle	.L205
	movq	24(%rbp), %rsi
	testq	%rsi, %rsi
	je	.L205
	leaq	(%rdx,%rax), %rcx
	movq	16(%rbp), %rdi
	subq	%rax, %rdx
	movl	$1, %eax
	imulq	%rsi, %rcx
	addq	%rdi, %rdi
	imulq	%rsi, %rdx
	subq	%rdi, %rcx
	addq	%rcx, %rcx
	cmpq	%rdx, %rcx
	jg	.L203
	negq	%rdx
	xorl	%eax, %eax
	cmpq	%rcx, %rdx
	setg	%al
	negl	%eax
	jmp	.L203
	.p2align 4,,10
	.p2align 3
.L208:
	movq	16(%rbx), %rdx
	leaq	48(%rsp), %r13
	movb	$0, 56(%rsp)
	movq	%r13, 32(%rsp)
	movq	40(%rbp), %r12
	movq	%rdx, 48(%rsp)
	movq	8(%rbx), %rdx
	movq	$8, 40(%rsp)
	movq	%rdx, 64(%rsp)
	movl	%eax, 72(%rsp)
	cmpq	48(%rbp), %r12
	je	.L211
	leaq	16(%r12), %rdx
	movq	%rdx, (%r12)
	movq	32(%rsp), %rax
	cmpq	%r13, %rax
	je	.L212
	movq	%rax, (%r12)
	movq	48(%rsp), %rax
	movq	%rax, 16(%r12)
.L213:
	movq	$8, 8(%r12)
	movq	64(%rsp), %rax
	movq	%rax, 32(%r12)
	movl	72(%rsp), %eax
	movl	%eax, 40(%r12)
	addq	$48, 40(%rbp)
.L214:
	movl	4(%rbx), %eax
	movq	8(%rbx), %rcx
	movq	32(%rbp), %rdx
	imulq	%rax, %rcx
	movq	%rax, %xmm2
	movq	40(%rbp), %rax
	subq	%rdx, %rax
	movq	%rcx, %xmm0
	punpcklqdq	%xmm2, %xmm0
	paddq	16(%rbp), %xmm0
	movaps	%xmm0, 16(%rbp)
	cmpq	$1536, %rax
	jbe	.L272
	leaq	-1584(%rdx,%rax), %rdx
	movl	40(%rdx), %eax
	movq	32(%rdx), %rcx
	imulq	%rax, %rcx
	movq	%rax, %xmm3
	movq	%rcx, %xmm1
	punpcklqdq	%xmm3, %xmm1
	psubq	%xmm1, %xmm0
	movaps	%xmm0, 16(%rbp)
.L272:
	movq	0(%rbp), %rax
	jmp	.L210
	.p2align 4,,10
	.p2align 3
.L275:
	movq	%rax, 0(%rbp)
	jmp	.L210
	.p2align 4,,10
	.p2align 3
.L211:
	movq	32(%rbp), %r15
	movq	%r12, %r14
	movabsq	$-6148914691236517205, %rsi
	subq	%r15, %r14
	movq	%r14, %rcx
	sarq	$4, %rcx
	imulq	%rsi, %rcx
	movabsq	$192153584101141162, %rsi
	cmpq	%rsi, %rcx
	je	.L276
	cmpq	%r15, %r12
	je	.L277
	leaq	(%rcx,%rcx), %rsi
	cmpq	%rcx, %rsi
	jb	.L249
	testq	%rsi, %rsi
	jne	.L278
	leaq	16(%r14), %r8
	movl	$8, %esi
	xorl	%ecx, %ecx
	movq	$0, 24(%rsp)
	movq	%r8, (%r14)
	movq	$48, 16(%rsp)
.L246:
	leaq	1(%rsi), %rdi
	cmpl	$8, %edi
	jnb	.L223
	testb	$4, %dil
	jne	.L279
	testl	%edi, %edi
	je	.L229
	movzbl	48(%rsp), %r9d
	movb	%r9b, (%r8)
	testb	$2, %dil
	jne	.L280
	.p2align 4,,10
	.p2align 3
.L229:
	movq	%rsi, 8(%r14)
	movq	%r13, 32(%rsp)
	movq	$0, 40(%rsp)
	movb	$0, 48(%rsp)
	movq	%rdx, 32(%r14)
	movl	%eax, 40(%r14)
	cmpq	%r15, %r12
	je	.L230
	movq	%r15, %rax
	movq	%rcx, %rdx
	jmp	.L239
	.p2align 4,,10
	.p2align 3
.L231:
	movq	%rsi, (%rdx)
	movq	16(%rax), %rsi
	movq	%rsi, 16(%rdx)
.L271:
	movq	8(%rax), %r8
.L238:
	movq	%r8, 8(%rdx)
	movq	32(%rax), %rsi
	addq	$48, %rax
	addq	$48, %rdx
	movq	%rsi, -16(%rdx)
	movl	-8(%rax), %esi
	movl	%esi, -8(%rdx)
	cmpq	%rax, %r12
	je	.L281
.L239:
	leaq	16(%rdx), %rdi
	leaq	16(%rax), %r8
	movq	%rdi, (%rdx)
	movq	(%rax), %rsi
	cmpq	%r8, %rsi
	jne	.L231
	movq	8(%rax), %r8
	leaq	1(%r8), %r9
	cmpl	$8, %r9d
	jnb	.L232
	testb	$4, %r9b
	jne	.L282
	testl	%r9d, %r9d
	je	.L238
	movzbl	(%rsi), %r8d
	movb	%r8b, (%rdi)
	testb	$2, %r9b
	je	.L271
	movl	%r9d, %r9d
	movzwl	-2(%rsi,%r9), %esi
	movw	%si, -2(%rdi,%r9)
	movq	8(%rax), %r8
	jmp	.L238
	.p2align 4,,10
	.p2align 3
.L281:
	subq	$48, %r12
	subq	%r15, %r12
	andq	$-16, %r12
	leaq	96(%rcx,%r12), %rax
	movq	%rax, 16(%rsp)
.L230:
	testq	%r15, %r15
	je	.L240
	movq	48(%rbp), %rsi
	movq	%r15, %rdi
	movq	%rcx, 8(%rsp)
	subq	%r15, %rsi
	call	_ZdlPvm@PLT
	movq	16(%rsp), %rax
	movq	8(%rsp), %rcx
	movq	32(%rsp), %rdi
	movq	%rax, 40(%rbp)
	movq	24(%rsp), %rax
	movq	%rcx, 32(%rbp)
	movq	%rax, 48(%rbp)
	cmpq	%r13, %rdi
	je	.L214
	movq	48(%rsp), %rax
	leaq	1(%rax), %rsi
	call	_ZdlPvm@PLT
	jmp	.L214
	.p2align 4,,10
	.p2align 3
.L232:
	movq	(%rsi), %r8
	movq	%r8, (%rdi)
	movl	%r9d, %r8d
	movq	-8(%rsi,%r8), %r10
	movq	%r10, -8(%rdi,%r8)
	leaq	24(%rdx), %r8
	andq	$-8, %r8
	subq	%r8, %rdi
	addl	%edi, %r9d
	subq	%rdi, %rsi
	andl	$-8, %r9d
	cmpl	$8, %r9d
	jb	.L271
	andl	$-8, %r9d
	xorl	%edi, %edi
.L236:
	movl	%edi, %r10d
	addl	$8, %edi
	movq	(%rsi,%r10), %r11
	movq	%r11, (%r8,%r10)
	cmpl	%r9d, %edi
	jb	.L236
	jmp	.L271
	.p2align 4,,10
	.p2align 3
.L212:
	movq	(%rax), %rcx
	movq	%rcx, 16(%r12)
	movzbl	8(%rax), %eax
	movb	%al, 8(%rdx)
	jmp	.L213
	.p2align 4,,10
	.p2align 3
.L277:
	addq	$1, %rcx
	jc	.L249
	movabsq	$192153584101141162, %rax
	cmpq	%rax, %rcx
	cmovbe	%rcx, %rax
	leaq	(%rax,%rax,2), %rax
	salq	$4, %rax
	movq	%rax, 8(%rsp)
.L220:
	movq	8(%rsp), %rdi
.LEHB4:
	call	_Znwm@PLT
	movq	8(%rsp), %rdi
	movq	%rax, %rcx
	movq	64(%rsp), %rdx
	leaq	48(%rcx), %r11
	movl	72(%rsp), %eax
	movq	40(%rsp), %rsi
	addq	%rcx, %r14
	addq	%rcx, %rdi
	movq	%r11, 16(%rsp)
	movq	%rdi, 24(%rsp)
	movq	32(%rsp), %rdi
	cmpq	%r13, %rdi
	je	.L283
	movq	%rdi, (%r14)
	movq	48(%rsp), %rdi
	movq	%rdi, 16(%r14)
	jmp	.L229
	.p2align 4,,10
	.p2align 3
.L249:
	movabsq	$9223372036854775776, %rax
	movq	%rax, 8(%rsp)
	jmp	.L220
.L223:
	movq	48(%rsp), %r9
	movq	%r9, (%r8)
	movl	%edi, %r9d
	movq	-8(%r13,%r9), %r10
	movq	%r10, -8(%r8,%r9)
	leaq	8(%r8), %r9
	movq	%r13, %r10
	andq	$-8, %r9
	subq	%r9, %r8
	addl	%r8d, %edi
	subq	%r8, %r10
	andl	$-8, %edi
	cmpl	$8, %edi
	jb	.L229
	movl	%eax, 8(%rsp)
	andl	$-8, %edi
	movl	%edi, %r11d
	xorl	%edi, %edi
.L227:
	movl	%edi, %r8d
	addl	$8, %edi
	movq	(%r10,%r8), %rax
	movq	%rax, (%r9,%r8)
	cmpl	%r11d, %edi
	jb	.L227
	movl	8(%rsp), %eax
	jmp	.L229
.L282:
	movl	(%rsi), %r8d
	movl	%r9d, %r9d
	movl	%r8d, (%rdi)
	movl	-4(%rsi,%r9), %esi
	movl	%esi, -4(%rdi,%r9)
	movq	8(%rax), %r8
	jmp	.L238
.L278:
	movabsq	$192153584101141162, %rax
	cmpq	%rax, %rsi
	cmova	%rax, %rsi
	imulq	$48, %rsi, %rax
	movq	%rax, 8(%rsp)
	jmp	.L220
.L244:
	leaq	32(%rsp), %rdi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	movq	88(%rsp), %rax
	subq	%fs:40, %rax
	je	.L245
.L274:
	call	__stack_chk_fail@PLT
.L279:
	movl	48(%rsp), %r9d
	movl	%edi, %edi
	movl	%r9d, (%r8)
	movl	-4(%r13,%rdi), %r9d
	movl	%r9d, -4(%r8,%rdi)
	jmp	.L229
.L280:
	movl	%edi, %edi
	movzwl	-2(%r13,%rdi), %r9d
	movw	%r9w, -2(%r8,%rdi)
	jmp	.L229
.L240:
	movq	16(%rsp), %rax
	movq	%rcx, 32(%rbp)
	movq	%rax, 40(%rbp)
	movq	24(%rsp), %rax
	movq	%rax, 48(%rbp)
	jmp	.L214
.L276:
	movq	88(%rsp), %rax
	subq	%fs:40, %rax
	jne	.L274
	leaq	.LC1(%rip), %rdi
	call	_ZSt20__throw_length_errorPKc@PLT
.LEHE4:
.L283:
	leaq	16(%r14), %r8
	movq	%r8, (%r14)
	jmp	.L246
.L251:
	endbr64
	movq	%rax, %rbx
	jmp	.L244
.L245:
	movq	%rbx, %rdi
.LEHB5:
	call	_Unwind_Resume@PLT
.LEHE5:
	.cfi_endproc
.LFE13185:
	.section	.gcc_except_table._ZN2v27Handler6on_msgERK3Msg,"aG",@progbits,_ZN2v27Handler6on_msgERK3Msg,comdat
.LLSDA13185:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE13185-.LLSDACSB13185
.LLSDACSB13185:
	.uleb128 .LEHB4-.LFB13185
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L251-.LFB13185
	.uleb128 0
	.uleb128 .LEHB5-.LFB13185
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
.LLSDACSE13185:
	.section	.text._ZN2v27Handler6on_msgERK3Msg,"axG",@progbits,_ZN2v27Handler6on_msgERK3Msg,comdat
	.size	_ZN2v27Handler6on_msgERK3Msg, .-_ZN2v27Handler6on_msgERK3Msg
	.text
	.p2align 4
	.globl	_Z9on_msg_v2RN2v27HandlerERK3Msg
	.type	_Z9on_msg_v2RN2v27HandlerERK3Msg, @function
_Z9on_msg_v2RN2v27HandlerERK3Msg:
.LFB13220:
	.cfi_startproc
	endbr64
	jmp	_ZN2v27Handler6on_msgERK3Msg
	.cfi_endproc
.LFE13220:
	.size	_Z9on_msg_v2RN2v27HandlerERK3Msg, .-_Z9on_msg_v2RN2v27HandlerERK3Msg
	.section	.text._ZN2v37Handler6on_msgERK3Msg,"axG",@progbits,_ZN2v37Handler6on_msgERK3Msg,comdat
	.align 2
	.p2align 4
	.weak	_ZN2v37Handler6on_msgERK3Msg
	.type	_ZN2v37Handler6on_msgERK3Msg, @function
_ZN2v37Handler6on_msgERK3Msg:
.LFB13196:
	.cfi_startproc
	.cfi_personality 0x9b,DW.ref.__gxx_personality_v0
	.cfi_lsda 0x1b,.LLSDA13196
	endbr64
	pushq	%r15
	.cfi_def_cfa_offset 16
	.cfi_offset 15, -16
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
	movq	%rsi, %rbp
	pushq	%rbx
	.cfi_def_cfa_offset 56
	.cfi_offset 3, -56
	subq	$104, %rsp
	.cfi_def_cfa_offset 160
	movzbl	1(%rsi), %edx
	movq	%fs:40, %rax
	movq	%rax, 88(%rsp)
	movl	4(%rsi), %eax
	cmpq	$0, 8(%rsi)
	setg	%sil
	testl	%eax, %eax
	setne	%cl
	testb	%cl, %sil
	je	.L331
	cmpb	$66, %dl
	sete	%cl
	cmpb	$83, %dl
	sete	%dl
	orb	%dl, %cl
	je	.L331
	movzwl	2(%rbp), %ebx
	salq	$6, %rbx
	addq	(%rdi), %rbx
	addq	$1, 56(%rbx)
	cmpb	$81, 0(%rbp)
	jne	.L289
	movq	8(%rbp), %rdx
	xorl	%eax, %eax
	cmpb	$83, 1(%rbp)
	sete	%al
	movq	16(%rbx), %rcx
	movq	%rdx, (%rbx,%rax,8)
	movq	24(%rbx), %rdx
.L290:
	movq	(%rbx), %rdi
	movq	8(%rbx), %rax
	testq	%rdi, %rdi
	setg	%r8b
	cmpq	%rax, %rdi
	setl	%sil
	testb	%sil, %r8b
	je	.L288
	testq	%rdx, %rdx
	je	.L288
	leaq	(%rdi,%rax), %rsi
	subq	%rdi, %rax
	addq	%rcx, %rcx
	imulq	%rdx, %rsi
	imulq	%rdx, %rax
	xorl	%edx, %edx
	subq	%rcx, %rsi
	leaq	(%rsi,%rsi), %rcx
	cmpq	%rax, %rcx
	setg	%dl
	negq	%rax
	cmpq	%rcx, %rax
	movl	%edx, %eax
	setg	%cl
	movzbl	%cl, %ecx
	subl	%ecx, %eax
.L285:
	movq	88(%rsp), %rdx
	subq	%fs:40, %rdx
	jne	.L352
	addq	$104, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 56
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
	.p2align 4,,10
	.p2align 3
.L289:
	.cfi_restore_state
	movq	16(%rbp), %rdx
	leaq	48(%rsp), %r13
	movb	$0, 56(%rsp)
	movq	%r13, 32(%rsp)
	movq	40(%rbx), %r12
	movq	%rdx, 48(%rsp)
	movq	8(%rbp), %rdx
	movq	$8, 40(%rsp)
	movq	%rdx, 64(%rsp)
	movl	%eax, 72(%rsp)
	cmpq	48(%rbx), %r12
	je	.L291
	leaq	16(%r12), %rdx
	movq	%rdx, (%r12)
	movq	32(%rsp), %rax
	cmpq	%r13, %rax
	je	.L292
	movq	%rax, (%r12)
	movq	48(%rsp), %rax
	movq	%rax, 16(%r12)
.L293:
	movq	$8, 8(%r12)
	movq	64(%rsp), %rax
	movq	%rax, 32(%r12)
	movl	72(%rsp), %eax
	movl	%eax, 40(%r12)
	addq	$48, 40(%rbx)
.L294:
	movl	4(%rbp), %edx
	movq	8(%rbp), %rcx
	movq	32(%rbx), %rsi
	movq	40(%rbx), %rax
	imulq	%rdx, %rcx
	addq	24(%rbx), %rdx
	addq	16(%rbx), %rcx
	subq	%rsi, %rax
	movq	%rcx, 16(%rbx)
	movq	%rdx, 24(%rbx)
	cmpq	$1536, %rax
	jbe	.L290
	leaq	-1584(%rsi,%rax), %rsi
	movl	40(%rsi), %eax
	movq	32(%rsi), %rdi
	imulq	%rax, %rdi
	subq	%rax, %rdx
	movq	%rdx, 24(%rbx)
	subq	%rdi, %rcx
	movq	%rcx, 16(%rbx)
	jmp	.L290
	.p2align 4,,10
	.p2align 3
.L331:
	addq	$1, 24(%rdi)
	.p2align 4,,10
	.p2align 3
.L288:
	xorl	%eax, %eax
	jmp	.L285
	.p2align 4,,10
	.p2align 3
.L291:
	movq	32(%rbx), %r15
	movq	%r12, %r14
	movabsq	$-6148914691236517205, %rsi
	subq	%r15, %r14
	movq	%r14, %rcx
	sarq	$4, %rcx
	imulq	%rsi, %rcx
	movabsq	$192153584101141162, %rsi
	cmpq	%rsi, %rcx
	je	.L353
	cmpq	%r15, %r12
	je	.L354
	leaq	(%rcx,%rcx), %rsi
	cmpq	%rcx, %rsi
	jb	.L329
	testq	%rsi, %rsi
	jne	.L355
	leaq	16(%r14), %r8
	movl	$8, %esi
	xorl	%ecx, %ecx
	movq	$0, 24(%rsp)
	movq	%r8, (%r14)
	movq	$48, 16(%rsp)
.L326:
	leaq	1(%rsi), %rdi
	cmpl	$8, %edi
	jnb	.L303
	testb	$4, %dil
	jne	.L356
	testl	%edi, %edi
	je	.L309
	movzbl	48(%rsp), %r9d
	movb	%r9b, (%r8)
	testb	$2, %dil
	jne	.L357
	.p2align 4,,10
	.p2align 3
.L309:
	movq	%rsi, 8(%r14)
	movq	%r13, 32(%rsp)
	movq	$0, 40(%rsp)
	movb	$0, 48(%rsp)
	movq	%rdx, 32(%r14)
	movl	%eax, 40(%r14)
	cmpq	%r15, %r12
	je	.L310
	movq	%r15, %rax
	movq	%rcx, %rdx
	jmp	.L319
	.p2align 4,,10
	.p2align 3
.L311:
	movq	%rsi, (%rdx)
	movq	16(%rax), %rsi
	movq	%rsi, 16(%rdx)
.L350:
	movq	8(%rax), %r8
.L318:
	movq	%r8, 8(%rdx)
	movq	32(%rax), %rsi
	addq	$48, %rax
	addq	$48, %rdx
	movq	%rsi, -16(%rdx)
	movl	-8(%rax), %esi
	movl	%esi, -8(%rdx)
	cmpq	%rax, %r12
	je	.L358
.L319:
	leaq	16(%rdx), %rdi
	leaq	16(%rax), %r8
	movq	%rdi, (%rdx)
	movq	(%rax), %rsi
	cmpq	%r8, %rsi
	jne	.L311
	movq	8(%rax), %r8
	leaq	1(%r8), %r9
	cmpl	$8, %r9d
	jnb	.L312
	testb	$4, %r9b
	jne	.L359
	testl	%r9d, %r9d
	je	.L318
	movzbl	(%rsi), %r8d
	movb	%r8b, (%rdi)
	testb	$2, %r9b
	je	.L350
	movl	%r9d, %r9d
	movzwl	-2(%rsi,%r9), %esi
	movw	%si, -2(%rdi,%r9)
	movq	8(%rax), %r8
	jmp	.L318
	.p2align 4,,10
	.p2align 3
.L292:
	movq	(%rax), %rcx
	movq	%rcx, 16(%r12)
	movzbl	8(%rax), %eax
	movb	%al, 8(%rdx)
	jmp	.L293
	.p2align 4,,10
	.p2align 3
.L358:
	subq	$48, %r12
	subq	%r15, %r12
	andq	$-16, %r12
	leaq	96(%rcx,%r12), %rax
	movq	%rax, 16(%rsp)
.L310:
	testq	%r15, %r15
	je	.L320
	movq	48(%rbx), %rsi
	movq	%r15, %rdi
	movq	%rcx, 8(%rsp)
	subq	%r15, %rsi
	call	_ZdlPvm@PLT
	movq	16(%rsp), %rax
	movq	8(%rsp), %rcx
	movq	32(%rsp), %rdi
	movq	%rax, 40(%rbx)
	movq	24(%rsp), %rax
	movq	%rcx, 32(%rbx)
	movq	%rax, 48(%rbx)
	cmpq	%r13, %rdi
	je	.L294
	movq	48(%rsp), %rax
	leaq	1(%rax), %rsi
	call	_ZdlPvm@PLT
	jmp	.L294
	.p2align 4,,10
	.p2align 3
.L312:
	movq	(%rsi), %r8
	movq	%r8, (%rdi)
	movl	%r9d, %r8d
	movq	-8(%rsi,%r8), %r10
	movq	%r10, -8(%rdi,%r8)
	leaq	24(%rdx), %r8
	andq	$-8, %r8
	subq	%r8, %rdi
	addl	%edi, %r9d
	subq	%rdi, %rsi
	andl	$-8, %r9d
	cmpl	$8, %r9d
	jb	.L350
	andl	$-8, %r9d
	xorl	%edi, %edi
.L316:
	movl	%edi, %r10d
	addl	$8, %edi
	movq	(%rsi,%r10), %r11
	movq	%r11, (%r8,%r10)
	cmpl	%r9d, %edi
	jb	.L316
	jmp	.L350
	.p2align 4,,10
	.p2align 3
.L354:
	addq	$1, %rcx
	jc	.L329
	movabsq	$192153584101141162, %rax
	cmpq	%rax, %rcx
	cmova	%rax, %rcx
	leaq	(%rcx,%rcx,2), %rax
	salq	$4, %rax
	movq	%rax, 8(%rsp)
.L300:
	movq	8(%rsp), %rdi
.LEHB6:
	call	_Znwm@PLT
	movq	8(%rsp), %rdi
	movq	%rax, %rcx
	movq	64(%rsp), %rdx
	leaq	48(%rcx), %r11
	movl	72(%rsp), %eax
	movq	40(%rsp), %rsi
	addq	%rcx, %r14
	addq	%rcx, %rdi
	movq	%r11, 16(%rsp)
	movq	%rdi, 24(%rsp)
	movq	32(%rsp), %rdi
	cmpq	%r13, %rdi
	je	.L360
	movq	%rdi, (%r14)
	movq	48(%rsp), %rdi
	movq	%rdi, 16(%r14)
	jmp	.L309
	.p2align 4,,10
	.p2align 3
.L329:
	movabsq	$9223372036854775776, %rax
	movq	%rax, 8(%rsp)
	jmp	.L300
.L303:
	movq	48(%rsp), %r9
	movq	%r9, (%r8)
	movl	%edi, %r9d
	movq	-8(%r13,%r9), %r10
	movq	%r10, -8(%r8,%r9)
	leaq	8(%r8), %r9
	movq	%r13, %r10
	andq	$-8, %r9
	subq	%r9, %r8
	addl	%r8d, %edi
	subq	%r8, %r10
	andl	$-8, %edi
	cmpl	$8, %edi
	jb	.L309
	movl	%eax, 8(%rsp)
	andl	$-8, %edi
	movl	%edi, %r11d
	xorl	%edi, %edi
.L307:
	movl	%edi, %r8d
	addl	$8, %edi
	movq	(%r10,%r8), %rax
	movq	%rax, (%r9,%r8)
	cmpl	%r11d, %edi
	jb	.L307
	movl	8(%rsp), %eax
	jmp	.L309
.L359:
	movl	(%rsi), %r8d
	movl	%r9d, %r9d
	movl	%r8d, (%rdi)
	movl	-4(%rsi,%r9), %esi
	movl	%esi, -4(%rdi,%r9)
	movq	8(%rax), %r8
	jmp	.L318
.L355:
	movabsq	$192153584101141162, %rax
	cmpq	%rax, %rsi
	cmova	%rax, %rsi
	leaq	(%rsi,%rsi,2), %rax
	salq	$4, %rax
	movq	%rax, 8(%rsp)
	jmp	.L300
.L356:
	movl	48(%rsp), %r9d
	movl	%edi, %edi
	movl	%r9d, (%r8)
	movl	-4(%r13,%rdi), %r9d
	movl	%r9d, -4(%r8,%rdi)
	jmp	.L309
.L357:
	movl	%edi, %edi
	movzwl	-2(%r13,%rdi), %r9d
	movw	%r9w, -2(%r8,%rdi)
	jmp	.L309
.L324:
	leaq	32(%rsp), %rdi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	movq	88(%rsp), %rax
	subq	%fs:40, %rax
	je	.L325
.L352:
	call	__stack_chk_fail@PLT
.L320:
	movq	16(%rsp), %rax
	movq	%rcx, 32(%rbx)
	movq	%rax, 40(%rbx)
	movq	24(%rsp), %rax
	movq	%rax, 48(%rbx)
	jmp	.L294
.L353:
	movq	88(%rsp), %rax
	subq	%fs:40, %rax
	jne	.L352
	leaq	.LC1(%rip), %rdi
	call	_ZSt20__throw_length_errorPKc@PLT
.LEHE6:
.L360:
	leaq	16(%r14), %r8
	movq	%r8, (%r14)
	jmp	.L326
.L330:
	endbr64
	movq	%rax, %rbx
	jmp	.L324
.L325:
	movq	%rbx, %rdi
.LEHB7:
	call	_Unwind_Resume@PLT
.LEHE7:
	.cfi_endproc
.LFE13196:
	.section	.gcc_except_table._ZN2v37Handler6on_msgERK3Msg,"aG",@progbits,_ZN2v37Handler6on_msgERK3Msg,comdat
.LLSDA13196:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE13196-.LLSDACSB13196
.LLSDACSB13196:
	.uleb128 .LEHB6-.LFB13196
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L330-.LFB13196
	.uleb128 0
	.uleb128 .LEHB7-.LFB13196
	.uleb128 .LEHE7-.LEHB7
	.uleb128 0
	.uleb128 0
.LLSDACSE13196:
	.section	.text._ZN2v37Handler6on_msgERK3Msg,"axG",@progbits,_ZN2v37Handler6on_msgERK3Msg,comdat
	.size	_ZN2v37Handler6on_msgERK3Msg, .-_ZN2v37Handler6on_msgERK3Msg
	.text
	.p2align 4
	.globl	_Z9on_msg_v3RN2v37HandlerERK3Msg
	.type	_Z9on_msg_v3RN2v37HandlerERK3Msg, @function
_Z9on_msg_v3RN2v37HandlerERK3Msg:
.LFB13221:
	.cfi_startproc
	endbr64
	jmp	_ZN2v37Handler6on_msgERK3Msg
	.cfi_endproc
.LFE13221:
	.size	_Z9on_msg_v3RN2v37HandlerERK3Msg, .-_Z9on_msg_v3RN2v37HandlerERK3Msg
	.section	.rodata.cst8,"aM",@progbits,8
	.align 8
.LC2:
	.long	0
	.long	1071644672
	.align 8
.LC3:
	.long	0
	.long	1070596096
	.align 8
.LC4:
	.long	0
	.long	-1076887552
	.hidden	DW.ref.__gxx_personality_v0
	.weak	DW.ref.__gxx_personality_v0
	.section	.data.rel.local.DW.ref.__gxx_personality_v0,"awG",@progbits,DW.ref.__gxx_personality_v0,comdat
	.align 8
	.type	DW.ref.__gxx_personality_v0, @object
	.size	DW.ref.__gxx_personality_v0, 8
DW.ref.__gxx_personality_v0:
	.quad	__gxx_personality_v0
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
