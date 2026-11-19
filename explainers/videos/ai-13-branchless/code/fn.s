
fn.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <scan(std::vector<Tick, std::allocator<Tick> > const&, int)>:
   0:	endbr64
   4:	push   %r14
   6:	pxor   %xmm0,%xmm0
   a:	push   %r13
   c:	push   %r12
   e:	push   %rbp
   f:	mov    %rdi,%rbp
  12:	push   %rbx
  13:	mov    (%rsi),%rbx
  16:	mov    0x8(%rsi),%r12
  1a:	movq   $0x0,0x20(%rdi)
  22:	movups %xmm0,(%rdi)
  25:	movups %xmm0,0x10(%rdi)
  29:	cmp    %rbx,%r12
  2c:	je     7e <scan(std::vector<Tick, std::allocator<Tick> > const&, int)+0x7e>
  2e:	mov    %edx,%r14d
  31:	lea    0x0(%rip),%r13        # 38 <scan(std::vector<Tick, std::allocator<Tick> > const&, int)+0x38>
  38:	jmp    57 <scan(std::vector<Tick, std::allocator<Tick> > const&, int)+0x57>
  3a:	nopw   0x0(%rax,%rax,1)
  40:	add    %rax,0x0(%rbp)
  44:	cmp    %r14d,%ecx
  47:	jl     4e <scan(std::vector<Tick, std::allocator<Tick> > const&, int)+0x4e>
  49:	addq   $0x1,0x10(%rbp)
  4e:	add    $0x10,%rbx
  52:	cmp    %rbx,%r12
  55:	je     7e <scan(std::vector<Tick, std::allocator<Tick> > const&, int)+0x7e>
  57:	mov    0x8(%rbx),%ecx
  5a:	test   %ecx,%ecx
  5c:	jle    90 <scan(std::vector<Tick, std::allocator<Tick> > const&, int)+0x90>
  5e:	cmpb   $0x0,0xc(%rbx)
  62:	movslq %ecx,%rax
  65:	je     40 <scan(std::vector<Tick, std::allocator<Tick> > const&, int)+0x40>
  67:	add    %rax,0x8(%rbp)
  6b:	cmp    %r14d,%ecx
  6e:	jl     4e <scan(std::vector<Tick, std::allocator<Tick> > const&, int)+0x4e>
  70:	add    $0x10,%rbx
  74:	addq   $0x1,0x18(%rbp)
  79:	cmp    %rbx,%r12
  7c:	jne    57 <scan(std::vector<Tick, std::allocator<Tick> > const&, int)+0x57>
  7e:	pop    %rbx
  7f:	mov    %rbp,%rax
  82:	pop    %rbp
  83:	pop    %r12
  85:	pop    %r13
  87:	pop    %r14
  89:	ret
  8a:	nopw   0x0(%rax,%rax,1)
  90:	mov    0x0(%rip),%rdi        # 97 <scan(std::vector<Tick, std::allocator<Tick> > const&, int)+0x97>
  97:	mov    %r13,%rdx
  9a:	mov    $0x2,%esi
  9f:	xor    %eax,%eax
  a1:	call   a6 <scan(std::vector<Tick, std::allocator<Tick> > const&, int)+0xa6>
  a6:	addq   $0x1,0x20(%rbp)
  ab:	jmp    4e <scan(std::vector<Tick, std::allocator<Tick> > const&, int)+0x4e>
  ad:	nopl   (%rax)

00000000000000b0 <f_general(std::vector<Tick, std::allocator<Tick> > const&, int)>:
  b0:	endbr64
  b4:	push   %rbx
  b5:	mov    %rdi,%rbx
  b8:	sub    $0x10,%rsp
  bc:	mov    %fs:0x28,%rax
  c5:	mov    %rax,0x8(%rsp)
  ca:	xor    %eax,%eax
  cc:	call   d1 <f_general(std::vector<Tick, std::allocator<Tick> > const&, int)+0x21>
  d1:	mov    0x8(%rsp),%rax
  d6:	sub    %fs:0x28,%rax
  df:	jne    ea <f_general(std::vector<Tick, std::allocator<Tick> > const&, int)+0x3a>
  e1:	add    $0x10,%rsp
  e5:	mov    %rbx,%rax
  e8:	pop    %rbx
  e9:	ret
  ea:	call   ef <f_general(std::vector<Tick, std::allocator<Tick> > const&, int)+0x3f>
  ef:	nop

00000000000000f0 <f_hot(Tick const*, unsigned long, long)>:
  f0:	endbr64
  f4:	push   %r15
  f6:	mov    %rdi,%r8
  f9:	push   %r14
  fb:	push   %r13
  fd:	push   %r12
  ff:	push   %rbp
 100:	push   %rbx
 101:	sub    $0x28,%rsp
 105:	test   %rdx,%rdx
 108:	je     198 <f_hot(Tick const*, unsigned long, long)+0xa8>
 10e:	lea    0x8(%rsi),%rbx
 112:	mov    %rdx,%r9
 115:	xor    %r14d,%r14d
 118:	xor    %r12d,%r12d
 11b:	xor    %r15d,%r15d
 11e:	xor    %r13d,%r13d
 121:	xor    %esi,%esi
 123:	xor    %ebp,%ebp
 125:	nopl   (%rax)
 128:	movslq (%rbx),%rdx
 12b:	mov    %rdx,%rdi
 12e:	test   %rdx,%rdx
 131:	jle    137 <f_hot(Tick const*, unsigned long, long)+0x47>
 137:	movzbl 0x4(%rbx),%eax
 13b:	xor    %edi,%edi
 13d:	neg    %rax
 140:	cmp    %rdx,%rcx
 143:	setle  %dil
 147:	add    %rdx,%r13
 14a:	and    %rax,%rdx
 14d:	and    %rdi,%rax
 150:	add    %rdx,%r15
 153:	add    %rdi,%r12
 156:	add    %rax,%r14
 159:	add    $0x1,%rbp
 15d:	add    $0x10,%rbx
 161:	cmp    %rbp,%r9
 164:	jne    128 <f_hot(Tick const*, unsigned long, long)+0x38>
 166:	sub    %r15,%r13
 169:	sub    %r14,%r12
 16c:	mov    %r13,(%r8)
 16f:	mov    %r8,%rax
 172:	mov    %r15,0x8(%r8)
 176:	mov    %r12,0x10(%r8)
 17a:	mov    %r14,0x18(%r8)
 17e:	mov    %rsi,0x20(%r8)
 182:	add    $0x28,%rsp
 186:	pop    %rbx
 187:	pop    %rbp
 188:	pop    %r12
 18a:	pop    %r13
 18c:	pop    %r14
 18e:	pop    %r15
 190:	ret
 191:	nopl   0x0(%rax)
 198:	xor    %r12d,%r12d
 19b:	xor    %r13d,%r13d
 19e:	xor    %r14d,%r14d
 1a1:	xor    %r15d,%r15d
 1a4:	xor    %esi,%esi
 1a6:	jmp    16c <f_hot(Tick const*, unsigned long, long)+0x7c>

Disassembly of section .text.unlikely:

0000000000000000 <hot::on_bad(Tick const&) [clone .isra.0]>:
   0:	mov    %edi,%ecx
   2:	mov    0x0(%rip),%rdi        # 9 <hot::on_bad(Tick const&) [clone .isra.0]+0x9>
   9:	mov    $0x2,%esi
   e:	xor    %eax,%eax
  10:	lea    0x0(%rip),%rdx        # 17 <hot::on_bad(Tick const&) [clone .isra.0]+0x17>
  17:	jmp    1c <f_hot(Tick const*, unsigned long, long) [clone .cold]>

000000000000001c <f_hot(Tick const*, unsigned long, long) [clone .cold]>:
  1c:	mov    %rcx,0x18(%rsp)
  21:	mov    %r9,0x10(%rsp)
  26:	mov    %r8,0x8(%rsp)
  2b:	mov    %rsi,(%rsp)
  2f:	call   0 <hot::on_bad(Tick const&) [clone .isra.0]>
  34:	mov    (%rsp),%rsi
  38:	mov    0x8(%rsp),%r8
  3d:	mov    0x10(%rsp),%r9
  42:	mov    0x18(%rsp),%rcx
  47:	add    $0x1,%rsi
  4b:	jmp    50 <f_hot(Tick const*, unsigned long, long) [clone .cold]+0x34>
