	.text
	.file	"arm.c"
	.globl	st_seq                          // -- Begin function st_seq
	.p2align	2
	.type	st_seq,@function
st_seq:                                 // @st_seq
	.cfi_startproc
// %bb.0:
	adrp	x8, head
	add	x8, x8, :lo12:head
	stlr	x0, [x8]
	ret
.Lfunc_end0:
	.size	st_seq, .Lfunc_end0-st_seq
	.cfi_endproc
                                        // -- End function
	.globl	st_rel                          // -- Begin function st_rel
	.p2align	2
	.type	st_rel,@function
st_rel:                                 // @st_rel
	.cfi_startproc
// %bb.0:
	adrp	x8, head
	add	x8, x8, :lo12:head
	stlr	x0, [x8]
	ret
.Lfunc_end1:
	.size	st_rel, .Lfunc_end1-st_rel
	.cfi_endproc
                                        // -- End function
	.globl	st_rlx                          // -- Begin function st_rlx
	.p2align	2
	.type	st_rlx,@function
st_rlx:                                 // @st_rlx
	.cfi_startproc
// %bb.0:
	adrp	x8, head
	str	x0, [x8, :lo12:head]
	ret
.Lfunc_end2:
	.size	st_rlx, .Lfunc_end2-st_rlx
	.cfi_endproc
                                        // -- End function
	.globl	ld_seq                          // -- Begin function ld_seq
	.p2align	2
	.type	ld_seq,@function
ld_seq:                                 // @ld_seq
	.cfi_startproc
// %bb.0:
	adrp	x8, head
	add	x8, x8, :lo12:head
	ldar	x0, [x8]
	ret
.Lfunc_end3:
	.size	ld_seq, .Lfunc_end3-ld_seq
	.cfi_endproc
                                        // -- End function
	.globl	ld_acq                          // -- Begin function ld_acq
	.p2align	2
	.type	ld_acq,@function
ld_acq:                                 // @ld_acq
	.cfi_startproc
// %bb.0:
	adrp	x8, head
	add	x8, x8, :lo12:head
	ldar	x0, [x8]
	ret
.Lfunc_end4:
	.size	ld_acq, .Lfunc_end4-ld_acq
	.cfi_endproc
                                        // -- End function
	.globl	ld_rlx                          // -- Begin function ld_rlx
	.p2align	2
	.type	ld_rlx,@function
ld_rlx:                                 // @ld_rlx
	.cfi_startproc
// %bb.0:
	adrp	x8, head
	ldr	x0, [x8, :lo12:head]
	ret
.Lfunc_end5:
	.size	ld_rlx, .Lfunc_end5-ld_rlx
	.cfi_endproc
                                        // -- End function
	.type	head,@object                    // @head
	.bss
	.globl	head
	.p2align	3, 0x0
head:
	.xword	0                               // 0x0
	.size	head, 8

	.ident	"Ubuntu clang version 18.1.3 (1ubuntu1)"
	.section	".note.GNU-stack","",@progbits
	.addrsig
