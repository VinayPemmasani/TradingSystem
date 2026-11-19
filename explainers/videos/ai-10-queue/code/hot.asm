
hot.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <ai_push(BlockingQueue<Tick>&, Tick const&)>:
   0:	endbr64
   4:	push   %r15
   6:	push   %r14
   8:	push   %r13
   a:	push   %r12
   c:	push   %rbp
   d:	mov    %rsi,%rbp
  10:	push   %rbx
  11:	mov    %rdi,%rbx
  14:	sub    $0x8,%rsp
  18:	call   1d <ai_push(BlockingQueue<Tick>&, Tick const&)+0x1d>
			19: R_X86_64_PLT32	pthread_mutex_lock-0x4
  1d:	test   %eax,%eax
  1f:	jne    2dc <ai_push(BlockingQueue<Tick>&, Tick const&)+0x2dc>
  25:	mov    0x98(%rbx),%rcx
  2c:	mov    0x88(%rbx),%rax
  33:	lea    -0x20(%rcx),%rdx
  37:	cmp    %rdx,%rax
  3a:	je     80 <ai_push(BlockingQueue<Tick>&, Tick const&)+0x80>
  3c:	movdqu 0x0(%rbp),%xmm1
  41:	add    $0x20,%rax
  45:	movups %xmm1,-0x20(%rax)
  49:	movdqu 0x10(%rbp),%xmm2
  4e:	movups %xmm2,-0x10(%rax)
  52:	mov    %rax,0x88(%rbx)
  59:	mov    %rbx,%rdi
  5c:	call   61 <ai_push(BlockingQueue<Tick>&, Tick const&)+0x61>
			5d: R_X86_64_PLT32	pthread_mutex_unlock-0x4
  61:	add    $0x8,%rsp
  65:	lea    0x28(%rbx),%rdi
  69:	pop    %rbx
  6a:	pop    %rbp
  6b:	pop    %r12
  6d:	pop    %r13
  6f:	pop    %r14
  71:	pop    %r15
  73:	jmp    78 <ai_push(BlockingQueue<Tick>&, Tick const&)+0x78>
			74: R_X86_64_PLT32	std::condition_variable::notify_one()-0x4
  78:	nopl   0x0(%rax,%rax,1)
  80:	mov    0xa0(%rbx),%r12
  87:	mov    0x80(%rbx),%rsi
  8e:	mov    %r12,%r13
  91:	sub    %rsi,%r13
  94:	mov    %r13,%rcx
  97:	sar    $0x3,%rcx
  9b:	cmp    $0x1,%r12
  9f:	mov    %rcx,%rdx
  a2:	adc    $0xffffffffffffffff,%rdx
  a6:	sub    0x90(%rbx),%rax
  ad:	shl    $0x4,%rdx
  b1:	sar    $0x5,%rax
  b5:	add    %rdx,%rax
  b8:	mov    0x78(%rbx),%rdx
  bc:	sub    0x68(%rbx),%rdx
  c0:	sar    $0x5,%rdx
  c4:	add    %rdx,%rax
  c7:	movabs $0x7ffffffffffffff,%rdx
  d1:	cmp    %rdx,%rax
  d4:	je     2e3 <ai_push(BlockingQueue<Tick>&, Tick const&)+0x2e3>
  da:	mov    0x58(%rbx),%rdi
  de:	mov    0x60(%rbx),%rdx
  e2:	mov    %r12,%rax
  e5:	sub    %rdi,%rax
  e8:	mov    %rdx,%r8
  eb:	sar    $0x3,%rax
  ef:	sub    %rax,%r8
  f2:	cmp    $0x1,%r8
  f6:	jbe    160 <ai_push(BlockingQueue<Tick>&, Tick const&)+0x160>
  f8:	mov    $0x200,%edi
  fd:	call   102 <ai_push(BlockingQueue<Tick>&, Tick const&)+0x102>
			fe: R_X86_64_PLT32	operator new(unsigned long)-0x4
 102:	mov    %rax,0x8(%r12)
 107:	movdqu 0x0(%rbp),%xmm3
 10c:	mov    0x88(%rbx),%rax
 113:	movups %xmm3,(%rax)
 116:	movdqu 0x10(%rbp),%xmm4
 11b:	movups %xmm4,0x10(%rax)
 11f:	mov    0xa0(%rbx),%rax
 126:	lea    0x8(%rax),%rdx
 12a:	mov    0x8(%rax),%rax
 12e:	mov    %rdx,0xa0(%rbx)
 135:	lea    0x200(%rax),%rdx
 13c:	movq   %rax,%xmm0
 141:	movq   %rdx,%xmm5
 146:	punpcklqdq %xmm5,%xmm0
 14a:	movups %xmm0,0x90(%rbx)
 151:	jmp    52 <ai_push(BlockingQueue<Tick>&, Tick const&)+0x52>
 156:	cs nopw 0x0(%rax,%rax,1)
 160:	lea    0x2(%rcx),%r14
 164:	lea    (%r14,%r14,1),%rax
 168:	cmp    %rdx,%rax
 16b:	jb     240 <ai_push(BlockingQueue<Tick>&, Tick const&)+0x240>
 171:	test   %rdx,%rdx
 174:	je     288 <ai_push(BlockingQueue<Tick>&, Tick const&)+0x288>
 17a:	lea    0x1(%rdx),%rdi
 17e:	lea    (%rdi,%rdi,1),%r12
 182:	mov    %r12,%rax
 185:	shr    $0x3c,%rax
 189:	jne    298 <ai_push(BlockingQueue<Tick>&, Tick const&)+0x298>
 18f:	shl    $0x4,%rdi
 193:	call   198 <ai_push(BlockingQueue<Tick>&, Tick const&)+0x198>
			194: R_X86_64_PLT32	operator new(unsigned long)-0x4
 198:	mov    %rax,%r15
 19b:	mov    %r12,%rax
 19e:	mov    0x80(%rbx),%rsi
 1a5:	sub    %r14,%rax
 1a8:	shr    $1,%rax
 1ab:	lea    (%r15,%rax,8),%r14
 1af:	mov    0xa0(%rbx),%rax
 1b6:	lea    0x8(%rax),%rdx
 1ba:	sub    %rsi,%rdx
 1bd:	cmp    $0x8,%rdx
 1c1:	jle    2a3 <ai_push(BlockingQueue<Tick>&, Tick const&)+0x2a3>
 1c7:	mov    %r14,%rdi
 1ca:	call   1cf <ai_push(BlockingQueue<Tick>&, Tick const&)+0x1cf>
			1cb: R_X86_64_PLT32	memmove-0x4
 1cf:	mov    0x60(%rbx),%rax
 1d3:	mov    0x58(%rbx),%rdi
 1d7:	lea    0x0(,%rax,8),%rsi
 1df:	call   1e4 <ai_push(BlockingQueue<Tick>&, Tick const&)+0x1e4>
			1e0: R_X86_64_PLT32	operator delete(void*, unsigned long)-0x4
 1e4:	mov    %r15,0x58(%rbx)
 1e8:	mov    %r12,0x60(%rbx)
 1ec:	mov    (%r14),%rax
 1ef:	lea    (%r14,%r13,1),%r12
 1f3:	mov    %r14,0x80(%rbx)
 1fa:	mov    %r12,0xa0(%rbx)
 201:	lea    0x200(%rax),%rdx
 208:	movq   %rax,%xmm0
 20d:	movq   %rdx,%xmm6
 212:	punpcklqdq %xmm6,%xmm0
 216:	movups %xmm0,0x70(%rbx)
 21a:	mov    (%r12),%rax
 21e:	lea    0x200(%rax),%rdx
 225:	movq   %rax,%xmm0
 22a:	movq   %rdx,%xmm7
 22f:	punpcklqdq %xmm7,%xmm0
 233:	movups %xmm0,0x90(%rbx)
 23a:	jmp    f8 <ai_push(BlockingQueue<Tick>&, Tick const&)+0xf8>
 23f:	nop
 240:	sub    %r14,%rdx
 243:	shr    $1,%rdx
 246:	lea    (%rdi,%rdx,8),%r14
 24a:	lea    0x8(%r12),%rdx
 24f:	sub    %rsi,%rdx
 252:	cmp    %rsi,%r14
 255:	jae    270 <ai_push(BlockingQueue<Tick>&, Tick const&)+0x270>
 257:	cmp    $0x8,%rdx
 25b:	jle    2b4 <ai_push(BlockingQueue<Tick>&, Tick const&)+0x2b4>
 25d:	mov    %r14,%rdi
 260:	call   265 <ai_push(BlockingQueue<Tick>&, Tick const&)+0x265>
			261: R_X86_64_PLT32	memmove-0x4
 265:	jmp    1ec <ai_push(BlockingQueue<Tick>&, Tick const&)+0x1ec>
 267:	nopw   0x0(%rax,%rax,1)
 270:	lea    0x8(%r14,%r13,1),%rdi
 275:	cmp    $0x8,%rdx
 279:	jle    2c5 <ai_push(BlockingQueue<Tick>&, Tick const&)+0x2c5>
 27b:	sub    %rdx,%rdi
 27e:	call   283 <ai_push(BlockingQueue<Tick>&, Tick const&)+0x283>
			27f: R_X86_64_PLT32	memmove-0x4
 283:	jmp    1ec <ai_push(BlockingQueue<Tick>&, Tick const&)+0x1ec>
 288:	mov    $0x18,%edi
 28d:	mov    $0x3,%r12d
 293:	jmp    193 <ai_push(BlockingQueue<Tick>&, Tick const&)+0x193>
 298:	shr    $0x3d,%r12
 29c:	je     2d7 <ai_push(BlockingQueue<Tick>&, Tick const&)+0x2d7>
 29e:	call   2a3 <ai_push(BlockingQueue<Tick>&, Tick const&)+0x2a3>
			29f: R_X86_64_PLT32	std::__throw_bad_array_new_length()-0x4
 2a3:	jne    1cf <ai_push(BlockingQueue<Tick>&, Tick const&)+0x1cf>
 2a9:	mov    (%rsi),%rax
 2ac:	mov    %rax,(%r14)
 2af:	jmp    1cf <ai_push(BlockingQueue<Tick>&, Tick const&)+0x1cf>
 2b4:	jne    1ec <ai_push(BlockingQueue<Tick>&, Tick const&)+0x1ec>
 2ba:	mov    (%rsi),%rax
 2bd:	mov    %rax,(%r14)
 2c0:	jmp    1ec <ai_push(BlockingQueue<Tick>&, Tick const&)+0x1ec>
 2c5:	jne    1ec <ai_push(BlockingQueue<Tick>&, Tick const&)+0x1ec>
 2cb:	mov    (%rsi),%rax
 2ce:	mov    %rax,-0x8(%rdi)
 2d2:	jmp    1ec <ai_push(BlockingQueue<Tick>&, Tick const&)+0x1ec>
 2d7:	call   2dc <ai_push(BlockingQueue<Tick>&, Tick const&)+0x2dc>
			2d8: R_X86_64_PLT32	std::__throw_bad_alloc()-0x4
 2dc:	mov    %eax,%edi
 2de:	call   2e3 <ai_push(BlockingQueue<Tick>&, Tick const&)+0x2e3>
			2df: R_X86_64_PLT32	std::__throw_system_error(int)-0x4
 2e3:	lea    0x0(%rip),%rdi        # 2ea <ai_push(BlockingQueue<Tick>&, Tick const&)+0x2ea>
			2e6: R_X86_64_PC32	.LC0-0x4
 2ea:	call   2ef <ai_push(BlockingQueue<Tick>&, Tick const&)+0x2ef>
			2eb: R_X86_64_PLT32	std::__throw_length_error(char const*)-0x4
 2ef:	endbr64
 2f3:	mov    %rax,%rbp
 2f6:	jmp    2fb <ai_push(BlockingQueue<Tick>&, Tick const&)+0x2fb>
			2f7: R_X86_64_PC32	.text.unlikely-0x4
 2fb:	nopl   0x0(%rax,%rax,1)

0000000000000300 <ai_pop(BlockingQueue<Tick>&)>:
 300:	endbr64
 304:	push   %r13
 306:	mov    %rdi,%r13
 309:	mov    %rsi,%rdi
 30c:	push   %r12
 30e:	push   %rbp
 30f:	push   %rbx
 310:	mov    %rsi,%rbx
 313:	sub    $0x28,%rsp
 317:	mov    %fs:0x28,%rax
 320:	mov    %rax,0x18(%rsp)
 325:	xor    %eax,%eax
 327:	mov    %rsi,(%rsp)
 32b:	movb   $0x0,0x8(%rsp)
 330:	call   335 <ai_pop(BlockingQueue<Tick>&)+0x35>
			331: R_X86_64_PLT32	pthread_mutex_lock-0x4
 335:	test   %eax,%eax
 337:	jne    412 <ai_pop(BlockingQueue<Tick>&)+0x112>
 33d:	movb   $0x1,0x8(%rsp)
 342:	lea    0x28(%rbx),%r12
 346:	mov    %rsp,%rbp
 349:	jmp    35b <ai_pop(BlockingQueue<Tick>&)+0x5b>
 34b:	nopl   0x0(%rax,%rax,1)
 350:	mov    %rbp,%rsi
 353:	mov    %r12,%rdi
 356:	call   35b <ai_pop(BlockingQueue<Tick>&)+0x5b>
			357: R_X86_64_PLT32	std::condition_variable::wait(std::unique_lock<std::mutex>&)-0x4
 35b:	mov    0x68(%rbx),%rax
 35f:	cmp    %rax,0x88(%rbx)
 366:	je     350 <ai_pop(BlockingQueue<Tick>&)+0x50>
 368:	mov    0x78(%rbx),%rcx
 36c:	movdqu (%rax),%xmm1
 370:	movdqu 0x10(%rax),%xmm2
 375:	lea    -0x20(%rcx),%rdx
 379:	movups %xmm1,0x0(%r13)
 37e:	movups %xmm2,0x10(%r13)
 383:	cmp    %rdx,%rax
 386:	je     3d0 <ai_pop(BlockingQueue<Tick>&)+0xd0>
 388:	add    $0x20,%rax
 38c:	cmpb   $0x0,0x8(%rsp)
 391:	mov    %rax,0x68(%rbx)
 395:	jne    3c0 <ai_pop(BlockingQueue<Tick>&)+0xc0>
 397:	mov    0x18(%rsp),%rax
 39c:	sub    %fs:0x28,%rax
 3a5:	jne    429 <ai_pop(BlockingQueue<Tick>&)+0x129>
 3ab:	add    $0x28,%rsp
 3af:	mov    %r13,%rax
 3b2:	pop    %rbx
 3b3:	pop    %rbp
 3b4:	pop    %r12
 3b6:	pop    %r13
 3b8:	ret
 3b9:	nopl   0x0(%rax)
 3c0:	mov    (%rsp),%rdi
 3c4:	test   %rdi,%rdi
 3c7:	je     397 <ai_pop(BlockingQueue<Tick>&)+0x97>
 3c9:	call   3ce <ai_pop(BlockingQueue<Tick>&)+0xce>
			3ca: R_X86_64_PLT32	pthread_mutex_unlock-0x4
 3ce:	jmp    397 <ai_pop(BlockingQueue<Tick>&)+0x97>
 3d0:	mov    0x70(%rbx),%rdi
 3d4:	mov    $0x200,%esi
 3d9:	call   3de <ai_pop(BlockingQueue<Tick>&)+0xde>
			3da: R_X86_64_PLT32	operator delete(void*, unsigned long)-0x4
 3de:	mov    0x80(%rbx),%rax
 3e5:	lea    0x8(%rax),%rdx
 3e9:	mov    0x8(%rax),%rax
 3ed:	mov    %rdx,0x80(%rbx)
 3f4:	lea    0x200(%rax),%rdx
 3fb:	movq   %rax,%xmm0
 400:	movq   %rdx,%xmm3
 405:	punpcklqdq %xmm3,%xmm0
 409:	movups %xmm0,0x70(%rbx)
 40d:	jmp    38c <ai_pop(BlockingQueue<Tick>&)+0x8c>
 412:	mov    0x18(%rsp),%rdx
 417:	sub    %fs:0x28,%rdx
 420:	jne    429 <ai_pop(BlockingQueue<Tick>&)+0x129>
 422:	mov    %eax,%edi
 424:	call   429 <ai_pop(BlockingQueue<Tick>&)+0x129>
			425: R_X86_64_PLT32	std::__throw_system_error(int)-0x4
 429:	call   42e <ai_pop(BlockingQueue<Tick>&)+0x12e>
			42a: R_X86_64_PLT32	__stack_chk_fail-0x4
 42e:	endbr64
 432:	mov    %rax,%rbx
 435:	jmp    43a <ai_pop(BlockingQueue<Tick>&)+0x13a>
			436: R_X86_64_PC32	.text.unlikely+0xc
 43a:	nopw   0x0(%rax,%rax,1)

0000000000000440 <f_push(SpscRing<Tick, 1024ul>&, Tick const&)>:
 440:	endbr64
 444:	mov    (%rdi),%rdx
 447:	mov    %rdx,%rax
 44a:	sub    0x8(%rdi),%rax
 44e:	cmp    $0x400,%rax
 454:	je     490 <f_push(SpscRing<Tick, 1024ul>&, Tick const&)+0x50>
 456:	mov    %rdx,%rax
 459:	movdqu (%rsi),%xmm0
 45d:	add    $0x1,%rdx
 461:	and    $0x3ff,%eax
 466:	add    $0x4,%rax
 46a:	shl    $0x5,%rax
 46e:	add    %rdi,%rax
 471:	movaps %xmm0,(%rax)
 474:	movdqu 0x10(%rsi),%xmm1
 479:	movaps %xmm1,0x10(%rax)
 47d:	mov    $0x1,%eax
 482:	mov    %rdx,(%rdi)
 485:	ret
 486:	cs nopw 0x0(%rax,%rax,1)
 490:	mov    0x40(%rdi),%rax
 494:	mov    %rdx,%rcx
 497:	sub    %rax,%rcx
 49a:	mov    %rax,0x8(%rdi)
 49e:	cmp    $0x400,%rcx
 4a5:	jne    456 <f_push(SpscRing<Tick, 1024ul>&, Tick const&)+0x16>
 4a7:	xor    %eax,%eax
 4a9:	ret
 4aa:	nopw   0x0(%rax,%rax,1)

00000000000004b0 <f_pop(SpscRing<Tick, 1024ul>&, Tick&)>:
 4b0:	endbr64
 4b4:	mov    0x40(%rdi),%rdx
 4b8:	cmp    0x48(%rdi),%rdx
 4bc:	je     4f0 <f_pop(SpscRing<Tick, 1024ul>&, Tick&)+0x40>
 4be:	mov    %rdx,%rax
 4c1:	add    $0x1,%rdx
 4c5:	and    $0x3ff,%eax
 4ca:	add    $0x4,%rax
 4ce:	shl    $0x5,%rax
 4d2:	add    %rdi,%rax
 4d5:	movdqa (%rax),%xmm0
 4d9:	movups %xmm0,(%rsi)
 4dc:	movdqa 0x10(%rax),%xmm1
 4e1:	mov    $0x1,%eax
 4e6:	movups %xmm1,0x10(%rsi)
 4ea:	mov    %rdx,0x40(%rdi)
 4ee:	ret
 4ef:	nop
 4f0:	mov    (%rdi),%rax
 4f3:	mov    %rax,0x48(%rdi)
 4f7:	cmp    %rax,%rdx
 4fa:	jne    4be <f_pop(SpscRing<Tick, 1024ul>&, Tick&)+0xe>
 4fc:	xor    %eax,%eax
 4fe:	ret

Disassembly of section .text.unlikely:

0000000000000000 <ai_push(BlockingQueue<Tick>&, Tick const&) [clone .cold]>:
   0:	mov    %rbx,%rdi
   3:	call   8 <ai_push(BlockingQueue<Tick>&, Tick const&) [clone .cold]+0x8>
			4: R_X86_64_PLT32	pthread_mutex_unlock-0x4
   8:	mov    %rbp,%rdi
   b:	call   10 <ai_pop(BlockingQueue<Tick>&) [clone .cold]>
			c: R_X86_64_PLT32	_Unwind_Resume-0x4

0000000000000010 <ai_pop(BlockingQueue<Tick>&) [clone .cold]>:
  10:	cmpb   $0x0,0x8(%rsp)
  15:	je     25 <ai_pop(BlockingQueue<Tick>&) [clone .cold]+0x15>
  17:	mov    (%rsp),%rdi
  1b:	test   %rdi,%rdi
  1e:	je     25 <ai_pop(BlockingQueue<Tick>&) [clone .cold]+0x15>
  20:	call   25 <ai_pop(BlockingQueue<Tick>&) [clone .cold]+0x15>
			21: R_X86_64_PLT32	pthread_mutex_unlock-0x4
  25:	mov    0x18(%rsp),%rax
  2a:	sub    %fs:0x28,%rax
  33:	jne    3d <ai_pop(BlockingQueue<Tick>&) [clone .cold]+0x2d>
  35:	mov    %rbx,%rdi
  38:	call   3d <ai_pop(BlockingQueue<Tick>&) [clone .cold]+0x2d>
			39: R_X86_64_PLT32	_Unwind_Resume-0x4
  3d:	call   42 <ai_pop(BlockingQueue<Tick>&) [clone .cold]+0x32>
			3e: R_X86_64_PLT32	__stack_chk_fail-0x4
