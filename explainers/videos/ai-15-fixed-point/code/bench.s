
bench:     file format elf64-x86-64


Disassembly of section .init:

0000000000001000 <_init>:
    1000:	endbr64
    1004:	sub    $0x8,%rsp
    1008:	mov    0x3fe1(%rip),%rax        # 4ff0 <__gmon_start__@Base>
    100f:	test   %rax,%rax
    1012:	je     1016 <_init+0x16>
    1014:	call   *%rax
    1016:	add    $0x8,%rsp
    101a:	ret

Disassembly of section .plt:

0000000000001020 <.plt>:
    1020:	push   0x3f2a(%rip)        # 4f50 <_GLOBAL_OFFSET_TABLE_+0x8>
    1026:	jmp    *0x3f2c(%rip)        # 4f58 <_GLOBAL_OFFSET_TABLE_+0x10>
    102c:	nopl   0x0(%rax)
    1030:	endbr64
    1034:	push   $0x0
    1039:	jmp    1020 <_init+0x20>
    103e:	xchg   %ax,%ax
    1040:	endbr64
    1044:	push   $0x1
    1049:	jmp    1020 <_init+0x20>
    104e:	xchg   %ax,%ax
    1050:	endbr64
    1054:	push   $0x2
    1059:	jmp    1020 <_init+0x20>
    105e:	xchg   %ax,%ax
    1060:	endbr64
    1064:	push   $0x3
    1069:	jmp    1020 <_init+0x20>
    106e:	xchg   %ax,%ax
    1070:	endbr64
    1074:	push   $0x4
    1079:	jmp    1020 <_init+0x20>
    107e:	xchg   %ax,%ax
    1080:	endbr64
    1084:	push   $0x5
    1089:	jmp    1020 <_init+0x20>
    108e:	xchg   %ax,%ax
    1090:	endbr64
    1094:	push   $0x6
    1099:	jmp    1020 <_init+0x20>
    109e:	xchg   %ax,%ax
    10a0:	endbr64
    10a4:	push   $0x7
    10a9:	jmp    1020 <_init+0x20>
    10ae:	xchg   %ax,%ax
    10b0:	endbr64
    10b4:	push   $0x8
    10b9:	jmp    1020 <_init+0x20>
    10be:	xchg   %ax,%ax
    10c0:	endbr64
    10c4:	push   $0x9
    10c9:	jmp    1020 <_init+0x20>
    10ce:	xchg   %ax,%ax
    10d0:	endbr64
    10d4:	push   $0xa
    10d9:	jmp    1020 <_init+0x20>
    10de:	xchg   %ax,%ax
    10e0:	endbr64
    10e4:	push   $0xb
    10e9:	jmp    1020 <_init+0x20>
    10ee:	xchg   %ax,%ax
    10f0:	endbr64
    10f4:	push   $0xc
    10f9:	jmp    1020 <_init+0x20>
    10fe:	xchg   %ax,%ax
    1100:	endbr64
    1104:	push   $0xd
    1109:	jmp    1020 <_init+0x20>
    110e:	xchg   %ax,%ax

Disassembly of section .plt.got:

0000000000001110 <__cxa_finalize@plt>:
    1110:	endbr64
    1114:	jmp    *0x3eb6(%rip)        # 4fd0 <__cxa_finalize@GLIBC_2.2.5>
    111a:	nopw   0x0(%rax,%rax,1)

Disassembly of section .plt.sec:

0000000000001120 <__printf_chk@plt>:
    1120:	endbr64
    1124:	jmp    *0x3e36(%rip)        # 4f60 <__printf_chk@GLIBC_2.3.4>
    112a:	nopw   0x0(%rax,%rax,1)

0000000000001130 <round@plt>:
    1130:	endbr64
    1134:	jmp    *0x3e2e(%rip)        # 4f68 <round@GLIBC_2.2.5>
    113a:	nopw   0x0(%rax,%rax,1)

0000000000001140 <__cxa_allocate_exception@plt>:
    1140:	endbr64
    1144:	jmp    *0x3e26(%rip)        # 4f70 <__cxa_allocate_exception@CXXABI_1.3>
    114a:	nopw   0x0(%rax,%rax,1)

0000000000001150 <std::__throw_length_error(char const*)@plt>:
    1150:	endbr64
    1154:	jmp    *0x3e1e(%rip)        # 4f78 <std::__throw_length_error(char const*)@GLIBCXX_3.4>
    115a:	nopw   0x0(%rax,%rax,1)

0000000000001160 <memset@plt>:
    1160:	endbr64
    1164:	jmp    *0x3e16(%rip)        # 4f80 <memset@GLIBC_2.2.5>
    116a:	nopw   0x0(%rax,%rax,1)

0000000000001170 <__cxa_free_exception@plt>:
    1170:	endbr64
    1174:	jmp    *0x3e0e(%rip)        # 4f88 <__cxa_free_exception@CXXABI_1.3>
    117a:	nopw   0x0(%rax,%rax,1)

0000000000001180 <operator new(unsigned long)@plt>:
    1180:	endbr64
    1184:	jmp    *0x3e06(%rip)        # 4f90 <operator new(unsigned long)@GLIBCXX_3.4>
    118a:	nopw   0x0(%rax,%rax,1)

0000000000001190 <operator delete(void*, unsigned long)@plt>:
    1190:	endbr64
    1194:	jmp    *0x3dfe(%rip)        # 4f98 <operator delete(void*, unsigned long)@CXXABI_1.3.9>
    119a:	nopw   0x0(%rax,%rax,1)

00000000000011a0 <__stack_chk_fail@plt>:
    11a0:	endbr64
    11a4:	jmp    *0x3df6(%rip)        # 4fa0 <__stack_chk_fail@GLIBC_2.4>
    11aa:	nopw   0x0(%rax,%rax,1)

00000000000011b0 <std::chrono::_V2::steady_clock::now()@plt>:
    11b0:	endbr64
    11b4:	jmp    *0x3dee(%rip)        # 4fa8 <std::chrono::_V2::steady_clock::now()@GLIBCXX_3.4.19>
    11ba:	nopw   0x0(%rax,%rax,1)

00000000000011c0 <memmove@plt>:
    11c0:	endbr64
    11c4:	jmp    *0x3de6(%rip)        # 4fb0 <memmove@GLIBC_2.2.5>
    11ca:	nopw   0x0(%rax,%rax,1)

00000000000011d0 <__cxa_throw@plt>:
    11d0:	endbr64
    11d4:	jmp    *0x3dde(%rip)        # 4fb8 <__cxa_throw@CXXABI_1.3>
    11da:	nopw   0x0(%rax,%rax,1)

00000000000011e0 <_Unwind_Resume@plt>:
    11e0:	endbr64
    11e4:	jmp    *0x3dd6(%rip)        # 4fc0 <_Unwind_Resume@GCC_3.0>
    11ea:	nopw   0x0(%rax,%rax,1)

00000000000011f0 <std::invalid_argument::invalid_argument(char const*)@plt>:
    11f0:	endbr64
    11f4:	jmp    *0x3dce(%rip)        # 4fc8 <std::invalid_argument::invalid_argument(char const*)@GLIBCXX_3.4.21>
    11fa:	nopw   0x0(%rax,%rax,1)

Disassembly of section .text:

0000000000001200 <apply(Levels&, double, double) [clone .cold]>:
    1200:	mov    $0x10,%edi
    1205:	call   1140 <__cxa_allocate_exception@plt>
    120a:	lea    0x1f3b(%rip),%rsi        # 314c <_IO_stdin_used+0x14c>
    1211:	mov    %rax,%rdi
    1214:	mov    %rax,%rbx
    1217:	call   11f0 <std::invalid_argument::invalid_argument(char const*)@plt>
    121c:	mov    0x3dbd(%rip),%rdx        # 4fe0 <std::invalid_argument::~invalid_argument()@GLIBCXX_3.4>
    1223:	lea    0x3ae6(%rip),%rsi        # 4d10 <typeinfo for std::invalid_argument@GLIBCXX_3.4>
    122a:	mov    %rbx,%rdi
    122d:	call   11d0 <__cxa_throw@plt>
    1232:	endbr64
    1236:	mov    %rax,%rbp
    1239:	mov    %rbx,%rdi
    123c:	call   1170 <__cxa_free_exception@plt>
    1241:	mov    %rbp,%rdi
    1244:	call   11e0 <_Unwind_Resume@plt>

0000000000001249 <k_dbl(Levels&, double const*, double const*, unsigned long) [clone .cold]>:
    1249:	mov    $0x10,%edi
    124e:	call   1140 <__cxa_allocate_exception@plt>
    1253:	lea    0x1ef2(%rip),%rsi        # 314c <_IO_stdin_used+0x14c>
    125a:	mov    %rax,%rdi
    125d:	mov    %rax,%rbx
    1260:	call   11f0 <std::invalid_argument::invalid_argument(char const*)@plt>
    1265:	mov    0x3d74(%rip),%rdx        # 4fe0 <std::invalid_argument::~invalid_argument()@GLIBCXX_3.4>
    126c:	lea    0x3a9d(%rip),%rsi        # 4d10 <typeinfo for std::invalid_argument@GLIBCXX_3.4>
    1273:	mov    %rbx,%rdi
    1276:	call   11d0 <__cxa_throw@plt>
    127b:	endbr64
    127f:	mov    %rax,%rbp
    1282:	mov    %rbx,%rdi
    1285:	call   1170 <__cxa_free_exception@plt>
    128a:	mov    %rbp,%rdi
    128d:	call   11e0 <_Unwind_Resume@plt>

0000000000001292 <main.cold>:
    1292:	mov    0x60(%rsp),%rdi
    1297:	call   2a10 <std::vector<double, std::allocator<double> >::~vector()>
    129c:	lea    0x140(%rsp),%rdi
    12a4:	call   2a10 <std::vector<double, std::allocator<double> >::~vector()>
    12a9:	lea    0x120(%rsp),%rdi
    12b1:	call   2a10 <std::vector<double, std::allocator<double> >::~vector()>
    12b6:	lea    0x100(%rsp),%rdi
    12be:	call   2a10 <std::vector<double, std::allocator<double> >::~vector()>
    12c3:	lea    0x198(%rsp),%rdi
    12cb:	call   2a40 <std::vector<long, std::allocator<long> >::~vector()>
    12d0:	mov    0x58(%rsp),%rdi
    12d5:	call   2a10 <std::vector<double, std::allocator<double> >::~vector()>
    12da:	lea    0xe0(%rsp),%rdi
    12e2:	call   2a40 <std::vector<long, std::allocator<long> >::~vector()>
    12e7:	lea    0xc0(%rsp),%rdi
    12ef:	call   2a40 <std::vector<long, std::allocator<long> >::~vector()>
    12f4:	mov    0x50(%rsp),%rdi
    12f9:	call   2a10 <std::vector<double, std::allocator<double> >::~vector()>
    12fe:	mov    0x48(%rsp),%rdi
    1303:	call   2a10 <std::vector<double, std::allocator<double> >::~vector()>
    1308:	mov    0xbb8(%rsp),%rax
    1310:	sub    %fs:0x28,%rax
    1319:	jne    1323 <main.cold+0x91>
    131b:	mov    %rbx,%rdi
    131e:	call   11e0 <_Unwind_Resume@plt>
    1323:	call   11a0 <__stack_chk_fail@plt>
    1328:	nopl   0x0(%rax,%rax,1)

0000000000001330 <main>:
    1330:	endbr64
    1334:	push   %r15
    1336:	mov    $0x1,%ecx
    133b:	movabs $0x5851f42d4c957f2d,%rsi
    1345:	push   %r14
    1347:	push   %r13
    1349:	push   %r12
    134b:	push   %rbp
    134c:	push   %rbx
    134d:	sub    $0xbc8,%rsp
    1354:	mov    %fs:0x28,%rax
    135d:	mov    %rax,0xbb8(%rsp)
    1365:	xor    %eax,%eax
    1367:	mov    $0xb,%eax
    136c:	lea    0x1f0(%rsp),%r12
    1374:	movq   $0xb,0x1f0(%rsp)
    1380:	mov    %rax,%rdx
    1383:	nopl   0x0(%rax,%rax,1)
    1388:	mov    %rdx,%rax
    138b:	shr    $0x3e,%rax
    138f:	xor    %rdx,%rax
    1392:	imul   %rsi,%rax
    1396:	lea    (%rax,%rcx,1),%rdx
    139a:	mov    %rdx,(%r12,%rcx,8)
    139e:	add    $0x1,%rcx
    13a2:	cmp    $0x138,%rcx
    13a9:	jne    1388 <main+0x58>
    13ab:	lea    0x80(%rsp),%rdi
    13b3:	mov    $0x2000,%esi
    13b8:	movq   $0x138,0xbb0(%rsp)
    13c4:	mov    %rdi,0x48(%rsp)
    13c9:	call   20c0 <std::vector<double, std::allocator<double> >::vector(unsigned long, std::allocator<double> const&) [clone .isra.0]>
    13ce:	lea    0xa0(%rsp),%rax
    13d6:	mov    $0x2000,%esi
    13db:	mov    %rax,%rdi
    13de:	mov    %rax,0x50(%rsp)
    13e3:	call   20c0 <std::vector<double, std::allocator<double> >::vector(unsigned long, std::allocator<double> const&) [clone .isra.0]>
    13e8:	pxor   %xmm0,%xmm0
    13ec:	mov    $0x10000,%edi
    13f1:	movups %xmm0,0xc8(%rsp)
    13f9:	call   1180 <operator new(unsigned long)@plt>
    13fe:	lea    0x8(%rax),%rdi
    1402:	mov    $0xfff8,%edx
    1407:	xor    %esi,%esi
    1409:	mov    %rax,0x8(%rsp)
    140e:	movq   $0x0,(%rax)
    1415:	lea    0x10000(%rax),%rbx
    141c:	mov    %rax,0xc0(%rsp)
    1424:	mov    %rbx,0xd0(%rsp)
    142c:	call   1160 <memset@plt>
    1431:	pxor   %xmm0,%xmm0
    1435:	mov    $0x10000,%edi
    143a:	mov    %rbx,0xc8(%rsp)
    1442:	movups %xmm0,0xe8(%rsp)
    144a:	call   1180 <operator new(unsigned long)@plt>
    144f:	movq   $0x0,(%rax)
    1456:	lea    0x8(%rax),%rdi
    145a:	xor    %esi,%esi
    145c:	xor    %r13d,%r13d
    145f:	lea    0x10000(%rax),%rbx
    1466:	mov    $0xfff8,%edx
    146b:	mov    %rax,0x10(%rsp)
    1470:	movabs $0x20c49ba5e353f7d,%r14
    147a:	mov    %rbx,0xf0(%rsp)
    1482:	mov    %rax,0xe0(%rsp)
    148a:	call   1160 <memset@plt>
    148f:	mov    %rbx,0xe8(%rsp)
    1497:	mov    0xa0(%rsp),%rbp
    149f:	mov    0x80(%rsp),%rbx
    14a7:	nopw   0x0(%rax,%rax,1)
    14b0:	mov    %r12,%rdi
    14b3:	call   2bb0 <std::mersenne_twister_engine<unsigned long, 64ul, 312ul, 156ul, 31ul, 13043109905998158313ul, 29ul, 6148914691236517205ul, 17ul, 8202884508482404352ul, 37ul, 18444473444759240704ul, 43ul, 6364136223846793005ul>::operator()()>
    14b8:	mov    %r12,%rdi
    14bb:	mov    %rax,%rdx
    14be:	mov    %rax,%rsi
    14c1:	shr    $0x4,%rdx
    14c5:	mov    %rdx,%rax
    14c8:	mul    %r14
    14cb:	imul   $0x7d0,%rdx,%rdx
    14d2:	sub    %rdx,%rsi
    14d5:	lea    0x7a120(%rsi),%r15
    14dc:	call   2bb0 <std::mersenne_twister_engine<unsigned long, 64ul, 312ul, 156ul, 31ul, 13043109905998158313ul, 29ul, 6148914691236517205ul, 17ul, 8202884508482404352ul, 37ul, 18444473444759240704ul, 43ul, 6364136223846793005ul>::operator()()>
    14e1:	pxor   %xmm0,%xmm0
    14e5:	mov    %rax,%rdx
    14e8:	cvtsi2sd %r15,%xmm0
    14ed:	mov    %rax,%rcx
    14f0:	movabs $0x28f5c28f5c28f5c3,%rax
    14fa:	shr    $0x2,%rdx
    14fe:	divsd  0x1c9a(%rip),%xmm0        # 31a0 <_IO_stdin_used+0x1a0>
    1506:	mul    %rdx
    1509:	mov    %rdx,%rax
    150c:	and    $0xfffffffffffffffc,%rdx
    1510:	shr    $0x2,%rax
    1514:	add    %rax,%rdx
    1517:	lea    (%rdx,%rdx,4),%rax
    151b:	shl    $0x2,%rax
    151f:	sub    %rax,%rcx
    1522:	mov    0x8(%rsp),%rax
    1527:	add    $0x1,%rcx
    152b:	mov    %r15,(%rax,%r13,8)
    152f:	mov    0x10(%rsp),%rax
    1534:	mov    %rcx,(%rax,%r13,8)
    1538:	movsd  %xmm0,(%rbx,%r13,8)
    153e:	pxor   %xmm0,%xmm0
    1542:	cvtsi2sd %rcx,%xmm0
    1547:	movsd  %xmm0,0x0(%rbp,%r13,8)
    154e:	add    $0x1,%r13
    1552:	cmp    $0x2000,%r13
    1559:	jne    14b0 <main+0x180>
    155f:	mov    0x1c42(%rip),%rax        # 31a8 <_IO_stdin_used+0x1a8>
    1566:	pxor   %xmm0,%xmm0
    156a:	mov    $0x7d1,%esi
    156f:	movups %xmm0,0x168(%rsp)
    1577:	mov    %rax,0x160(%rsp)
    157f:	lea    0x168(%rsp),%rax
    1587:	mov    %rax,%rdi
    158a:	mov    %rax,0x58(%rsp)
    158f:	movups %xmm0,0x178(%rsp)
    1597:	call   20c0 <std::vector<double, std::allocator<double> >::vector(unsigned long, std::allocator<double> const&) [clone .isra.0]>
    159c:	pxor   %xmm0,%xmm0
    15a0:	mov    $0x3e88,%edi
    15a5:	movq   $0x0,0x1b0(%rsp)
    15b1:	movq   $0x7a120,0x190(%rsp)
    15bd:	movaps %xmm0,0x1a0(%rsp)
    15c5:	call   1180 <operator new(unsigned long)@plt>
    15ca:	lea    0x8(%rax),%rdi
    15ce:	xor    %esi,%esi
    15d0:	mov    $0x3e80,%edx
    15d5:	mov    %rax,0x68(%rsp)
    15da:	movq   $0x0,(%rax)
    15e1:	lea    0x3e88(%rax),%r12
    15e8:	mov    %rax,0x198(%rsp)
    15f0:	mov    %r12,0x1a8(%rsp)
    15f8:	call   1160 <memset@plt>
    15fd:	mov    0x1ba4(%rip),%rax        # 31a8 <_IO_stdin_used+0x1a8>
    1604:	pxor   %xmm0,%xmm0
    1608:	mov    $0x7d1,%esi
    160d:	mov    %r12,0x1a0(%rsp)
    1615:	mov    %rax,0x1c0(%rsp)
    161d:	lea    0x1c8(%rsp),%rax
    1625:	mov    %rax,%rdi
    1628:	movq   $0x0,0x110(%rsp)
    1634:	movq   $0x0,0x130(%rsp)
    1640:	movq   $0x0,0x150(%rsp)
    164c:	mov    %rax,0x60(%rsp)
    1651:	movaps %xmm0,0x100(%rsp)
    1659:	movaps %xmm0,0x120(%rsp)
    1661:	movaps %xmm0,0x140(%rsp)
    1669:	movups %xmm0,0x1c8(%rsp)
    1671:	movups %xmm0,0x1d8(%rsp)
    1679:	call   20c0 <std::vector<double, std::allocator<double> >::vector(unsigned long, std::allocator<double> const&) [clone .isra.0]>
    167e:	lea    0x1c0(%rsp),%rax
    1686:	mov    $0x29,%r13d
    168c:	xor    %r14d,%r14d
    168f:	xor    %r12d,%r12d
    1692:	movq   $0x0,0x28(%rsp)
    169b:	mov    %rax,0x20(%rsp)
    16a0:	jmp    16cc <main+0x39c>
    16a2:	nopw   0x0(%rax,%rax,1)
    16a8:	movsd  %xmm3,(%r12)
    16ae:	add    $0x8,%r12
    16b2:	mov    %r12,0x148(%rsp)
    16ba:	sub    $0x1,%r13d
    16be:	je     17a9 <main+0x479>
    16c4:	mov    0x150(%rsp),%r14
    16cc:	call   11b0 <std::chrono::_V2::steady_clock::now()@plt>
    16d1:	mov    0x20(%rsp),%rdi
    16d6:	mov    %rbp,%rdx
    16d9:	mov    %rbx,%rsi
    16dc:	mov    $0x2000,%ecx
    16e1:	mov    %rax,%r15
    16e4:	call   28f0 <k_dbl_nocheck(Levels&, double const*, double const*, unsigned long)>
    16e9:	call   11b0 <std::chrono::_V2::steady_clock::now()@plt>
    16ee:	pxor   %xmm0,%xmm0
    16f2:	movsd  0x1ab6(%rip),%xmm3        # 31b0 <_IO_stdin_used+0x1b0>
    16fa:	sub    %r15,%rax
    16fd:	cvtsi2sd %rax,%xmm0
    1702:	mulsd  %xmm0,%xmm3
    1706:	movsd  %xmm3,0x18(%rsp)
    170c:	cmp    %r12,%r14
    170f:	jne    16a8 <main+0x378>
    1711:	mov    0x28(%rsp),%rax
    1716:	mov    %r14,%r15
    1719:	movabs $0xfffffffffffffff,%rdi
    1723:	sub    %rax,%r15
    1726:	mov    %r15,%rax
    1729:	sar    $0x3,%rax
    172d:	cmp    %rdi,%rax
    1730:	je     1e4f <main+0xb1f>
    1736:	cmp    %r14,0x28(%rsp)
    173b:	je     1b70 <main+0x840>
    1741:	lea    (%rax,%rax,1),%rdx
    1745:	cmp    %rax,%rdx
    1748:	jb     1ba3 <main+0x873>
    174e:	test   %rdx,%rdx
    1751:	jne    1e31 <main+0xb01>
    1757:	xor    %r8d,%r8d
    175a:	xor    %ecx,%ecx
    175c:	movsd  0x18(%rsp),%xmm5
    1762:	lea    0x8(%rcx,%r15,1),%r12
    1767:	movsd  %xmm5,(%rcx,%r15,1)
    176d:	test   %r15,%r15
    1770:	jg     1b20 <main+0x7f0>
    1776:	cmpq   $0x0,0x28(%rsp)
    177c:	jne    1b3d <main+0x80d>
    1782:	mov    %rcx,0x140(%rsp)
    178a:	mov    %r12,0x148(%rsp)
    1792:	mov    %r8,0x150(%rsp)
    179a:	mov    %rcx,0x28(%rsp)
    179f:	sub    $0x1,%r13d
    17a3:	jne    16c4 <main+0x394>
    17a9:	mov    0x28(%rsp),%r14
    17ae:	mov    %r12,%rsi
    17b1:	mov    $0x29,%r15d
    17b7:	mov    %r14,%rdi
    17ba:	call   25f0 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]>
    17bf:	lea    0x160(%rsp),%rax
    17c7:	movsd  0xa0(%r14),%xmm7
    17d0:	mov    %rax,0x20(%rsp)
    17d5:	movsd  %xmm7,0x70(%rsp)
    17db:	jmp    17fa <main+0x4ca>
    17dd:	nopl   (%rax)
    17e0:	movsd  %xmm4,(%rax)
    17e4:	add    $0x8,%rax
    17e8:	mov    %rax,0x108(%rsp)
    17f0:	sub    $0x1,%r15d
    17f4:	je     18ea <main+0x5ba>
    17fa:	call   11b0 <std::chrono::_V2::steady_clock::now()@plt>
    17ff:	mov    0x20(%rsp),%rdi
    1804:	mov    %rbp,%rdx
    1807:	mov    %rbx,%rsi
    180a:	mov    $0x2000,%ecx
    180f:	mov    %rax,%r13
    1812:	call   27b0 <k_dbl(Levels&, double const*, double const*, unsigned long)>
    1817:	call   11b0 <std::chrono::_V2::steady_clock::now()@plt>
    181c:	pxor   %xmm0,%xmm0
    1820:	movsd  0x1988(%rip),%xmm4        # 31b0 <_IO_stdin_used+0x1b0>
    1828:	mov    0x110(%rsp),%r14
    1830:	sub    %r13,%rax
    1833:	cvtsi2sd %rax,%xmm0
    1838:	mov    0x108(%rsp),%rax
    1840:	mulsd  %xmm0,%xmm4
    1844:	movsd  %xmm4,0x18(%rsp)
    184a:	cmp    %r14,%rax
    184d:	jne    17e0 <main+0x4b0>
    184f:	mov    0x100(%rsp),%rdi
    1857:	sub    %rdi,%rax
    185a:	mov    %rdi,0x30(%rsp)
    185f:	movabs $0xfffffffffffffff,%rdi
    1869:	mov    %rax,%r13
    186c:	sar    $0x3,%rax
    1870:	cmp    %rdi,%rax
    1873:	je     1e6e <main+0xb3e>
    1879:	mov    0x30(%rsp),%rdi
    187e:	cmp    %rdi,%r14
    1881:	je     1c0a <main+0x8da>
    1887:	lea    (%rax,%rax,1),%rdx
    188b:	cmp    %rax,%rdx
    188e:	jb     1c46 <main+0x916>
    1894:	xor    %r8d,%r8d
    1897:	xor    %ecx,%ecx
    1899:	test   %rdx,%rdx
    189c:	jne    1e05 <main+0xad5>
    18a2:	movsd  0x18(%rsp),%xmm6
    18a8:	lea    0x8(%rcx,%r13,1),%r9
    18ad:	movsd  %xmm6,(%rcx,%r13,1)
    18b3:	test   %r13,%r13
    18b6:	jg     1bb0 <main+0x880>
    18bc:	cmpq   $0x0,0x30(%rsp)
    18c2:	jne    1bd7 <main+0x8a7>
    18c8:	mov    %rcx,0x100(%rsp)
    18d0:	mov    %r9,0x108(%rsp)
    18d8:	mov    %r8,0x110(%rsp)
    18e0:	sub    $0x1,%r15d
    18e4:	jne    17fa <main+0x4ca>
    18ea:	mov    0x100(%rsp),%rbx
    18f2:	mov    0x108(%rsp),%rsi
    18fa:	mov    $0x29,%r13d
    1900:	xor    %r15d,%r15d
    1903:	mov    %rbx,%rdi
    1906:	mov    %rbx,0x40(%rsp)
    190b:	mov    %rsi,0x38(%rsp)
    1910:	call   25f0 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]>
    1915:	movsd  0xa0(%rbx),%xmm2
    191d:	xor    %ebx,%ebx
    191f:	lea    0x190(%rsp),%rax
    1927:	mov    %rax,0x18(%rsp)
    192c:	movsd  %xmm2,0x78(%rsp)
    1932:	jmp    1952 <main+0x622>
    1934:	nopl   0x0(%rax)
    1938:	movsd  %xmm0,(%rbx)
    193c:	add    $0x8,%rbx
    1940:	mov    %rbx,0x128(%rsp)
    1948:	sub    $0x1,%r13d
    194c:	je     1a1f <main+0x6ef>
    1952:	call   11b0 <std::chrono::_V2::steady_clock::now()@plt>
    1957:	mov    0x10(%rsp),%rdx
    195c:	mov    0x8(%rsp),%rsi
    1961:	mov    $0x2000,%ecx
    1966:	mov    0x18(%rsp),%rdi
    196b:	mov    %rax,%rbp
    196e:	call   29d0 <k_int(hot::Levels&, long const*, long const*, unsigned long)>
    1973:	call   11b0 <std::chrono::_V2::steady_clock::now()@plt>
    1978:	pxor   %xmm0,%xmm0
    197c:	sub    %rbp,%rax
    197f:	cvtsi2sd %rax,%xmm0
    1984:	mulsd  0x1824(%rip),%xmm0        # 31b0 <_IO_stdin_used+0x1b0>
    198c:	movq   %xmm0,%rbp
    1991:	cmp    %rbx,0x130(%rsp)
    1999:	jne    1938 <main+0x608>
    199b:	movabs $0xfffffffffffffff,%rdi
    19a5:	mov    %rbx,%r14
    19a8:	sub    %r15,%r14
    19ab:	mov    %r14,%rax
    19ae:	sar    $0x3,%rax
    19b2:	cmp    %rdi,%rax
    19b5:	je     1e8d <main+0xb5d>
    19bb:	cmp    %rbx,%r15
    19be:	je     1c91 <main+0x961>
    19c4:	lea    (%rax,%rax,1),%rdx
    19c8:	cmp    %rax,%rdx
    19cb:	jb     1cc4 <main+0x994>
    19d1:	xor    %r8d,%r8d
    19d4:	xor    %ecx,%ecx
    19d6:	test   %rdx,%rdx
    19d9:	jne    1e1b <main+0xaeb>
    19df:	mov    %rbp,(%rcx,%r14,1)
    19e3:	lea    0x8(%rcx,%r14,1),%rbx
    19e8:	test   %r14,%r14
    19eb:	jg     1c52 <main+0x922>
    19f1:	test   %r15,%r15
    19f4:	jne    1c6d <main+0x93d>
    19fa:	mov    %rcx,0x120(%rsp)
    1a02:	mov    %rcx,%r15
    1a05:	mov    %rbx,0x128(%rsp)
    1a0d:	mov    %r8,0x130(%rsp)
    1a15:	sub    $0x1,%r13d
    1a19:	jne    1952 <main+0x622>
    1a1f:	mov    %rbx,%rsi
    1a22:	mov    %r15,%rdi
    1a25:	call   25f0 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]>
    1a2a:	mov    0xa0(%r15),%rbp
    1a31:	mov    0x68(%rsp),%rsi
    1a36:	xor    %edx,%edx
    1a38:	mov    0x168(%rsp),%rcx
    1a40:	jmp    1a59 <main+0x729>
    1a42:	nopw   0x0(%rax,%rax,1)
    1a48:	add    $0x1,%rdx
    1a4c:	cmp    $0x7d1,%rdx
    1a53:	je     1cd0 <main+0x9a0>
    1a59:	cvttsd2si (%rcx,%rdx,8),%rax
    1a5f:	cmp    (%rsi,%rdx,8),%rax
    1a63:	je     1a48 <main+0x718>
    1a65:	lea    0x1703(%rip),%rsi        # 316f <_IO_stdin_used+0x16f>
    1a6c:	mov    $0x2,%edi
    1a71:	xor    %eax,%eax
    1a73:	call   1120 <__printf_chk@plt>
    1a78:	mov    0x60(%rsp),%rdi
    1a7d:	call   2a10 <std::vector<double, std::allocator<double> >::~vector()>
    1a82:	lea    0x140(%rsp),%rdi
    1a8a:	call   2a10 <std::vector<double, std::allocator<double> >::~vector()>
    1a8f:	lea    0x120(%rsp),%rdi
    1a97:	call   2a10 <std::vector<double, std::allocator<double> >::~vector()>
    1a9c:	lea    0x100(%rsp),%rdi
    1aa4:	call   2a10 <std::vector<double, std::allocator<double> >::~vector()>
    1aa9:	lea    0x198(%rsp),%rdi
    1ab1:	call   2a40 <std::vector<long, std::allocator<long> >::~vector()>
    1ab6:	mov    0x58(%rsp),%rdi
    1abb:	call   2a10 <std::vector<double, std::allocator<double> >::~vector()>
    1ac0:	lea    0xe0(%rsp),%rdi
    1ac8:	call   2a40 <std::vector<long, std::allocator<long> >::~vector()>
    1acd:	lea    0xc0(%rsp),%rdi
    1ad5:	call   2a40 <std::vector<long, std::allocator<long> >::~vector()>
    1ada:	mov    0x50(%rsp),%rdi
    1adf:	call   2a10 <std::vector<double, std::allocator<double> >::~vector()>
    1ae4:	mov    0x48(%rsp),%rdi
    1ae9:	call   2a10 <std::vector<double, std::allocator<double> >::~vector()>
    1aee:	mov    $0x1,%eax
    1af3:	mov    0xbb8(%rsp),%rdx
    1afb:	sub    %fs:0x28,%rdx
    1b04:	jne    1eac <main+0xb7c>
    1b0a:	add    $0xbc8,%rsp
    1b11:	pop    %rbx
    1b12:	pop    %rbp
    1b13:	pop    %r12
    1b15:	pop    %r13
    1b17:	pop    %r14
    1b19:	pop    %r15
    1b1b:	ret
    1b1c:	nopl   0x0(%rax)
    1b20:	mov    0x28(%rsp),%rsi
    1b25:	mov    %rcx,%rdi
    1b28:	mov    %r15,%rdx
    1b2b:	mov    %r8,0x18(%rsp)
    1b30:	call   11c0 <memmove@plt>
    1b35:	mov    0x18(%rsp),%r8
    1b3a:	mov    %rax,%rcx
    1b3d:	mov    0x28(%rsp),%rdi
    1b42:	mov    %r14,%rsi
    1b45:	mov    %r8,0x30(%rsp)
    1b4a:	mov    %rcx,0x18(%rsp)
    1b4f:	sub    %rdi,%rsi
    1b52:	call   1190 <operator delete(void*, unsigned long)@plt>
    1b57:	mov    0x30(%rsp),%r8
    1b5c:	mov    0x18(%rsp),%rcx
    1b61:	jmp    1782 <main+0x452>
    1b66:	cs nopw 0x0(%rax,%rax,1)
    1b70:	add    $0x1,%rax
    1b74:	jb     1ba3 <main+0x873>
    1b76:	movabs $0xfffffffffffffff,%rdx
    1b80:	cmp    %rdx,%rax
    1b83:	cmova  %rdx,%rax
    1b87:	lea    0x0(,%rax,8),%r12
    1b8f:	mov    %r12,%rdi
    1b92:	call   1180 <operator new(unsigned long)@plt>
    1b97:	mov    %rax,%rcx
    1b9a:	lea    (%rax,%r12,1),%r8
    1b9e:	jmp    175c <main+0x42c>
    1ba3:	movabs $0x7ffffffffffffff8,%r12
    1bad:	jmp    1b8f <main+0x85f>
    1baf:	nop
    1bb0:	mov    0x30(%rsp),%rsi
    1bb5:	mov    %rcx,%rdi
    1bb8:	mov    %r13,%rdx
    1bbb:	mov    %r8,0x38(%rsp)
    1bc0:	mov    %r9,0x18(%rsp)
    1bc5:	call   11c0 <memmove@plt>
    1bca:	mov    0x18(%rsp),%r9
    1bcf:	mov    0x38(%rsp),%r8
    1bd4:	mov    %rax,%rcx
    1bd7:	mov    0x30(%rsp),%rdi
    1bdc:	mov    %r14,%rsi
    1bdf:	mov    %rcx,0x40(%rsp)
    1be4:	mov    %r8,0x38(%rsp)
    1be9:	sub    %rdi,%rsi
    1bec:	mov    %r9,0x18(%rsp)
    1bf1:	call   1190 <operator delete(void*, unsigned long)@plt>
    1bf6:	mov    0x40(%rsp),%rcx
    1bfb:	mov    0x38(%rsp),%r8
    1c00:	mov    0x18(%rsp),%r9
    1c05:	jmp    18c8 <main+0x598>
    1c0a:	movabs $0xfffffffffffffff,%rdx
    1c14:	add    $0x1,%rax
    1c18:	jb     1c21 <main+0x8f1>
    1c1a:	cmp    %rdx,%rax
    1c1d:	cmovbe %rax,%rdx
    1c21:	lea    0x0(,%rdx,8),%rax
    1c29:	mov    %rax,%rdi
    1c2c:	mov    %rax,0x38(%rsp)
    1c31:	call   1180 <operator new(unsigned long)@plt>
    1c36:	mov    0x38(%rsp),%r8
    1c3b:	mov    %rax,%rcx
    1c3e:	add    %rax,%r8
    1c41:	jmp    18a2 <main+0x572>
    1c46:	movabs $0xfffffffffffffff,%rdx
    1c50:	jmp    1c21 <main+0x8f1>
    1c52:	mov    %rcx,%rdi
    1c55:	mov    %r14,%rdx
    1c58:	mov    %r15,%rsi
    1c5b:	mov    %r8,0x20(%rsp)
    1c60:	call   11c0 <memmove@plt>
    1c65:	mov    0x20(%rsp),%r8
    1c6a:	mov    %rax,%rcx
    1c6d:	mov    %r14,%rsi
    1c70:	mov    %r15,%rdi
    1c73:	mov    %rcx,0x30(%rsp)
    1c78:	mov    %r8,0x20(%rsp)
    1c7d:	call   1190 <operator delete(void*, unsigned long)@plt>
    1c82:	mov    0x30(%rsp),%rcx
    1c87:	mov    0x20(%rsp),%r8
    1c8c:	jmp    19fa <main+0x6ca>
    1c91:	movabs $0xfffffffffffffff,%rdx
    1c9b:	add    $0x1,%rax
    1c9f:	jb     1ca8 <main+0x978>
    1ca1:	cmp    %rdx,%rax
    1ca4:	cmovbe %rax,%rdx
    1ca8:	lea    0x0(,%rdx,8),%rbx
    1cb0:	mov    %rbx,%rdi
    1cb3:	call   1180 <operator new(unsigned long)@plt>
    1cb8:	mov    %rax,%rcx
    1cbb:	lea    (%rax,%rbx,1),%r8
    1cbf:	jmp    19df <main+0x6af>
    1cc4:	movabs $0xfffffffffffffff,%rdx
    1cce:	jmp    1ca8 <main+0x978>
    1cd0:	mov    0x38(%rsp),%rax
    1cd5:	movsd  0x78(%rsp),%xmm0
    1cdb:	mov    $0x2,%edi
    1ce0:	lea    0x1359(%rip),%rsi        # 3040 <_IO_stdin_used+0x40>
    1ce7:	movsd  -0x8(%rax),%xmm2
    1cec:	mov    0x40(%rsp),%rax
    1cf1:	movsd  (%rax),%xmm1
    1cf5:	mov    $0x3,%eax
    1cfa:	call   1120 <__printf_chk@plt>
    1cff:	mov    0x28(%rsp),%rax
    1d04:	movsd  -0x8(%r12),%xmm2
    1d0b:	lea    0x1376(%rip),%rsi        # 3088 <_IO_stdin_used+0x88>
    1d12:	mov    $0x2,%edi
    1d17:	movsd  0x70(%rsp),%xmm0
    1d1d:	movsd  (%rax),%xmm1
    1d21:	mov    $0x3,%eax
    1d26:	call   1120 <__printf_chk@plt>
    1d2b:	movsd  -0x8(%rbx),%xmm2
    1d30:	movsd  (%r15),%xmm1
    1d35:	movq   %rbp,%xmm0
    1d3a:	lea    0x138f(%rip),%rsi        # 30d0 <_IO_stdin_used+0xd0>
    1d41:	mov    $0x2,%edi
    1d46:	mov    $0x3,%eax
    1d4b:	call   1120 <__printf_chk@plt>
    1d50:	pxor   %xmm1,%xmm1
    1d54:	mov    0x1b0(%rsp),%rdx
    1d5c:	movsd  0x180(%rsp),%xmm0
    1d65:	lea    0x13ac(%rip),%rsi        # 3118 <_IO_stdin_used+0x118>
    1d6c:	mov    $0x2,%edi
    1d71:	mov    $0x2,%eax
    1d76:	cvtsi2sd %rdx,%xmm1
    1d7b:	divsd  0x141d(%rip),%xmm1        # 31a0 <_IO_stdin_used+0x1a0>
    1d83:	call   1120 <__printf_chk@plt>
    1d88:	mov    0x60(%rsp),%rdi
    1d8d:	call   2a10 <std::vector<double, std::allocator<double> >::~vector()>
    1d92:	lea    0x140(%rsp),%rdi
    1d9a:	call   2a10 <std::vector<double, std::allocator<double> >::~vector()>
    1d9f:	lea    0x120(%rsp),%rdi
    1da7:	call   2a10 <std::vector<double, std::allocator<double> >::~vector()>
    1dac:	lea    0x100(%rsp),%rdi
    1db4:	call   2a10 <std::vector<double, std::allocator<double> >::~vector()>
    1db9:	lea    0x198(%rsp),%rdi
    1dc1:	call   2a40 <std::vector<long, std::allocator<long> >::~vector()>
    1dc6:	mov    0x58(%rsp),%rdi
    1dcb:	call   2a10 <std::vector<double, std::allocator<double> >::~vector()>
    1dd0:	lea    0xe0(%rsp),%rdi
    1dd8:	call   2a40 <std::vector<long, std::allocator<long> >::~vector()>
    1ddd:	lea    0xc0(%rsp),%rdi
    1de5:	call   2a40 <std::vector<long, std::allocator<long> >::~vector()>
    1dea:	mov    0x50(%rsp),%rdi
    1def:	call   2a10 <std::vector<double, std::allocator<double> >::~vector()>
    1df4:	mov    0x48(%rsp),%rdi
    1df9:	call   2a10 <std::vector<double, std::allocator<double> >::~vector()>
    1dfe:	xor    %eax,%eax
    1e00:	jmp    1af3 <main+0x7c3>
    1e05:	movabs $0xfffffffffffffff,%rax
    1e0f:	cmp    %rax,%rdx
    1e12:	cmova  %rax,%rdx
    1e16:	jmp    1c21 <main+0x8f1>
    1e1b:	movabs $0xfffffffffffffff,%rax
    1e25:	cmp    %rax,%rdx
    1e28:	cmova  %rax,%rdx
    1e2c:	jmp    1ca8 <main+0x978>
    1e31:	movabs $0xfffffffffffffff,%rax
    1e3b:	cmp    %rax,%rdx
    1e3e:	cmova  %rax,%rdx
    1e42:	lea    0x0(,%rdx,8),%r12
    1e4a:	jmp    1b8f <main+0x85f>
    1e4f:	mov    0xbb8(%rsp),%rax
    1e57:	sub    %fs:0x28,%rax
    1e60:	jne    1eac <main+0xb7c>
    1e62:	lea    0x12ec(%rip),%rdi        # 3155 <_IO_stdin_used+0x155>
    1e69:	call   1150 <std::__throw_length_error(char const*)@plt>
    1e6e:	mov    0xbb8(%rsp),%rax
    1e76:	sub    %fs:0x28,%rax
    1e7f:	jne    1eac <main+0xb7c>
    1e81:	lea    0x12cd(%rip),%rdi        # 3155 <_IO_stdin_used+0x155>
    1e88:	call   1150 <std::__throw_length_error(char const*)@plt>
    1e8d:	mov    0xbb8(%rsp),%rax
    1e95:	sub    %fs:0x28,%rax
    1e9e:	jne    1eac <main+0xb7c>
    1ea0:	lea    0x12ae(%rip),%rdi        # 3155 <_IO_stdin_used+0x155>
    1ea7:	call   1150 <std::__throw_length_error(char const*)@plt>
    1eac:	call   11a0 <__stack_chk_fail@plt>
    1eb1:	endbr64
    1eb5:	mov    %rax,%rbx
    1eb8:	jmp    1292 <main.cold>
    1ebd:	endbr64
    1ec1:	mov    %rax,%rbx
    1ec4:	jmp    129c <main.cold+0xa>
    1ec9:	endbr64
    1ecd:	mov    %rax,%rbx
    1ed0:	jmp    12d0 <main.cold+0x3e>
    1ed5:	endbr64
    1ed9:	mov    %rax,%rbx
    1edc:	jmp    12da <main.cold+0x48>
    1ee1:	endbr64
    1ee5:	mov    %rax,%rbx
    1ee8:	jmp    12e7 <main.cold+0x55>
    1eed:	endbr64
    1ef1:	mov    %rax,%rbx
    1ef4:	jmp    12f4 <main.cold+0x62>
    1ef9:	endbr64
    1efd:	mov    %rax,%rbx
    1f00:	jmp    12fe <main.cold+0x6c>
    1f05:	cs nopw 0x0(%rax,%rax,1)
    1f0f:	nop

0000000000001f10 <_start>:
    1f10:	endbr64
    1f14:	xor    %ebp,%ebp
    1f16:	mov    %rdx,%r9
    1f19:	pop    %rsi
    1f1a:	mov    %rsp,%rdx
    1f1d:	and    $0xfffffffffffffff0,%rsp
    1f21:	push   %rax
    1f22:	push   %rsp
    1f23:	xor    %r8d,%r8d
    1f26:	xor    %ecx,%ecx
    1f28:	lea    -0xbff(%rip),%rdi        # 1330 <main>
    1f2f:	call   *0x30a3(%rip)        # 4fd8 <__libc_start_main@GLIBC_2.34>
    1f35:	hlt
    1f36:	cs nopw 0x0(%rax,%rax,1)

0000000000001f40 <deregister_tm_clones>:
    1f40:	lea    0x30d1(%rip),%rdi        # 5018 <__TMC_END__>
    1f47:	lea    0x30ca(%rip),%rax        # 5018 <__TMC_END__>
    1f4e:	cmp    %rdi,%rax
    1f51:	je     1f68 <deregister_tm_clones+0x28>
    1f53:	mov    0x308e(%rip),%rax        # 4fe8 <_ITM_deregisterTMCloneTable@Base>
    1f5a:	test   %rax,%rax
    1f5d:	je     1f68 <deregister_tm_clones+0x28>
    1f5f:	jmp    *%rax
    1f61:	nopl   0x0(%rax)
    1f68:	ret
    1f69:	nopl   0x0(%rax)

0000000000001f70 <register_tm_clones>:
    1f70:	lea    0x30a1(%rip),%rdi        # 5018 <__TMC_END__>
    1f77:	lea    0x309a(%rip),%rsi        # 5018 <__TMC_END__>
    1f7e:	sub    %rdi,%rsi
    1f81:	mov    %rsi,%rax
    1f84:	shr    $0x3f,%rsi
    1f88:	sar    $0x3,%rax
    1f8c:	add    %rax,%rsi
    1f8f:	sar    $1,%rsi
    1f92:	je     1fa8 <register_tm_clones+0x38>
    1f94:	mov    0x305d(%rip),%rax        # 4ff8 <_ITM_registerTMCloneTable@Base>
    1f9b:	test   %rax,%rax
    1f9e:	je     1fa8 <register_tm_clones+0x38>
    1fa0:	jmp    *%rax
    1fa2:	nopw   0x0(%rax,%rax,1)
    1fa8:	ret
    1fa9:	nopl   0x0(%rax)

0000000000001fb0 <__do_global_dtors_aux>:
    1fb0:	endbr64
    1fb4:	cmpb   $0x0,0x305d(%rip)        # 5018 <__TMC_END__>
    1fbb:	jne    1fe8 <__do_global_dtors_aux+0x38>
    1fbd:	push   %rbp
    1fbe:	cmpq   $0x0,0x300a(%rip)        # 4fd0 <__cxa_finalize@GLIBC_2.2.5>
    1fc6:	mov    %rsp,%rbp
    1fc9:	je     1fd7 <__do_global_dtors_aux+0x27>
    1fcb:	mov    0x3036(%rip),%rdi        # 5008 <__dso_handle>
    1fd2:	call   1110 <__cxa_finalize@plt>
    1fd7:	call   1f40 <deregister_tm_clones>
    1fdc:	movb   $0x1,0x3035(%rip)        # 5018 <__TMC_END__>
    1fe3:	pop    %rbp
    1fe4:	ret
    1fe5:	nopl   (%rax)
    1fe8:	ret
    1fe9:	nopl   0x0(%rax)

0000000000001ff0 <frame_dummy>:
    1ff0:	endbr64
    1ff4:	jmp    1f70 <register_tm_clones>
    1ff9:	nopl   0x0(%rax)

0000000000002000 <void std::__insertion_sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]>:
    2000:	cmp    %rsi,%rdi
    2003:	je     20bf <void std::__insertion_sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xbf>
    2009:	push   %r13
    200b:	mov    %rsi,%r13
    200e:	push   %r12
    2010:	push   %rbp
    2011:	mov    %rdi,%rbp
    2014:	push   %rbx
    2015:	lea    0x8(%rdi),%rbx
    2019:	sub    $0x18,%rsp
    201d:	cmp    %rbx,%rsi
    2020:	je     20ac <void std::__insertion_sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xac>
    2026:	mov    $0x8,%r12d
    202c:	jmp    2064 <void std::__insertion_sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x64>
    202e:	xchg   %ax,%ax
    2030:	sub    %rbp,%rdx
    2033:	cmp    $0x8,%rdx
    2037:	jle    20b7 <void std::__insertion_sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xb7>
    2039:	mov    %r12,%rdi
    203c:	mov    %rbp,%rsi
    203f:	movsd  %xmm1,0x8(%rsp)
    2045:	sub    %rdx,%rdi
    2048:	add    %rbx,%rdi
    204b:	call   11c0 <memmove@plt>
    2050:	movsd  0x8(%rsp),%xmm1
    2056:	add    $0x8,%rbx
    205a:	movsd  %xmm1,0x0(%rbp)
    205f:	cmp    %r13,%rbx
    2062:	je     20ac <void std::__insertion_sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xac>
    2064:	movsd  (%rbx),%xmm1
    2068:	movsd  0x0(%rbp),%xmm0
    206d:	mov    %rbx,%rdx
    2070:	comisd %xmm1,%xmm0
    2074:	ja     2030 <void std::__insertion_sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x30>
    2076:	movsd  -0x8(%rbx),%xmm0
    207b:	lea    -0x8(%rbx),%rax
    207f:	comisd %xmm1,%xmm0
    2083:	jbe    209f <void std::__insertion_sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x9f>
    2085:	nopl   (%rax)
    2088:	movsd  %xmm0,0x8(%rax)
    208d:	mov    %rax,%rdx
    2090:	movsd  -0x8(%rax),%xmm0
    2095:	sub    $0x8,%rax
    2099:	comisd %xmm1,%xmm0
    209d:	ja     2088 <void std::__insertion_sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x88>
    209f:	add    $0x8,%rbx
    20a3:	movsd  %xmm1,(%rdx)
    20a7:	cmp    %r13,%rbx
    20aa:	jne    2064 <void std::__insertion_sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x64>
    20ac:	add    $0x18,%rsp
    20b0:	pop    %rbx
    20b1:	pop    %rbp
    20b2:	pop    %r12
    20b4:	pop    %r13
    20b6:	ret
    20b7:	jne    2056 <void std::__insertion_sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x56>
    20b9:	movsd  %xmm0,(%rbx)
    20bd:	jmp    2056 <void std::__insertion_sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x56>
    20bf:	ret

00000000000020c0 <std::vector<double, std::allocator<double> >::vector(unsigned long, std::allocator<double> const&) [clone .isra.0]>:
    20c0:	push   %r13
    20c2:	mov    %rsi,%rax
    20c5:	push   %r12
    20c7:	push   %rbp
    20c8:	push   %rbx
    20c9:	sub    $0x8,%rsp
    20cd:	shr    $0x3c,%rax
    20d1:	jne    2149 <std::vector<double, std::allocator<double> >::vector(unsigned long, std::allocator<double> const&) [clone .isra.0]+0x89>
    20d3:	pxor   %xmm0,%xmm0
    20d7:	movq   $0x0,0x10(%rdi)
    20df:	mov    %rdi,%rbx
    20e2:	mov    %rsi,%rbp
    20e5:	movups %xmm0,(%rdi)
    20e8:	test   %rsi,%rsi
    20eb:	je     213c <std::vector<double, std::allocator<double> >::vector(unsigned long, std::allocator<double> const&) [clone .isra.0]+0x7c>
    20ed:	lea    0x0(,%rsi,8),%r12
    20f5:	mov    %r12,%rdi
    20f8:	call   1180 <operator new(unsigned long)@plt>
    20fd:	sub    $0x1,%rbp
    2101:	lea    (%rax,%r12,1),%r13
    2105:	mov    %rax,(%rbx)
    2108:	lea    0x8(%rax),%rdi
    210c:	mov    %r13,0x10(%rbx)
    2110:	movq   $0x0,(%rax)
    2117:	je     212d <std::vector<double, std::allocator<double> >::vector(unsigned long, std::allocator<double> const&) [clone .isra.0]+0x6d>
    2119:	cmp    %rdi,%r13
    211c:	je     212a <std::vector<double, std::allocator<double> >::vector(unsigned long, std::allocator<double> const&) [clone .isra.0]+0x6a>
    211e:	lea    -0x8(%r12),%rdx
    2123:	xor    %esi,%esi
    2125:	call   1160 <memset@plt>
    212a:	mov    %r13,%rdi
    212d:	mov    %rdi,0x8(%rbx)
    2131:	add    $0x8,%rsp
    2135:	pop    %rbx
    2136:	pop    %rbp
    2137:	pop    %r12
    2139:	pop    %r13
    213b:	ret
    213c:	xor    %eax,%eax
    213e:	mov    %rax,(%rdi)
    2141:	mov    %rax,0x10(%rdi)
    2145:	xor    %edi,%edi
    2147:	jmp    212d <std::vector<double, std::allocator<double> >::vector(unsigned long, std::allocator<double> const&) [clone .isra.0]+0x6d>
    2149:	lea    0xeb8(%rip),%rdi        # 3008 <_IO_stdin_used+0x8>
    2150:	call   1150 <std::__throw_length_error(char const*)@plt>
    2155:	data16 cs nopw 0x0(%rax,%rax,1)

0000000000002160 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]>:
    2160:	push   %r12
    2162:	mov    %rsi,%rax
    2165:	push   %rbp
    2166:	sub    %rdi,%rax
    2169:	mov    %rdi,%rbp
    216c:	push   %rbx
    216d:	sub    $0x10,%rsp
    2171:	cmp    $0x80,%rax
    2177:	jle    2403 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x2a3>
    217d:	mov    %rdx,%r12
    2180:	mov    %rsi,%rcx
    2183:	test   %rdx,%rdx
    2186:	je     240c <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x2ac>
    218c:	mov    %rsi,%rdi
    218f:	lea    0x8(%rbp),%rbx
    2193:	movupd 0x0(%rbp),%xmm0
    2198:	sar    $0x4,%rax
    219c:	sub    $0x1,%r12
    21a0:	movsd  -0x8(%rdi),%xmm3
    21a5:	lea    0x0(%rbp,%rax,8),%rax
    21aa:	movsd  (%rax),%xmm2
    21ae:	movapd %xmm0,%xmm5
    21b2:	movapd %xmm0,%xmm4
    21b6:	unpckhpd %xmm5,%xmm5
    21ba:	shufpd $0x1,%xmm0,%xmm4
    21bf:	comisd %xmm5,%xmm2
    21c3:	movapd %xmm5,%xmm1
    21c7:	jbe    22bb <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x15b>
    21cd:	comisd %xmm2,%xmm3
    21d1:	ja     22e8 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x188>
    21d7:	comisd %xmm5,%xmm3
    21db:	ja     22cb <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x16b>
    21e1:	movups %xmm4,0x0(%rbp)
    21e5:	movsd  -0x8(%rdi),%xmm2
    21ea:	comisd %xmm0,%xmm1
    21ee:	mov    %rbx,%rsi
    21f1:	mov    %rdi,%rdx
    21f4:	lea    0x8(%rsi),%rax
    21f8:	jbe    225b <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xfb>
    21fa:	nopw   0x0(%rax,%rax,1)
    2200:	mov    %rax,%rcx
    2203:	movsd  (%rax),%xmm0
    2207:	add    $0x8,%rax
    220b:	comisd %xmm0,%xmm1
    220f:	ja     2200 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xa0>
    2211:	comisd %xmm1,%xmm2
    2215:	lea    -0x10(%rdx),%rax
    2219:	jbe    2270 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x110>
    221b:	nopl   0x0(%rax,%rax,1)
    2220:	mov    %rax,%rdx
    2223:	movsd  (%rax),%xmm2
    2227:	sub    $0x8,%rax
    222b:	comisd %xmm1,%xmm2
    222f:	ja     2220 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xc0>
    2231:	cmp    %rdx,%rcx
    2234:	jae    2280 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x120>
    2236:	movsd  %xmm2,(%rcx)
    223a:	lea    0x8(%rcx),%rsi
    223e:	movsd  -0x8(%rdx),%xmm2
    2243:	movsd  %xmm0,(%rdx)
    2247:	movsd  0x8(%rcx),%xmm0
    224c:	movsd  0x0(%rbp),%xmm1
    2251:	lea    0x8(%rsi),%rax
    2255:	comisd %xmm0,%xmm1
    2259:	ja     2200 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xa0>
    225b:	comisd %xmm1,%xmm2
    225f:	mov    %rsi,%rcx
    2262:	lea    -0x10(%rdx),%rax
    2266:	ja     2220 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xc0>
    2268:	nopl   0x0(%rax,%rax,1)
    2270:	sub    $0x8,%rdx
    2274:	cmp    %rdx,%rcx
    2277:	jb     2236 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xd6>
    2279:	nopl   0x0(%rax)
    2280:	mov    %rdi,%rsi
    2283:	mov    %r12,%rdx
    2286:	mov    %rcx,%rdi
    2289:	mov    %rcx,0x8(%rsp)
    228e:	call   2160 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]>
    2293:	mov    0x8(%rsp),%rcx
    2298:	mov    %rcx,%rax
    229b:	sub    %rbp,%rax
    229e:	cmp    $0x80,%rax
    22a4:	jle    2403 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x2a3>
    22aa:	test   %r12,%r12
    22ad:	je     240c <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x2ac>
    22b3:	mov    %rcx,%rdi
    22b6:	jmp    2193 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x33>
    22bb:	comisd %xmm5,%xmm3
    22bf:	ja     21e1 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x81>
    22c5:	comisd %xmm2,%xmm3
    22c9:	jbe    22e8 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x188>
    22cb:	movsd  %xmm3,0x0(%rbp)
    22d0:	movapd %xmm0,%xmm2
    22d4:	movsd  %xmm0,-0x8(%rdi)
    22d9:	movsd  0x0(%rbp),%xmm1
    22de:	movsd  0x8(%rbp),%xmm0
    22e3:	jmp    21ea <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x8a>
    22e8:	movsd  %xmm2,0x0(%rbp)
    22ed:	movsd  %xmm0,(%rax)
    22f1:	movsd  0x8(%rbp),%xmm0
    22f6:	movsd  0x0(%rbp),%xmm1
    22fb:	movsd  -0x8(%rdi),%xmm2
    2300:	jmp    21ea <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x8a>
    2305:	sub    $0x8,%rcx
    2309:	nopl   0x0(%rax)
    2310:	mov    %rcx,%rdi
    2313:	movsd  0x0(%rbp),%xmm0
    2318:	movsd  (%rcx),%xmm2
    231c:	sub    %rbp,%rdi
    231f:	mov    %rdi,%r11
    2322:	movsd  %xmm0,(%rcx)
    2326:	sar    $0x3,%r11
    232a:	lea    -0x1(%r11),%rax
    232e:	mov    %r11,%rbx
    2331:	mov    %rax,%r10
    2334:	and    $0x1,%ebx
    2337:	shr    $0x3f,%r10
    233b:	add    %rax,%r10
    233e:	sar    $1,%r10
    2341:	cmp    $0x10,%rdi
    2345:	jle    258a <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x42a>
    234b:	xor    %esi,%esi
    234d:	jmp    2353 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x1f3>
    234f:	nop
    2350:	mov    %rdx,%rsi
    2353:	lea    0x1(%rsi),%rax
    2357:	lea    (%rax,%rax,1),%rdx
    235b:	shl    $0x4,%rax
    235f:	lea    -0x1(%rdx),%r8
    2363:	add    %rbp,%rax
    2366:	lea    0x0(%rbp,%r8,8),%r9
    236b:	movsd  (%rax),%xmm0
    236f:	movsd  (%r9),%xmm1
    2374:	comisd %xmm0,%xmm1
    2378:	jbe    2384 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x224>
    237a:	movapd %xmm1,%xmm0
    237e:	mov    %r9,%rax
    2381:	mov    %r8,%rdx
    2384:	movsd  %xmm0,0x0(%rbp,%rsi,8)
    238a:	cmp    %r10,%rdx
    238d:	jl     2350 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x1f0>
    238f:	test   %rbx,%rbx
    2392:	je     2534 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x3d4>
    2398:	lea    -0x1(%rdx),%r8
    239c:	mov    %r8,%rsi
    239f:	shr    $0x3f,%rsi
    23a3:	add    %r8,%rsi
    23a6:	sar    $1,%rsi
    23a9:	test   %rdx,%rdx
    23ac:	jne    23dc <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x27c>
    23ae:	jmp    25dd <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x47d>
    23b3:	nopl   0x0(%rax,%rax,1)
    23b8:	lea    -0x1(%rsi),%rdx
    23bc:	movsd  %xmm0,(%rax)
    23c0:	mov    %rdx,%rax
    23c3:	shr    $0x3f,%rax
    23c7:	add    %rdx,%rax
    23ca:	mov    %rsi,%rdx
    23cd:	sar    $1,%rax
    23d0:	test   %rsi,%rsi
    23d3:	je     251a <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x3ba>
    23d9:	mov    %rax,%rsi
    23dc:	lea    0x0(%rbp,%rsi,8),%r8
    23e1:	lea    0x0(%rbp,%rdx,8),%rax
    23e6:	movsd  (%r8),%xmm0
    23eb:	comisd %xmm0,%xmm2
    23ef:	ja     23b8 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x258>
    23f1:	movsd  %xmm2,(%rax)
    23f5:	sub    $0x8,%rcx
    23f9:	cmp    $0x8,%rdi
    23fd:	jg     2310 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x1b0>
    2403:	add    $0x10,%rsp
    2407:	pop    %rbx
    2408:	pop    %rbp
    2409:	pop    %r12
    240b:	ret
    240c:	sar    $0x3,%rax
    2410:	lea    -0x2(%rax),%r11
    2414:	lea    -0x1(%rax),%r9
    2418:	not    %rax
    241b:	sar    $1,%r11
    241e:	mov    %eax,%r8d
    2421:	sar    $1,%r9
    2424:	lea    0x0(%rbp,%r11,8),%r10
    2429:	mov    %r11,%rdi
    242c:	and    $0x1,%r8d
    2430:	movsd  (%r10),%xmm2
    2435:	mov    %r10,%rdx
    2438:	cmp    %r9,%rdi
    243b:	jge    250d <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x3ad>
    2441:	mov    %rdi,%rsi
    2444:	jmp    2453 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x2f3>
    2446:	cs nopw 0x0(%rax,%rax,1)
    2450:	mov    %rax,%rsi
    2453:	lea    0x1(%rsi),%rdx
    2457:	lea    (%rdx,%rdx,1),%rax
    245b:	shl    $0x4,%rdx
    245f:	lea    -0x1(%rax),%rbx
    2463:	add    %rbp,%rdx
    2466:	lea    0x0(%rbp,%rbx,8),%r12
    246b:	movsd  (%rdx),%xmm0
    246f:	movsd  (%r12),%xmm1
    2475:	comisd %xmm0,%xmm1
    2479:	jbe    2485 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x325>
    247b:	movapd %xmm1,%xmm0
    247f:	mov    %r12,%rdx
    2482:	mov    %rbx,%rax
    2485:	movsd  %xmm0,0x0(%rbp,%rsi,8)
    248b:	cmp    %r9,%rax
    248e:	jl     2450 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x2f0>
    2490:	cmp    %rax,%r11
    2493:	jne    249e <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x33e>
    2495:	test   %r8b,%r8b
    2498:	jne    25b0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x450>
    249e:	lea    -0x1(%rax),%rsi
    24a2:	sar    $1,%rsi
    24a5:	cmp    %rax,%rdi
    24a8:	jl     24d3 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x373>
    24aa:	jmp    25d4 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x474>
    24af:	nop
    24b0:	lea    -0x1(%rsi),%rdx
    24b4:	movsd  %xmm0,(%rax)
    24b8:	mov    %rdx,%rax
    24bb:	shr    $0x3f,%rax
    24bf:	add    %rdx,%rax
    24c2:	sar    $1,%rax
    24c5:	mov    %rax,%rdx
    24c8:	mov    %rsi,%rax
    24cb:	cmp    %rsi,%rdi
    24ce:	jge    2515 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x3b5>
    24d0:	mov    %rdx,%rsi
    24d3:	lea    0x0(%rbp,%rsi,8),%rbx
    24d8:	lea    0x0(%rbp,%rax,8),%rax
    24dd:	movsd  (%rbx),%xmm0
    24e1:	comisd %xmm0,%xmm2
    24e5:	ja     24b0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x350>
    24e7:	movsd  %xmm2,(%rax)
    24eb:	test   %rdi,%rdi
    24ee:	je     2305 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x1a5>
    24f4:	sub    $0x8,%r10
    24f8:	sub    $0x1,%rdi
    24fc:	movsd  (%r10),%xmm2
    2501:	mov    %r10,%rdx
    2504:	cmp    %r9,%rdi
    2507:	jl     2441 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x2e1>
    250d:	mov    %rdi,%rax
    2510:	jmp    2490 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x330>
    2515:	mov    %rbx,%rax
    2518:	jmp    24e7 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x387>
    251a:	mov    %r8,%rax
    251d:	sub    $0x8,%rcx
    2521:	movsd  %xmm2,(%rax)
    2525:	cmp    $0x8,%rdi
    2529:	jg     2310 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x1b0>
    252f:	jmp    2403 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x2a3>
    2534:	lea    -0x2(%r11),%rsi
    2538:	sar    $1,%rsi
    253b:	cmp    %rdx,%rsi
    253e:	je     256f <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x40f>
    2540:	lea    -0x1(%rdx),%r8
    2544:	mov    %r8,%rsi
    2547:	shr    $0x3f,%rsi
    254b:	add    %r8,%rsi
    254e:	sar    $1,%rsi
    2551:	test   %rdx,%rdx
    2554:	jne    23dc <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x27c>
    255a:	jmp    23f1 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x291>
    255f:	nop
    2560:	cmp    $0x2,%rax
    2564:	mov    %rbp,%rax
    2567:	ja     23f1 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x291>
    256d:	xor    %edx,%edx
    256f:	lea    0x1(%rdx,%rdx,1),%r8
    2574:	mov    %rdx,%rsi
    2577:	movsd  0x0(%rbp,%r8,8),%xmm0
    257e:	mov    %r8,%rdx
    2581:	movsd  %xmm0,(%rax)
    2585:	jmp    23dc <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x27c>
    258a:	test   %rbx,%rbx
    258d:	je     2560 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x400>
    258f:	mov    %rbp,%rax
    2592:	sub    $0x8,%rcx
    2596:	movsd  %xmm2,(%rax)
    259a:	cmp    $0x8,%rdi
    259e:	jg     2310 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x1b0>
    25a4:	jmp    2403 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x2a3>
    25a9:	nopl   0x0(%rax)
    25b0:	lea    (%rax,%rax,1),%rsi
    25b4:	lea    0x1(%rsi),%rax
    25b8:	sar    $1,%rsi
    25bb:	lea    0x0(%rbp,%rax,8),%rbx
    25c0:	movsd  (%rbx),%xmm0
    25c4:	movsd  %xmm0,(%rdx)
    25c8:	mov    %rbx,%rdx
    25cb:	cmp    %rax,%rdi
    25ce:	jl     24d3 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x373>
    25d4:	movsd  %xmm2,(%rdx)
    25d8:	jmp    24f4 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x394>
    25dd:	movsd  %xmm2,(%rax)
    25e1:	sub    $0x8,%rcx
    25e5:	jmp    2310 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x1b0>
    25ea:	nopw   0x0(%rax,%rax,1)

00000000000025f0 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]>:
    25f0:	cmp    %rsi,%rdi
    25f3:	je     26b8 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xc8>
    25f9:	push   %r12
    25fb:	mov    $0x40,%eax
    2600:	mov    %rdi,%r12
    2603:	push   %rbp
    2604:	mov    %rsi,%rbp
    2607:	push   %rbx
    2608:	mov    %rsi,%rbx
    260b:	sub    %rdi,%rbx
    260e:	mov    %rbx,%rdx
    2611:	sar    $0x3,%rdx
    2615:	je     261e <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x2e>
    2617:	bsr    %rdx,%rax
    261b:	xor    $0x3f,%eax
    261e:	mov    $0x3f,%edx
    2623:	mov    %rbp,%rsi
    2626:	mov    %r12,%rdi
    2629:	sub    %eax,%edx
    262b:	movslq %edx,%rdx
    262e:	add    %rdx,%rdx
    2631:	call   2160 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]>
    2636:	cmp    $0x80,%rbx
    263d:	jle    26a9 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xb9>
    263f:	lea    0x80(%r12),%rbx
    2647:	mov    %r12,%rdi
    264a:	mov    %rbx,%rsi
    264d:	call   2000 <void std::__insertion_sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]>
    2652:	mov    %rbx,%rcx
    2655:	cmp    %rbx,%rbp
    2658:	je     26a4 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xb4>
    265a:	nopw   0x0(%rax,%rax,1)
    2660:	movsd  (%rcx),%xmm1
    2664:	movsd  -0x8(%rcx),%xmm0
    2669:	mov    %rcx,%rdx
    266c:	lea    -0x8(%rcx),%rax
    2670:	comisd %xmm1,%xmm0
    2674:	jbe    2697 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xa7>
    2676:	cs nopw 0x0(%rax,%rax,1)
    2680:	movsd  %xmm0,0x8(%rax)
    2685:	mov    %rax,%rdx
    2688:	movsd  -0x8(%rax),%xmm0
    268d:	sub    $0x8,%rax
    2691:	comisd %xmm1,%xmm0
    2695:	ja     2680 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x90>
    2697:	add    $0x8,%rcx
    269b:	movsd  %xmm1,(%rdx)
    269f:	cmp    %rcx,%rbp
    26a2:	jne    2660 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x70>
    26a4:	pop    %rbx
    26a5:	pop    %rbp
    26a6:	pop    %r12
    26a8:	ret
    26a9:	pop    %rbx
    26aa:	mov    %rbp,%rsi
    26ad:	mov    %r12,%rdi
    26b0:	pop    %rbp
    26b1:	pop    %r12
    26b3:	jmp    2000 <void std::__insertion_sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]>
    26b8:	ret
    26b9:	nopl   0x0(%rax)

00000000000026c0 <apply(Levels&, double, double)>:
    26c0:	endbr64
    26c4:	push   %rbp
    26c5:	push   %rbx
    26c6:	mov    %rdi,%rbx
    26c9:	sub    $0x28,%rsp
    26cd:	movsd  %xmm0,0x8(%rsp)
    26d3:	movsd  %xmm1,0x10(%rsp)
    26d9:	movapd %xmm0,%xmm1
    26dd:	divsd  0xaa3(%rip),%xmm1        # 3188 <_IO_stdin_used+0x188>
    26e5:	movapd %xmm1,%xmm0
    26e9:	movsd  %xmm1,0x18(%rsp)
    26ef:	call   1130 <round@plt>
    26f4:	movsd  0x18(%rsp),%xmm1
    26fa:	subsd  %xmm0,%xmm1
    26fe:	andpd  0xaba(%rip),%xmm1        # 31c0 <_IO_stdin_used+0x1c0>
    2706:	comisd 0xa82(%rip),%xmm1        # 3190 <_IO_stdin_used+0x190>
    270e:	ja     1200 <apply(Levels&, double, double) [clone .cold]>
    2714:	movsd  0x8(%rsp),%xmm0
    271a:	subsd  (%rbx),%xmm0
    271e:	divsd  0xa62(%rip),%xmm0        # 3188 <_IO_stdin_used+0x188>
    2726:	call   1130 <round@plt>
    272b:	movsd  0xa65(%rip),%xmm1        # 3198 <_IO_stdin_used+0x198>
    2733:	comisd %xmm1,%xmm0
    2737:	jae    2778 <apply(Levels&, double, double)+0xb8>
    2739:	cvttsd2si %xmm0,%rax
    273e:	mov    0x8(%rbx),%rdx
    2742:	movsd  0x10(%rsp),%xmm2
    2748:	lea    (%rdx,%rax,8),%rax
    274c:	movsd  (%rax),%xmm0
    2750:	addsd  %xmm2,%xmm0
    2754:	movsd  %xmm0,(%rax)
    2758:	movsd  0x8(%rsp),%xmm0
    275e:	mulsd  %xmm2,%xmm0
    2762:	addsd  0x20(%rbx),%xmm0
    2767:	movsd  %xmm0,0x20(%rbx)
    276c:	add    $0x28,%rsp
    2770:	pop    %rbx
    2771:	pop    %rbp
    2772:	ret
    2773:	nopl   0x0(%rax,%rax,1)
    2778:	subsd  %xmm1,%xmm0
    277c:	cvttsd2si %xmm0,%rax
    2781:	btc    $0x3f,%rax
    2786:	jmp    273e <apply(Levels&, double, double)+0x7e>
    2788:	nopl   0x0(%rax,%rax,1)

0000000000002790 <hot::apply(hot::Levels&, long, long)>:
    2790:	endbr64
    2794:	mov    0x8(%rdi),%rax
    2798:	mov    %rsi,%rcx
    279b:	imul   %rdx,%rsi
    279f:	sub    (%rdi),%rcx
    27a2:	add    %rdx,(%rax,%rcx,8)
    27a6:	add    %rsi,0x20(%rdi)
    27aa:	ret
    27ab:	nopl   0x0(%rax,%rax,1)

00000000000027b0 <k_dbl(Levels&, double const*, double const*, unsigned long)>:
    27b0:	endbr64
    27b4:	test   %rcx,%rcx
    27b7:	je     28e0 <k_dbl(Levels&, double const*, double const*, unsigned long)+0x130>
    27bd:	push   %r15
    27bf:	xor    %r15d,%r15d
    27c2:	push   %r14
    27c4:	mov    %rdi,%r14
    27c7:	push   %r13
    27c9:	movabs $0x8000000000000000,%r13
    27d3:	push   %r12
    27d5:	mov    %rdx,%r12
    27d8:	push   %rbp
    27d9:	mov    %rsi,%rbp
    27dc:	push   %rbx
    27dd:	mov    %rcx,%rbx
    27e0:	sub    $0x28,%rsp
    27e4:	jmp    2832 <k_dbl(Levels&, double const*, double const*, unsigned long)+0x82>
    27e6:	cs nopw 0x0(%rax,%rax,1)
    27f0:	cvttsd2si %xmm0,%rax
    27f5:	mov    0x8(%r14),%rdx
    27f9:	movsd  0x10(%rsp),%xmm2
    27ff:	add    $0x1,%r15
    2803:	lea    (%rdx,%rax,8),%rax
    2807:	movsd  (%rax),%xmm0
    280b:	addsd  %xmm2,%xmm0
    280f:	movsd  %xmm0,(%rax)
    2813:	movsd  0x8(%rsp),%xmm0
    2819:	mulsd  %xmm2,%xmm0
    281d:	addsd  0x20(%r14),%xmm0
    2823:	movsd  %xmm0,0x20(%r14)
    2829:	cmp    %r15,%rbx
    282c:	je     28c8 <k_dbl(Levels&, double const*, double const*, unsigned long)+0x118>
    2832:	movsd  0x0(%rbp,%r15,8),%xmm3
    2839:	movsd  (%r12,%r15,8),%xmm4
    283f:	movapd %xmm3,%xmm1
    2843:	divsd  0x93d(%rip),%xmm1        # 3188 <_IO_stdin_used+0x188>
    284b:	movapd %xmm1,%xmm0
    284f:	movsd  %xmm1,0x18(%rsp)
    2855:	movsd  %xmm4,0x10(%rsp)
    285b:	movsd  %xmm3,0x8(%rsp)
    2861:	call   1130 <round@plt>
    2866:	movsd  0x18(%rsp),%xmm1
    286c:	subsd  %xmm0,%xmm1
    2870:	andpd  0x948(%rip),%xmm1        # 31c0 <_IO_stdin_used+0x1c0>
    2878:	comisd 0x910(%rip),%xmm1        # 3190 <_IO_stdin_used+0x190>
    2880:	ja     1249 <k_dbl(Levels&, double const*, double const*, unsigned long) [clone .cold]>
    2886:	movsd  0x8(%rsp),%xmm0
    288c:	subsd  (%r14),%xmm0
    2891:	divsd  0x8ef(%rip),%xmm0        # 3188 <_IO_stdin_used+0x188>
    2899:	call   1130 <round@plt>
    289e:	comisd 0x8f2(%rip),%xmm0        # 3198 <_IO_stdin_used+0x198>
    28a6:	jb     27f0 <k_dbl(Levels&, double const*, double const*, unsigned long)+0x40>
    28ac:	subsd  0x8e4(%rip),%xmm0        # 3198 <_IO_stdin_used+0x198>
    28b4:	cvttsd2si %xmm0,%rax
    28b9:	xor    %r13,%rax
    28bc:	jmp    27f5 <k_dbl(Levels&, double const*, double const*, unsigned long)+0x45>
    28c1:	nopl   0x0(%rax)
    28c8:	add    $0x28,%rsp
    28cc:	pop    %rbx
    28cd:	pop    %rbp
    28ce:	pop    %r12
    28d0:	pop    %r13
    28d2:	pop    %r14
    28d4:	pop    %r15
    28d6:	ret
    28d7:	nopw   0x0(%rax,%rax,1)
    28e0:	ret
    28e1:	data16 cs nopw 0x0(%rax,%rax,1)
    28ec:	nopl   0x0(%rax)

00000000000028f0 <k_dbl_nocheck(Levels&, double const*, double const*, unsigned long)>:
    28f0:	endbr64
    28f4:	test   %rcx,%rcx
    28f7:	je     29c0 <k_dbl_nocheck(Levels&, double const*, double const*, unsigned long)+0xd0>
    28fd:	push   %r15
    28ff:	mov    %rdx,%r15
    2902:	push   %r14
    2904:	mov    %rdi,%r14
    2907:	push   %r13
    2909:	mov    %rsi,%r13
    290c:	push   %r12
    290e:	movabs $0x8000000000000000,%r12
    2918:	push   %rbp
    2919:	push   %rbx
    291a:	lea    (%rsi,%rcx,8),%rbx
    291e:	sub    $0x8,%rsp
    2922:	mov    0x8(%rdi),%rbp
    2926:	jmp    296d <k_dbl_nocheck(Levels&, double const*, double const*, unsigned long)+0x7d>
    2928:	nopl   0x0(%rax,%rax,1)
    2930:	cvttsd2si %xmm0,%rax
    2935:	lea    0x0(%rbp,%rax,8),%rax
    293a:	add    $0x8,%r13
    293e:	add    $0x8,%r15
    2942:	movsd  (%rax),%xmm0
    2946:	addsd  -0x8(%r15),%xmm0
    294c:	movsd  %xmm0,(%rax)
    2950:	movsd  -0x8(%r13),%xmm0
    2956:	mulsd  -0x8(%r15),%xmm0
    295c:	addsd  0x20(%r14),%xmm0
    2962:	movsd  %xmm0,0x20(%r14)
    2968:	cmp    %r13,%rbx
    296b:	je     29a8 <k_dbl_nocheck(Levels&, double const*, double const*, unsigned long)+0xb8>
    296d:	movsd  0x0(%r13),%xmm0
    2973:	subsd  (%r14),%xmm0
    2978:	divsd  0x808(%rip),%xmm0        # 3188 <_IO_stdin_used+0x188>
    2980:	call   1130 <round@plt>
    2985:	comisd 0x80b(%rip),%xmm0        # 3198 <_IO_stdin_used+0x198>
    298d:	jb     2930 <k_dbl_nocheck(Levels&, double const*, double const*, unsigned long)+0x40>
    298f:	subsd  0x801(%rip),%xmm0        # 3198 <_IO_stdin_used+0x198>
    2997:	cvttsd2si %xmm0,%rax
    299c:	xor    %r12,%rax
    299f:	jmp    2935 <k_dbl_nocheck(Levels&, double const*, double const*, unsigned long)+0x45>
    29a1:	nopl   0x0(%rax)
    29a8:	add    $0x8,%rsp
    29ac:	pop    %rbx
    29ad:	pop    %rbp
    29ae:	pop    %r12
    29b0:	pop    %r13
    29b2:	pop    %r14
    29b4:	pop    %r15
    29b6:	ret
    29b7:	nopw   0x0(%rax,%rax,1)
    29c0:	ret
    29c1:	data16 cs nopw 0x0(%rax,%rax,1)
    29cc:	nopl   0x0(%rax)

00000000000029d0 <k_int(hot::Levels&, long const*, long const*, unsigned long)>:
    29d0:	endbr64
    29d4:	mov    %rdi,%r8
    29d7:	test   %rcx,%rcx
    29da:	je     2a0b <k_int(hot::Levels&, long const*, long const*, unsigned long)+0x3b>
    29dc:	mov    0x8(%rdi),%r11
    29e0:	xor    %eax,%eax
    29e2:	nopw   0x0(%rax,%rax,1)
    29e8:	mov    (%rsi,%rax,8),%r9
    29ec:	mov    (%rdx,%rax,8),%rdi
    29f0:	add    $0x1,%rax
    29f4:	mov    %r9,%r10
    29f7:	sub    (%r8),%r10
    29fa:	add    %rdi,(%r11,%r10,8)
    29fe:	imul   %r9,%rdi
    2a02:	add    %rdi,0x20(%r8)
    2a06:	cmp    %rax,%rcx
    2a09:	jne    29e8 <k_int(hot::Levels&, long const*, long const*, unsigned long)+0x18>
    2a0b:	ret
    2a0c:	nopl   0x0(%rax)

0000000000002a10 <std::vector<double, std::allocator<double> >::~vector()>:
    2a10:	endbr64
    2a14:	mov    (%rdi),%rax
    2a17:	test   %rax,%rax
    2a1a:	je     2a30 <std::vector<double, std::allocator<double> >::~vector()+0x20>
    2a1c:	mov    0x10(%rdi),%rsi
    2a20:	mov    %rax,%rdi
    2a23:	sub    %rax,%rsi
    2a26:	jmp    1190 <operator delete(void*, unsigned long)@plt>
    2a2b:	nopl   0x0(%rax,%rax,1)
    2a30:	ret
    2a31:	cs nopw 0x0(%rax,%rax,1)
    2a3b:	nopl   0x0(%rax,%rax,1)

0000000000002a40 <std::vector<long, std::allocator<long> >::~vector()>:
    2a40:	endbr64
    2a44:	mov    (%rdi),%rax
    2a47:	test   %rax,%rax
    2a4a:	je     2a60 <std::vector<long, std::allocator<long> >::~vector()+0x20>
    2a4c:	mov    0x10(%rdi),%rsi
    2a50:	mov    %rax,%rdi
    2a53:	sub    %rax,%rsi
    2a56:	jmp    1190 <operator delete(void*, unsigned long)@plt>
    2a5b:	nopl   0x0(%rax,%rax,1)
    2a60:	ret
    2a61:	cs nopw 0x0(%rax,%rax,1)
    2a6b:	nopl   0x0(%rax,%rax,1)

0000000000002a70 <std::mersenne_twister_engine<unsigned long, 64ul, 312ul, 156ul, 31ul, 13043109905998158313ul, 29ul, 6148914691236517205ul, 17ul, 8202884508482404352ul, 37ul, 18444473444759240704ul, 43ul, 6364136223846793005ul>::_M_gen_rand()>:
    2a70:	endbr64
    2a74:	movdqa 0x754(%rip),%xmm7        # 31d0 <_IO_stdin_used+0x1d0>
    2a7c:	mov    %rdi,%r9
    2a7f:	mov    %rdi,%rdx
    2a82:	movdqa 0x756(%rip),%xmm6        # 31e0 <_IO_stdin_used+0x1e0>
    2a8a:	movdqa 0x75e(%rip),%xmm5        # 31f0 <_IO_stdin_used+0x1f0>
    2a92:	movdqa 0x766(%rip),%xmm4        # 3200 <_IO_stdin_used+0x200>
    2a9a:	mov    %rdi,%rax
    2a9d:	pxor   %xmm3,%xmm3
    2aa1:	lea    0x4e0(%rdi),%rcx
    2aa8:	nopl   0x0(%rax,%rax,1)
    2ab0:	movdqu (%rax),%xmm0
    2ab4:	movdqu 0x8(%rax),%xmm1
    2ab9:	add    $0x10,%rax
    2abd:	movdqu 0x4d0(%rax),%xmm2
    2ac5:	pand   %xmm6,%xmm1
    2ac9:	pand   %xmm7,%xmm0
    2acd:	por    %xmm1,%xmm0
    2ad1:	movdqa %xmm0,%xmm1
    2ad5:	pand   %xmm5,%xmm0
    2ad9:	psrlq  $0x1,%xmm1
    2ade:	pxor   %xmm2,%xmm1
    2ae2:	movdqa %xmm3,%xmm2
    2ae6:	psubq  %xmm0,%xmm2
    2aea:	pand   %xmm4,%xmm2
    2aee:	movdqa %xmm2,%xmm0
    2af2:	pxor   %xmm1,%xmm0
    2af6:	movups %xmm0,-0x10(%rax)
    2afa:	cmp    %rcx,%rax
    2afd:	jne    2ab0 <std::mersenne_twister_engine<unsigned long, 64ul, 312ul, 156ul, 31ul, 13043109905998158313ul, 29ul, 6148914691236517205ul, 17ul, 8202884508482404352ul, 37ul, 18444473444759240704ul, 43ul, 6364136223846793005ul>::_M_gen_rand()+0x40>
    2aff:	mov    0x4e0(%r9),%rsi
    2b06:	lea    0x4d8(%r9),%r8
    2b0d:	movabs $0xb5026f5aa96619e9,%rdi
    2b17:	nopw   0x0(%rax,%rax,1)
    2b20:	and    $0xffffffff80000000,%rsi
    2b27:	add    $0x8,%rdx
    2b2b:	mov    %rsi,%rcx
    2b2e:	mov    0x4e0(%rdx),%rsi
    2b35:	mov    %rsi,%rax
    2b38:	and    $0x7fffffff,%eax
    2b3d:	or     %rcx,%rax
    2b40:	mov    %rax,%rcx
    2b43:	and    $0x1,%eax
    2b46:	neg    %rax
    2b49:	shr    $1,%rcx
    2b4c:	xor    -0x8(%rdx),%rcx
    2b50:	and    %rdi,%rax
    2b53:	xor    %rcx,%rax
    2b56:	mov    %rax,0x4d8(%rdx)
    2b5d:	cmp    %r8,%rdx
    2b60:	jne    2b20 <std::mersenne_twister_engine<unsigned long, 64ul, 312ul, 156ul, 31ul, 13043109905998158313ul, 29ul, 6148914691236517205ul, 17ul, 8202884508482404352ul, 37ul, 18444473444759240704ul, 43ul, 6364136223846793005ul>::_M_gen_rand()+0xb0>
    2b62:	mov    0x9b8(%r9),%rax
    2b69:	mov    (%r9),%rdx
    2b6c:	movq   $0x0,0x9c0(%r9)
    2b77:	and    $0x7fffffff,%edx
    2b7d:	and    $0xffffffff80000000,%rax
    2b83:	or     %rdx,%rax
    2b86:	mov    %rax,%rdx
    2b89:	and    $0x1,%eax
    2b8c:	neg    %rax
    2b8f:	shr    $1,%rdx
    2b92:	xor    0x4d8(%r9),%rdx
    2b99:	and    %rdi,%rax
    2b9c:	xor    %rdx,%rax
    2b9f:	mov    %rax,0x9b8(%r9)
    2ba6:	ret
    2ba7:	nopw   0x0(%rax,%rax,1)

0000000000002bb0 <std::mersenne_twister_engine<unsigned long, 64ul, 312ul, 156ul, 31ul, 13043109905998158313ul, 29ul, 6148914691236517205ul, 17ul, 8202884508482404352ul, 37ul, 18444473444759240704ul, 43ul, 6364136223846793005ul>::operator()()>:
    2bb0:	endbr64
    2bb4:	mov    0x9c0(%rdi),%rax
    2bbb:	push   %rbx
    2bbc:	mov    %rdi,%rbx
    2bbf:	cmp    $0x137,%rax
    2bc5:	ja     2c30 <std::mersenne_twister_engine<unsigned long, 64ul, 312ul, 156ul, 31ul, 13043109905998158313ul, 29ul, 6148914691236517205ul, 17ul, 8202884508482404352ul, 37ul, 18444473444759240704ul, 43ul, 6364136223846793005ul>::operator()()+0x80>
    2bc7:	movabs $0x5555555555555555,%rcx
    2bd1:	lea    0x1(%rax),%rdx
    2bd5:	mov    (%rbx,%rax,8),%rax
    2bd9:	mov    %rdx,0x9c0(%rbx)
    2be0:	pop    %rbx
    2be1:	mov    %rax,%rdx
    2be4:	shr    $0x1d,%rdx
    2be8:	and    %rcx,%rdx
    2beb:	movabs $0x71d67fffeda60000,%rcx
    2bf5:	xor    %rax,%rdx
    2bf8:	mov    %rdx,%rax
    2bfb:	shl    $0x11,%rax
    2bff:	and    %rcx,%rax
    2c02:	movabs $0xfff7eee000000000,%rcx
    2c0c:	xor    %rdx,%rax
    2c0f:	mov    %rax,%rdx
    2c12:	shl    $0x25,%rdx
    2c16:	and    %rcx,%rdx
    2c19:	xor    %rax,%rdx
    2c1c:	mov    %rdx,%rax
    2c1f:	shr    $0x2b,%rax
    2c23:	xor    %rdx,%rax
    2c26:	ret
    2c27:	nopw   0x0(%rax,%rax,1)
    2c30:	call   2a70 <std::mersenne_twister_engine<unsigned long, 64ul, 312ul, 156ul, 31ul, 13043109905998158313ul, 29ul, 6148914691236517205ul, 17ul, 8202884508482404352ul, 37ul, 18444473444759240704ul, 43ul, 6364136223846793005ul>::_M_gen_rand()>
    2c35:	mov    0x9c0(%rbx),%rax
    2c3c:	jmp    2bc7 <std::mersenne_twister_engine<unsigned long, 64ul, 312ul, 156ul, 31ul, 13043109905998158313ul, 29ul, 6148914691236517205ul, 17ul, 8202884508482404352ul, 37ul, 18444473444759240704ul, 43ul, 6364136223846793005ul>::operator()()+0x17>

Disassembly of section .fini:

0000000000002c40 <_fini>:
    2c40:	endbr64
    2c44:	sub    $0x8,%rsp
    2c48:	add    $0x8,%rsp
    2c4c:	ret
