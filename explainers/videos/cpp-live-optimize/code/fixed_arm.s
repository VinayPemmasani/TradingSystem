	.text
	.file	"fixed_arm.cpp"
	.globl	_Z7publishRK3Msg                // -- Begin function _Z7publishRK3Msg
	.p2align	2
	.type	_Z7publishRK3Msg,@function
_Z7publishRK3Msg:                       // @_Z7publishRK3Msg
	.cfi_startproc
// %bb.0:
	ldp	q1, q0, [x0]
	adrp	x8, slot
	add	x8, x8, :lo12:slot
	mov	w9, #1                          // =0x1
	stp	q1, q0, [x8]
	adrp	x8, ready
	add	x8, x8, :lo12:ready
	stlrb	w9, [x8]
	ret
.Lfunc_end0:
	.size	_Z7publishRK3Msg, .Lfunc_end0-_Z7publishRK3Msg
	.cfi_endproc
                                        // -- End function
	.globl	_Z7consumev                     // -- Begin function _Z7consumev
	.p2align	2
	.type	_Z7consumev,@function
_Z7consumev:                            // @_Z7consumev
	.cfi_startproc
// %bb.0:
	adrp	x8, ready
	add	x8, x8, :lo12:ready
.LBB1_1:                                // =>This Inner Loop Header: Depth=1
	ldarb	w9, [x8]
	tbz	w9, #0, .LBB1_1
// %bb.2:
	adrp	x8, ready
	strb	wzr, [x8, :lo12:ready]
	adrp	x8, slot+8
	ldr	x0, [x8, :lo12:slot+8]
	ret
.Lfunc_end1:
	.size	_Z7consumev, .Lfunc_end1-_Z7consumev
	.cfi_endproc
                                        // -- End function
	.type	slot,@object                    // @slot
	.bss
	.globl	slot
	.p2align	3, 0x0
slot:
	.zero	32
	.size	slot, 32

	.type	ready,@object                   // @ready
	.globl	ready
	.p2align	2, 0x0
ready:
	.byte	0                               // 0x0
	.size	ready, 1

	.section	".linker-options","e",@llvm_linker_options
	.ident	"Ubuntu clang version 18.1.3 (1ubuntu1)"
	.section	".note.GNU-stack","",@progbits
	.addrsig
