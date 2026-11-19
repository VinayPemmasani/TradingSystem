	.file	"broken.cpp"
	.text
	.p2align 4
	.globl	_Z7publishRK3Msg
	.type	_Z7publishRK3Msg, @function
_Z7publishRK3Msg:
.LFB12738:
	.cfi_startproc
	endbr64
	movdqu	(%rdi), %xmm0
	movb	$1, ready(%rip)
	movaps	%xmm0, slot(%rip)
	movdqu	16(%rdi), %xmm1
	movaps	%xmm1, 16+slot(%rip)
	ret
	.cfi_endproc
.LFE12738:
	.size	_Z7publishRK3Msg, .-_Z7publishRK3Msg
	.p2align 4
	.globl	_Z7consumev
	.type	_Z7consumev, @function
_Z7consumev:
.LFB12739:
	.cfi_startproc
	endbr64
	movb	$0, ready(%rip)
	movq	8+slot(%rip), %rax
	ret
	.cfi_endproc
.LFE12739:
	.size	_Z7consumev, .-_Z7consumev
	.globl	ready
	.bss
	.type	ready, @object
	.size	ready, 1
ready:
	.zero	1
	.globl	slot
	.align 32
	.type	slot, @object
	.size	slot, 32
slot:
	.zero	32
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
