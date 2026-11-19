
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
    1020:	push   0x3f52(%rip)        # 4f78 <_GLOBAL_OFFSET_TABLE_+0x8>
    1026:	jmp    *0x3f54(%rip)        # 4f80 <_GLOBAL_OFFSET_TABLE_+0x10>
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

Disassembly of section .plt.got:

00000000000010d0 <__cxa_finalize@plt>:
    10d0:	endbr64
    10d4:	jmp    *0x3efe(%rip)        # 4fd8 <__cxa_finalize@GLIBC_2.2.5>
    10da:	nopw   0x0(%rax,%rax,1)

Disassembly of section .plt.sec:

00000000000010e0 <__printf_chk@plt>:
    10e0:	endbr64
    10e4:	jmp    *0x3e9e(%rip)        # 4f88 <__printf_chk@GLIBC_2.3.4>
    10ea:	nopw   0x0(%rax,%rax,1)

00000000000010f0 <std::__throw_length_error(char const*)@plt>:
    10f0:	endbr64
    10f4:	jmp    *0x3e96(%rip)        # 4f90 <std::__throw_length_error(char const*)@GLIBCXX_3.4>
    10fa:	nopw   0x0(%rax,%rax,1)

0000000000001100 <operator new(unsigned long)@plt>:
    1100:	endbr64
    1104:	jmp    *0x3e8e(%rip)        # 4f98 <operator new(unsigned long)@GLIBCXX_3.4>
    110a:	nopw   0x0(%rax,%rax,1)

0000000000001110 <operator delete(void*, unsigned long)@plt>:
    1110:	endbr64
    1114:	jmp    *0x3e86(%rip)        # 4fa0 <operator delete(void*, unsigned long)@CXXABI_1.3.9>
    111a:	nopw   0x0(%rax,%rax,1)

0000000000001120 <__stack_chk_fail@plt>:
    1120:	endbr64
    1124:	jmp    *0x3e7e(%rip)        # 4fa8 <__stack_chk_fail@GLIBC_2.4>
    112a:	nopw   0x0(%rax,%rax,1)

0000000000001130 <exit@plt>:
    1130:	endbr64
    1134:	jmp    *0x3e76(%rip)        # 4fb0 <exit@GLIBC_2.2.5>
    113a:	nopw   0x0(%rax,%rax,1)

0000000000001140 <std::chrono::_V2::steady_clock::now()@plt>:
    1140:	endbr64
    1144:	jmp    *0x3e6e(%rip)        # 4fb8 <std::chrono::_V2::steady_clock::now()@GLIBCXX_3.4.19>
    114a:	nopw   0x0(%rax,%rax,1)

0000000000001150 <memmove@plt>:
    1150:	endbr64
    1154:	jmp    *0x3e66(%rip)        # 4fc0 <memmove@GLIBC_2.2.5>
    115a:	nopw   0x0(%rax,%rax,1)

0000000000001160 <__fprintf_chk@plt>:
    1160:	endbr64
    1164:	jmp    *0x3e5e(%rip)        # 4fc8 <__fprintf_chk@GLIBC_2.3.4>
    116a:	nopw   0x0(%rax,%rax,1)

0000000000001170 <_Unwind_Resume@plt>:
    1170:	endbr64
    1174:	jmp    *0x3e56(%rip)        # 4fd0 <_Unwind_Resume@GCC_3.0>
    117a:	nopw   0x0(%rax,%rax,1)

Disassembly of section .text:

0000000000001180 <hot::on_bad(Tick const&) [clone .isra.0]>:
    1180:	mov    %edi,%ecx
    1182:	mov    0x3e97(%rip),%rdi        # 5020 <stderr@GLIBC_2.2.5>
    1189:	mov    $0x2,%esi
    118e:	xor    %eax,%eax
    1190:	lea    0x1e6d(%rip),%rdx        # 3004 <_IO_stdin_used+0x4>
    1197:	jmp    1160 <__fprintf_chk@plt>

000000000000119c <k_hot(Tick const*, unsigned long, long) [clone .cold]>:
    119c:	mov    %rcx,0x18(%rsp)
    11a1:	mov    %r9,0x10(%rsp)
    11a6:	mov    %r8,0x8(%rsp)
    11ab:	mov    %rsi,(%rsp)
    11af:	call   1180 <hot::on_bad(Tick const&) [clone .isra.0]>
    11b4:	mov    (%rsp),%rsi
    11b8:	mov    0x8(%rsp),%r8
    11bd:	mov    0x10(%rsp),%r9
    11c2:	mov    0x18(%rsp),%rcx
    11c7:	add    $0x1,%rsi
    11cb:	jmp    2ae9 <k_hot(Tick const*, unsigned long, long)+0x69>

00000000000011d0 <k_bc(Tick const*, unsigned long, int) [clone .cold]>:
    11d0:	mov    %r8,0x18(%rsp)
    11d5:	mov    %rdx,0x10(%rsp)
    11da:	mov    %rcx,0x8(%rsp)
    11df:	mov    %rsi,(%rsp)
    11e3:	call   1180 <hot::on_bad(Tick const&) [clone .isra.0]>
    11e8:	mov    0x18(%rsp),%r8
    11ed:	mov    (%rsp),%rsi
    11f1:	mov    0x8(%rsp),%rcx
    11f6:	mov    0x10(%rsp),%rdx
    11fb:	add    $0x1,%r8
    11ff:	jmp    2b8e <k_bc(Tick const*, unsigned long, int)+0x4e>

0000000000001204 <k_lut(Tick const*, unsigned long, int) [clone .cold]>:
    1204:	mov    %ecx,0x1c(%rsp)
    1208:	add    $0x1,%r12
    120c:	mov    %rdx,0x10(%rsp)
    1211:	mov    %rsi,0x8(%rsp)
    1216:	call   1180 <hot::on_bad(Tick const&) [clone .isra.0]>
    121b:	mov    0x8(%rsp),%rsi
    1220:	mov    0x10(%rsp),%rdx
    1225:	mov    0x1c(%rsp),%ecx
    1229:	jmp    2c65 <k_lut(Tick const*, unsigned long, int)+0x65>

000000000000122e <main.cold>:
    122e:	lea    0x90(%rsp),%rdi
    1236:	call   2ea0 <std::vector<double, std::allocator<double> >::~vector()>
    123b:	mov    0x28(%rsp),%rdi
    1240:	mov    $0x40000,%esi
    1245:	call   1110 <operator delete(void*, unsigned long)@plt>
    124a:	mov    0xbf8(%rsp),%rax
    1252:	sub    %fs:0x28,%rax
    125b:	jne    1271 <main.cold+0x43>
    125d:	mov    %rbx,%rdi
    1260:	call   1170 <_Unwind_Resume@plt>
    1265:	mov    0x68(%rsp),%rdi
    126a:	call   2ea0 <std::vector<double, std::allocator<double> >::~vector()>
    126f:	jmp    123b <main.cold+0xd>
    1271:	call   1120 <__stack_chk_fail@plt>
    1276:	mov    0x68(%rsp),%rdi
    127b:	call   2ea0 <std::vector<double, std::allocator<double> >::~vector()>
    1280:	jmp    123b <main.cold+0xd>
    1282:	mov    0x68(%rsp),%rdi
    1287:	call   2ea0 <std::vector<double, std::allocator<double> >::~vector()>
    128c:	jmp    123b <main.cold+0xd>
    128e:	xchg   %ax,%ax

0000000000001290 <main>:
    1290:	endbr64
    1294:	push   %r15
    1296:	mov    $0x1,%ecx
    129b:	movabs $0x5851f42d4c957f2d,%rsi
    12a5:	push   %r14
    12a7:	push   %r13
    12a9:	push   %r12
    12ab:	push   %rbp
    12ac:	push   %rbx
    12ad:	sub    $0xc08,%rsp
    12b4:	mov    %fs:0x28,%rax
    12bd:	mov    %rax,0xbf8(%rsp)
    12c5:	xor    %eax,%eax
    12c7:	mov    $0x2a,%eax
    12cc:	lea    0x230(%rsp),%r15
    12d4:	movq   $0x2a,0x230(%rsp)
    12e0:	mov    %rax,%rdx
    12e3:	nopl   0x0(%rax,%rax,1)
    12e8:	mov    %rdx,%rax
    12eb:	shr    $0x3e,%rax
    12ef:	xor    %rdx,%rax
    12f2:	imul   %rsi,%rax
    12f6:	lea    (%rax,%rcx,1),%rdx
    12fa:	mov    %rdx,(%r15,%rcx,8)
    12fe:	add    $0x1,%rcx
    1302:	cmp    $0x138,%rcx
    1309:	jne    12e8 <main+0x58>
    130b:	lea    0x1d4e(%rip),%rax        # 3060 <_IO_stdin_used+0x60>
    1312:	movq   $0x138,0xbf0(%rsp)
    131e:	mov    %rax,0x200(%rsp)
    1326:	lea    0x1d63(%rip),%rax        # 3090 <_IO_stdin_used+0x90>
    132d:	mov    %rax,0x210(%rsp)
    1335:	lea    0x1d7c(%rip),%rax        # 30b8 <_IO_stdin_used+0xb8>
    133c:	mov    %rax,0x220(%rsp)
    1344:	lea    0x200(%rsp),%rax
    134c:	mov    %rax,0x58(%rsp)
    1351:	lea    0x110(%rsp),%rax
    1359:	mov    %rax,0x60(%rsp)
    135e:	lea    0x70(%rsp),%rax
    1363:	movl   $0x0,0x208(%rsp)
    136e:	movl   $0x1,0x218(%rsp)
    1379:	movl   $0x2,0x228(%rsp)
    1384:	mov    %rax,0x10(%rsp)
    1389:	mov    0x58(%rsp),%rax
    138e:	mov    $0x40000,%edi
    1393:	mov    (%rax),%rbx
    1396:	mov    0x8(%rax),%r14d
    139a:	call   1100 <operator new(unsigned long)@plt>
    139f:	lea    0x40000(%rax),%rdx
    13a6:	mov    %rax,0x28(%rsp)
    13ab:	mov    %rax,%rcx
    13ae:	mov    %rdx,0x80(%rsp)
    13b6:	mov    %rax,0x70(%rsp)
    13bb:	lea    0x10(%rax),%rax
    13bf:	movq   $0x0,-0x10(%rax)
    13c7:	movl   $0x0,-0x8(%rax)
    13ce:	movb   $0x0,-0x4(%rax)
    13d2:	nopw   0x0(%rax,%rax,1)
    13d8:	movdqu (%rcx),%xmm7
    13dc:	add    $0x10,%rax
    13e0:	movups %xmm7,-0x10(%rax)
    13e4:	cmp    %rax,%rdx
    13e7:	jne    13d8 <main+0x148>
    13e9:	mov    %rdx,0x78(%rsp)
    13ee:	mov    0x28(%rsp),%rbp
    13f3:	xor    %r13d,%r13d
    13f6:	xor    %r12d,%r12d
    13f9:	mov    %rbx,0x8(%rsp)
    13fe:	jmp    14e5 <main+0x255>
    1403:	nopl   0x0(%rax,%rax,1)
    1408:	mov    %r13,%r12
    140b:	mov    $0x1,%ebx
    1410:	shr    $0x8,%r12
    1414:	and    $0x1,%r12d
    1418:	mov    %r15,%rdi
    141b:	call   2e10 <std::mersenne_twister_engine<unsigned long, 64ul, 312ul, 156ul, 31ul, 13043109905998158313ul, 29ul, 6148914691236517205ul, 17ul, 8202884508482404352ul, 37ul, 18444473444759240704ul, 43ul, 6364136223846793005ul>::operator()()>
    1420:	mov    %r15,%rdi
    1423:	mov    %rax,%rdx
    1426:	mov    %rax,%rcx
    1429:	movabs $0x28f5c28f5c28f5c3,%rax
    1433:	shr    $0x2,%rdx
    1437:	mul    %rdx
    143a:	mov    %rdx,%rax
    143d:	and    $0xfffffffffffffffc,%rdx
    1441:	shr    $0x2,%rax
    1445:	add    %rax,%rdx
    1448:	mov    %rcx,%rax
    144b:	lea    (%rdx,%rdx,4),%rdx
    144f:	shl    $0x2,%rdx
    1453:	sub    %rdx,%rax
    1456:	cmp    %eax,%ebx
    1458:	jle    1550 <main+0x2c0>
    145e:	call   2e10 <std::mersenne_twister_engine<unsigned long, 64ul, 312ul, 156ul, 31ul, 13043109905998158313ul, 29ul, 6148914691236517205ul, 17ul, 8202884508482404352ul, 37ul, 18444473444759240704ul, 43ul, 6364136223846793005ul>::operator()()>
    1463:	mov    %rax,%rdx
    1466:	mov    %rax,%rbx
    1469:	movabs $0x20c49ba5e353f7cf,%rax
    1473:	shr    $0x3,%rdx
    1477:	mul    %rdx
    147a:	shr    $0x4,%rdx
    147e:	imul   $0x3e8,%rdx,%rdx
    1485:	sub    %rdx,%rbx
    1488:	add    $0x1f4,%ebx
    148e:	mov    %r15,%rdi
    1491:	add    $0x1,%r13
    1495:	add    $0x10,%rbp
    1499:	call   2e10 <std::mersenne_twister_engine<unsigned long, 64ul, 312ul, 156ul, 31ul, 13043109905998158313ul, 29ul, 6148914691236517205ul, 17ul, 8202884508482404352ul, 37ul, 18444473444759240704ul, 43ul, 6364136223846793005ul>::operator()()>
    149e:	mov    %ebx,-0x8(%rbp)
    14a1:	mov    %rax,%rdx
    14a4:	mov    %rax,%rcx
    14a7:	mov    %r12b,-0x4(%rbp)
    14ab:	movabs $0xa3d70a3d70a3d70b,%rax
    14b5:	shr    $1,%rdx
    14b8:	mul    %rdx
    14bb:	shr    $0x4,%rdx
    14bf:	lea    (%rdx,%rdx,4),%rax
    14c3:	lea    (%rax,%rax,4),%rax
    14c7:	add    %rax,%rax
    14ca:	sub    %rax,%rcx
    14cd:	add    $0x2710,%rcx
    14d4:	mov    %rcx,-0x10(%rbp)
    14d8:	cmp    $0x4000,%r13
    14df:	je     15a1 <main+0x311>
    14e5:	test   %r14d,%r14d
    14e8:	je     1408 <main+0x178>
    14ee:	cmp    $0x1,%r14d
    14f2:	jne    1580 <main+0x2f0>
    14f8:	mov    %r15,%rdi
    14fb:	mov    $0xa,%ebx
    1500:	call   2e10 <std::mersenne_twister_engine<unsigned long, 64ul, 312ul, 156ul, 31ul, 13043109905998158313ul, 29ul, 6148914691236517205ul, 17ul, 8202884508482404352ul, 37ul, 18444473444759240704ul, 43ul, 6364136223846793005ul>::operator()()>
    1505:	mov    %rax,%rdx
    1508:	mov    %rax,%rcx
    150b:	movabs $0x28f5c28f5c28f5c3,%rax
    1515:	shr    $0x2,%rdx
    1519:	mul    %rdx
    151c:	mov    %rdx,%rax
    151f:	and    $0xfffffffffffffffc,%rdx
    1523:	shr    $0x2,%rax
    1527:	add    %rax,%rdx
    152a:	lea    (%rdx,%rdx,4),%rax
    152e:	shl    $0x2,%rax
    1532:	sub    %rax,%rcx
    1535:	mov    %r12d,%eax
    1538:	xor    $0x1,%r12d
    153c:	cmp    $0x4f,%rcx
    1540:	cmovbe %eax,%r12d
    1544:	jmp    1418 <main+0x188>
    1549:	nopl   0x0(%rax)
    1550:	call   2e10 <std::mersenne_twister_engine<unsigned long, 64ul, 312ul, 156ul, 31ul, 13043109905998158313ul, 29ul, 6148914691236517205ul, 17ul, 8202884508482404352ul, 37ul, 18444473444759240704ul, 43ul, 6364136223846793005ul>::operator()()>
    1555:	mov    %rax,%rbx
    1558:	movabs $0x8355ace3c897db1,%rax
    1562:	mul    %rbx
    1565:	shr    $0x4,%rdx
    1569:	imul   $0x1f3,%rdx,%rdx
    1570:	sub    %rdx,%rbx
    1573:	add    $0x1,%ebx
    1576:	jmp    148e <main+0x1fe>
    157b:	nopl   0x0(%rax,%rax,1)
    1580:	cmp    $0x2,%r14d
    1584:	je     1590 <main+0x300>
    1586:	mov    $0x32,%ebx
    158b:	jmp    1418 <main+0x188>
    1590:	mov    %r15,%rdi
    1593:	call   2e10 <std::mersenne_twister_engine<unsigned long, 64ul, 312ul, 156ul, 31ul, 13043109905998158313ul, 29ul, 6148914691236517205ul, 17ul, 8202884508482404352ul, 37ul, 18444473444759240704ul, 43ul, 6364136223846793005ul>::operator()()>
    1598:	mov    %eax,%r12d
    159b:	and    $0x1,%r12d
    159f:	jmp    1586 <main+0x2f6>
    15a1:	mov    0x10(%rsp),%rsi
    15a6:	mov    0x60(%rsp),%rdi
    15ab:	mov    $0x1f4,%edx
    15b0:	mov    0x8(%rsp),%rbx
    15b5:	call   2990 <scan(std::vector<Tick, std::allocator<Tick> > const&, int)>
    15ba:	mov    %rbx,%rdx
    15bd:	lea    0x1a5d(%rip),%rsi        # 3021 <_IO_stdin_used+0x21>
    15c4:	mov    $0x2,%edi
    15c9:	xor    %eax,%eax
    15cb:	call   10e0 <__printf_chk@plt>
    15d0:	lea    0x140(%rsp),%rax
    15d8:	pxor   %xmm0,%xmm0
    15dc:	mov    $0x65,%r12d
    15e2:	movq   $0x0,0xa0(%rsp)
    15ee:	mov    %rax,0x18(%rsp)
    15f3:	movaps %xmm0,0x90(%rsp)
    15fb:	nopl   0x0(%rax,%rax,1)
    1600:	call   1140 <std::chrono::_V2::steady_clock::now()@plt>
    1605:	mov    0x10(%rsp),%rsi
    160a:	mov    0x18(%rsp),%rdi
    160f:	mov    $0x1f4,%edx
    1614:	mov    %rax,%rbx
    1617:	call   2a40 <k_general(std::vector<Tick, std::allocator<Tick> > const&, int)>
    161c:	call   1140 <std::chrono::_V2::steady_clock::now()@plt>
    1621:	mov    0x110(%rsp),%r14
    1629:	cmp    %r14,0x140(%rsp)
    1631:	je     1660 <main+0x3d0>
    1633:	lea    0x19d6(%rip),%rdx        # 3010 <_IO_stdin_used+0x10>
    163a:	lea    0x19d7(%rip),%rsi        # 3018 <_IO_stdin_used+0x18>
    1641:	mov    $0x2,%edi
    1646:	xor    %eax,%eax
    1648:	call   10e0 <__printf_chk@plt>
    164d:	mov    $0x1,%edi
    1652:	call   1130 <exit@plt>
    1657:	nopw   0x0(%rax,%rax,1)
    1660:	mov    0x118(%rsp),%rsi
    1668:	mov    %rsi,0x20(%rsp)
    166d:	cmp    %rsi,0x148(%rsp)
    1675:	jne    1633 <main+0x3a3>
    1677:	mov    0x120(%rsp),%rdi
    167f:	mov    %rdi,0x30(%rsp)
    1684:	cmp    %rdi,0x150(%rsp)
    168c:	jne    1633 <main+0x3a3>
    168e:	mov    0x128(%rsp),%rdi
    1696:	mov    0x130(%rsp),%rsi
    169e:	mov    %rdi,0x48(%rsp)
    16a3:	mov    %rsi,0x40(%rsp)
    16a8:	cmp    %rsi,0x160(%rsp)
    16b0:	jne    1633 <main+0x3a3>
    16b2:	cmp    %rdi,0x158(%rsp)
    16ba:	jne    1633 <main+0x3a3>
    16c0:	sub    %rbx,%rax
    16c3:	pxor   %xmm0,%xmm0
    16c7:	mov    0x98(%rsp),%rbx
    16cf:	mov    0xa0(%rsp),%r13
    16d7:	cvtsi2sd %rax,%xmm0
    16dc:	mulsd  0x1a7c(%rip),%xmm0        # 3160 <_IO_stdin_used+0x160>
    16e4:	movsd  %xmm0,0x8(%rsp)
    16ea:	cmp    %r13,%rbx
    16ed:	je     17f8 <main+0x568>
    16f3:	movsd  0x8(%rsp),%xmm3
    16f9:	add    $0x8,%rbx
    16fd:	movsd  %xmm3,-0x8(%rbx)
    1702:	mov    %rbx,0x98(%rsp)
    170a:	sub    $0x1,%r12d
    170e:	jne    1600 <main+0x370>
    1714:	mov    0x90(%rsp),%rbx
    171c:	mov    0x98(%rsp),%rsi
    1724:	mov    %rbx,%rdi
    1727:	call   2770 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]>
    172c:	movsd  (%rbx),%xmm1
    1730:	movsd  0x190(%rbx),%xmm0
    1738:	lea    0x18d1(%rip),%rdx        # 3010 <_IO_stdin_used+0x10>
    173f:	movsd  0x318(%rbx),%xmm2
    1747:	mov    $0x2,%edi
    174c:	mov    $0x3,%eax
    1751:	lea    0x1988(%rip),%rsi        # 30e0 <_IO_stdin_used+0xe0>
    1758:	call   10e0 <__printf_chk@plt>
    175d:	mov    0xa0(%rsp),%rsi
    1765:	mov    %rbx,%rdi
    1768:	mov    $0x65,%r12d
    176e:	sub    %rbx,%rsi
    1771:	call   1110 <operator delete(void*, unsigned long)@plt>
    1776:	lea    0xb0(%rsp),%rdi
    177e:	xor    %eax,%eax
    1780:	mov    $0x6,%ecx
    1785:	mov    %rdi,0x68(%rsp)
    178a:	rep stos %eax,%es:(%rdi)
    178c:	lea    0x170(%rsp),%rax
    1794:	mov    %rax,0x18(%rsp)
    1799:	nopl   0x0(%rax)
    17a0:	call   1140 <std::chrono::_V2::steady_clock::now()@plt>
    17a5:	mov    0x28(%rsp),%rsi
    17aa:	mov    0x18(%rsp),%rdi
    17af:	mov    $0x1f4,%ecx
    17b4:	mov    $0x4000,%edx
    17b9:	mov    %rax,%rbx
    17bc:	call   2a80 <k_hot(Tick const*, unsigned long, long)>
    17c1:	call   1140 <std::chrono::_V2::steady_clock::now()@plt>
    17c6:	cmp    0x170(%rsp),%r14
    17ce:	je     1930 <main+0x6a0>
    17d4:	lea    0x1864(%rip),%rdx        # 303f <_IO_stdin_used+0x3f>
    17db:	lea    0x1836(%rip),%rsi        # 3018 <_IO_stdin_used+0x18>
    17e2:	mov    $0x2,%edi
    17e7:	xor    %eax,%eax
    17e9:	call   10e0 <__printf_chk@plt>
    17ee:	jmp    164d <main+0x3bd>
    17f3:	nopl   0x0(%rax,%rax,1)
    17f8:	mov    0x90(%rsp),%rbp
    1800:	movabs $0xfffffffffffffff,%rax
    180a:	sub    %rbp,%rbx
    180d:	mov    %rbx,%rdx
    1810:	sar    $0x3,%rdx
    1814:	cmp    %rax,%rdx
    1817:	je     2124 <main+0xe94>
    181d:	cmp    %rbp,%r13
    1820:	je     18d8 <main+0x648>
    1826:	lea    (%rdx,%rdx,1),%rax
    182a:	cmp    %rdx,%rax
    182d:	jb     1918 <main+0x688>
    1833:	xor    %r8d,%r8d
    1836:	xor    %ecx,%ecx
    1838:	test   %rax,%rax
    183b:	jne    1bd3 <main+0x943>
    1841:	movsd  0x8(%rsp),%xmm6
    1847:	lea    0x8(%rcx,%rbx,1),%r9
    184c:	movsd  %xmm6,(%rcx,%rbx,1)
    1851:	test   %rbx,%rbx
    1854:	jg     1880 <main+0x5f0>
    1856:	test   %rbp,%rbp
    1859:	jne    18a5 <main+0x615>
    185b:	mov    %rcx,0x90(%rsp)
    1863:	mov    %r9,0x98(%rsp)
    186b:	mov    %r8,0xa0(%rsp)
    1873:	jmp    170a <main+0x47a>
    1878:	nopl   0x0(%rax,%rax,1)
    1880:	mov    %rcx,%rdi
    1883:	mov    %rbx,%rdx
    1886:	mov    %rbp,%rsi
    1889:	mov    %r9,0x38(%rsp)
    188e:	mov    %r8,0x8(%rsp)
    1893:	call   1150 <memmove@plt>
    1898:	mov    0x8(%rsp),%r8
    189d:	mov    0x38(%rsp),%r9
    18a2:	mov    %rax,%rcx
    18a5:	mov    %r13,%rsi
    18a8:	mov    %rbp,%rdi
    18ab:	mov    %r9,0x50(%rsp)
    18b0:	sub    %rbp,%rsi
    18b3:	mov    %r8,0x38(%rsp)
    18b8:	mov    %rcx,0x8(%rsp)
    18bd:	call   1110 <operator delete(void*, unsigned long)@plt>
    18c2:	mov    0x50(%rsp),%r9
    18c7:	mov    0x38(%rsp),%r8
    18cc:	mov    0x8(%rsp),%rcx
    18d1:	jmp    185b <main+0x5cb>
    18d3:	nopl   0x0(%rax,%rax,1)
    18d8:	add    $0x1,%rdx
    18dc:	jb     1918 <main+0x688>
    18de:	movabs $0xfffffffffffffff,%rax
    18e8:	cmp    %rax,%rdx
    18eb:	cmovbe %rdx,%rax
    18ef:	shl    $0x3,%rax
    18f3:	mov    %rax,0x38(%rsp)
    18f8:	mov    0x38(%rsp),%rdi
    18fd:	call   1100 <operator new(unsigned long)@plt>
    1902:	mov    0x38(%rsp),%r8
    1907:	mov    %rax,%rcx
    190a:	add    %rax,%r8
    190d:	jmp    1841 <main+0x5b1>
    1912:	nopw   0x0(%rax,%rax,1)
    1918:	movabs $0x7ffffffffffffff8,%rax
    1922:	mov    %rax,0x38(%rsp)
    1927:	jmp    18f8 <main+0x668>
    1929:	nopl   0x0(%rax)
    1930:	mov    0x20(%rsp),%rsi
    1935:	cmp    0x178(%rsp),%rsi
    193d:	jne    17d4 <main+0x544>
    1943:	mov    0x30(%rsp),%rsi
    1948:	cmp    0x180(%rsp),%rsi
    1950:	jne    17d4 <main+0x544>
    1956:	mov    0x40(%rsp),%rsi
    195b:	cmp    %rsi,0x190(%rsp)
    1963:	jne    17d4 <main+0x544>
    1969:	mov    0x48(%rsp),%rsi
    196e:	cmp    %rsi,0x188(%rsp)
    1976:	jne    17d4 <main+0x544>
    197c:	sub    %rbx,%rax
    197f:	pxor   %xmm0,%xmm0
    1983:	mov    0xb8(%rsp),%rbx
    198b:	mov    0xc0(%rsp),%r13
    1993:	cvtsi2sd %rax,%xmm0
    1998:	mulsd  0x17c0(%rip),%xmm0        # 3160 <_IO_stdin_used+0x160>
    19a0:	movsd  %xmm0,0x8(%rsp)
    19a6:	cmp    %r13,%rbx
    19a9:	je     1ab0 <main+0x820>
    19af:	movsd  0x8(%rsp),%xmm4
    19b5:	add    $0x8,%rbx
    19b9:	movsd  %xmm4,-0x8(%rbx)
    19be:	mov    %rbx,0xb8(%rsp)
    19c6:	sub    $0x1,%r12d
    19ca:	jne    17a0 <main+0x510>
    19d0:	mov    0xb0(%rsp),%rbx
    19d8:	mov    0xb8(%rsp),%rsi
    19e0:	mov    %rbx,%rdi
    19e3:	call   2770 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]>
    19e8:	movsd  (%rbx),%xmm1
    19ec:	movsd  0x190(%rbx),%xmm0
    19f4:	lea    0x1644(%rip),%rdx        # 303f <_IO_stdin_used+0x3f>
    19fb:	movsd  0x318(%rbx),%xmm2
    1a03:	mov    $0x2,%edi
    1a08:	mov    $0x3,%eax
    1a0d:	lea    0x16cc(%rip),%rsi        # 30e0 <_IO_stdin_used+0xe0>
    1a14:	call   10e0 <__printf_chk@plt>
    1a19:	mov    0xc0(%rsp),%rsi
    1a21:	mov    %rbx,%rdi
    1a24:	mov    $0x65,%ebp
    1a29:	sub    %rbx,%rsi
    1a2c:	call   1110 <operator delete(void*, unsigned long)@plt>
    1a31:	lea    0xd0(%rsp),%rdi
    1a39:	xor    %eax,%eax
    1a3b:	mov    $0x6,%ecx
    1a40:	mov    %rdi,0x68(%rsp)
    1a45:	rep stos %eax,%es:(%rdi)
    1a47:	lea    0x1a0(%rsp),%rax
    1a4f:	mov    %rax,0x18(%rsp)
    1a54:	nopl   0x0(%rax)
    1a58:	call   1140 <std::chrono::_V2::steady_clock::now()@plt>
    1a5d:	mov    0x28(%rsp),%rsi
    1a62:	mov    0x18(%rsp),%rdi
    1a67:	mov    $0x1f4,%ecx
    1a6c:	mov    $0x4000,%edx
    1a71:	mov    %rax,%rbx
    1a74:	call   2b40 <k_bc(Tick const*, unsigned long, int)>
    1a79:	call   1140 <std::chrono::_V2::steady_clock::now()@plt>
    1a7e:	cmp    0x1a0(%rsp),%r14
    1a86:	je     1bf8 <main+0x968>
    1a8c:	lea    0x15b7(%rip),%rdx        # 304a <_IO_stdin_used+0x4a>
    1a93:	lea    0x157e(%rip),%rsi        # 3018 <_IO_stdin_used+0x18>
    1a9a:	mov    $0x2,%edi
    1a9f:	xor    %eax,%eax
    1aa1:	call   10e0 <__printf_chk@plt>
    1aa6:	jmp    164d <main+0x3bd>
    1aab:	nopl   0x0(%rax,%rax,1)
    1ab0:	mov    0xb0(%rsp),%rbp
    1ab8:	movabs $0xfffffffffffffff,%rsi
    1ac2:	sub    %rbp,%rbx
    1ac5:	mov    %rbx,%rax
    1ac8:	sar    $0x3,%rax
    1acc:	cmp    %rsi,%rax
    1acf:	je     2181 <main+0xef1>
    1ad5:	cmp    %rbp,%r13
    1ad8:	je     1b88 <main+0x8f8>
    1ade:	lea    (%rax,%rax,1),%rdx
    1ae2:	cmp    %rax,%rdx
    1ae5:	jb     1bc2 <main+0x932>
    1aeb:	xor    %r8d,%r8d
    1aee:	xor    %ecx,%ecx
    1af0:	test   %rdx,%rdx
    1af3:	jne    20dc <main+0xe4c>
    1af9:	movsd  0x8(%rsp),%xmm2
    1aff:	lea    0x8(%rcx,%rbx,1),%r9
    1b04:	movsd  %xmm2,(%rcx,%rbx,1)
    1b09:	test   %rbx,%rbx
    1b0c:	jg     1b30 <main+0x8a0>
    1b0e:	test   %rbp,%rbp
    1b11:	jne    1b55 <main+0x8c5>
    1b13:	mov    %rcx,0xb0(%rsp)
    1b1b:	mov    %r9,0xb8(%rsp)
    1b23:	mov    %r8,0xc0(%rsp)
    1b2b:	jmp    19c6 <main+0x736>
    1b30:	mov    %rcx,%rdi
    1b33:	mov    %rbx,%rdx
    1b36:	mov    %rbp,%rsi
    1b39:	mov    %r9,0x38(%rsp)
    1b3e:	mov    %r8,0x8(%rsp)
    1b43:	call   1150 <memmove@plt>
    1b48:	mov    0x8(%rsp),%r8
    1b4d:	mov    0x38(%rsp),%r9
    1b52:	mov    %rax,%rcx
    1b55:	mov    %r13,%rsi
    1b58:	mov    %rbp,%rdi
    1b5b:	mov    %r9,0x50(%rsp)
    1b60:	sub    %rbp,%rsi
    1b63:	mov    %rcx,0x38(%rsp)
    1b68:	mov    %r8,0x8(%rsp)
    1b6d:	call   1110 <operator delete(void*, unsigned long)@plt>
    1b72:	mov    0x50(%rsp),%r9
    1b77:	mov    0x38(%rsp),%rcx
    1b7c:	mov    0x8(%rsp),%r8
    1b81:	jmp    1b13 <main+0x883>
    1b83:	nopl   0x0(%rax,%rax,1)
    1b88:	add    $0x1,%rax
    1b8c:	jb     1bc2 <main+0x932>
    1b8e:	movabs $0xfffffffffffffff,%rdx
    1b98:	cmp    %rdx,%rax
    1b9b:	cmova  %rdx,%rax
    1b9f:	shl    $0x3,%rax
    1ba3:	mov    %rax,0x38(%rsp)
    1ba8:	mov    0x38(%rsp),%rdi
    1bad:	call   1100 <operator new(unsigned long)@plt>
    1bb2:	mov    0x38(%rsp),%r8
    1bb7:	mov    %rax,%rcx
    1bba:	add    %rax,%r8
    1bbd:	jmp    1af9 <main+0x869>
    1bc2:	movabs $0x7ffffffffffffff8,%rax
    1bcc:	mov    %rax,0x38(%rsp)
    1bd1:	jmp    1ba8 <main+0x918>
    1bd3:	movabs $0xfffffffffffffff,%rdx
    1bdd:	cmp    %rdx,%rax
    1be0:	cmova  %rdx,%rax
    1be4:	shl    $0x3,%rax
    1be8:	mov    %rax,0x38(%rsp)
    1bed:	jmp    18f8 <main+0x668>
    1bf2:	nopw   0x0(%rax,%rax,1)
    1bf8:	mov    0x20(%rsp),%rsi
    1bfd:	cmp    0x1a8(%rsp),%rsi
    1c05:	jne    1a8c <main+0x7fc>
    1c0b:	mov    0x30(%rsp),%rdi
    1c10:	cmp    0x1b0(%rsp),%rdi
    1c18:	jne    1a8c <main+0x7fc>
    1c1e:	mov    0x40(%rsp),%rsi
    1c23:	cmp    %rsi,0x1c0(%rsp)
    1c2b:	jne    1a8c <main+0x7fc>
    1c31:	mov    0x48(%rsp),%rsi
    1c36:	cmp    %rsi,0x1b8(%rsp)
    1c3e:	jne    1a8c <main+0x7fc>
    1c44:	sub    %rbx,%rax
    1c47:	pxor   %xmm0,%xmm0
    1c4b:	mov    0xe0(%rsp),%r12
    1c53:	cvtsi2sd %rax,%xmm0
    1c58:	mulsd  0x1500(%rip),%xmm0        # 3160 <_IO_stdin_used+0x160>
    1c60:	mov    0xd8(%rsp),%rax
    1c68:	movsd  %xmm0,0x8(%rsp)
    1c6e:	cmp    %r12,%rax
    1c71:	je     1eb0 <main+0xc20>
    1c77:	movsd  0x8(%rsp),%xmm5
    1c7d:	add    $0x8,%rax
    1c81:	movsd  %xmm5,-0x8(%rax)
    1c86:	mov    %rax,0xd8(%rsp)
    1c8e:	sub    $0x1,%ebp
    1c91:	jne    1a58 <main+0x7c8>
    1c97:	mov    0xd0(%rsp),%rbx
    1c9f:	mov    0xd8(%rsp),%rsi
    1ca7:	mov    %rbx,%rdi
    1caa:	call   2770 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]>
    1caf:	movsd  (%rbx),%xmm1
    1cb3:	movsd  0x190(%rbx),%xmm0
    1cbb:	lea    0x1388(%rip),%rdx        # 304a <_IO_stdin_used+0x4a>
    1cc2:	movsd  0x318(%rbx),%xmm2
    1cca:	mov    $0x2,%edi
    1ccf:	mov    $0x3,%eax
    1cd4:	lea    0x1405(%rip),%rsi        # 30e0 <_IO_stdin_used+0xe0>
    1cdb:	call   10e0 <__printf_chk@plt>
    1ce0:	mov    0xe0(%rsp),%rsi
    1ce8:	mov    %rbx,%rdi
    1ceb:	mov    $0x65,%r12d
    1cf1:	sub    %rbx,%rsi
    1cf4:	call   1110 <operator delete(void*, unsigned long)@plt>
    1cf9:	lea    0xf0(%rsp),%rdi
    1d01:	xor    %eax,%eax
    1d03:	mov    $0x6,%ecx
    1d08:	mov    %rdi,0x68(%rsp)
    1d0d:	rep stos %eax,%es:(%rdi)
    1d0f:	lea    0x1d0(%rsp),%rax
    1d17:	mov    %rax,0x18(%rsp)
    1d1c:	nopl   0x0(%rax)
    1d20:	call   1140 <std::chrono::_V2::steady_clock::now()@plt>
    1d25:	mov    0x28(%rsp),%rsi
    1d2a:	mov    0x18(%rsp),%rdi
    1d2f:	mov    $0x1f4,%ecx
    1d34:	mov    $0x4000,%edx
    1d39:	mov    %rax,%rbx
    1d3c:	call   2c00 <k_lut(Tick const*, unsigned long, int)>
    1d41:	call   1140 <std::chrono::_V2::steady_clock::now()@plt>
    1d46:	cmp    0x1d0(%rsp),%r14
    1d4e:	je     1d70 <main+0xae0>
    1d50:	lea    0x1300(%rip),%rdx        # 3057 <_IO_stdin_used+0x57>
    1d57:	lea    0x12ba(%rip),%rsi        # 3018 <_IO_stdin_used+0x18>
    1d5e:	mov    $0x2,%edi
    1d63:	xor    %eax,%eax
    1d65:	call   10e0 <__printf_chk@plt>
    1d6a:	jmp    164d <main+0x3bd>
    1d6f:	nop
    1d70:	mov    0x20(%rsp),%rsi
    1d75:	cmp    0x1d8(%rsp),%rsi
    1d7d:	jne    1d50 <main+0xac0>
    1d7f:	mov    0x30(%rsp),%rdi
    1d84:	cmp    0x1e0(%rsp),%rdi
    1d8c:	jne    1d50 <main+0xac0>
    1d8e:	mov    0x40(%rsp),%rdi
    1d93:	cmp    %rdi,0x1f0(%rsp)
    1d9b:	jne    1d50 <main+0xac0>
    1d9d:	mov    0x48(%rsp),%rsi
    1da2:	cmp    %rsi,0x1e8(%rsp)
    1daa:	jne    1d50 <main+0xac0>
    1dac:	sub    %rbx,%rax
    1daf:	pxor   %xmm0,%xmm0
    1db3:	mov    0x100(%rsp),%rbp
    1dbb:	cvtsi2sd %rax,%xmm0
    1dc0:	mulsd  0x1398(%rip),%xmm0        # 3160 <_IO_stdin_used+0x160>
    1dc8:	mov    0xf8(%rsp),%rax
    1dd0:	movsd  %xmm0,0x8(%rsp)
    1dd6:	cmp    %rbp,%rax
    1dd9:	je     1f43 <main+0xcb3>
    1ddf:	movsd  0x8(%rsp),%xmm1
    1de5:	add    $0x8,%rax
    1de9:	movsd  %xmm1,-0x8(%rax)
    1dee:	mov    %rax,0xf8(%rsp)
    1df6:	sub    $0x1,%r12d
    1dfa:	jne    1d20 <main+0xa90>
    1e00:	mov    0xf0(%rsp),%rbx
    1e08:	mov    0xf8(%rsp),%rsi
    1e10:	mov    %rbx,%rdi
    1e13:	call   2770 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]>
    1e18:	movsd  (%rbx),%xmm1
    1e1c:	movsd  0x190(%rbx),%xmm0
    1e24:	lea    0x122c(%rip),%rdx        # 3057 <_IO_stdin_used+0x57>
    1e2b:	movsd  0x318(%rbx),%xmm2
    1e33:	mov    $0x2,%edi
    1e38:	mov    $0x3,%eax
    1e3d:	lea    0x129c(%rip),%rsi        # 30e0 <_IO_stdin_used+0xe0>
    1e44:	call   10e0 <__printf_chk@plt>
    1e49:	mov    0x100(%rsp),%rsi
    1e51:	mov    %rbx,%rdi
    1e54:	sub    %rbx,%rsi
    1e57:	call   1110 <operator delete(void*, unsigned long)@plt>
    1e5c:	mov    0x28(%rsp),%rdi
    1e61:	mov    $0x40000,%esi
    1e66:	call   1110 <operator delete(void*, unsigned long)@plt>
    1e6b:	addq   $0x10,0x58(%rsp)
    1e71:	mov    0x58(%rsp),%rax
    1e76:	cmp    %r15,%rax
    1e79:	jne    1389 <main+0xf9>
    1e7f:	mov    0xbf8(%rsp),%rax
    1e87:	sub    %fs:0x28,%rax
    1e90:	jne    21a0 <main+0xf10>
    1e96:	add    $0xc08,%rsp
    1e9d:	xor    %eax,%eax
    1e9f:	pop    %rbx
    1ea0:	pop    %rbp
    1ea1:	pop    %r12
    1ea3:	pop    %r13
    1ea5:	pop    %r14
    1ea7:	pop    %r15
    1ea9:	ret
    1eaa:	nopw   0x0(%rax,%rax,1)
    1eb0:	mov    0xd0(%rsp),%rbx
    1eb8:	movabs $0xfffffffffffffff,%rsi
    1ec2:	sub    %rbx,%rax
    1ec5:	mov    %rax,%r13
    1ec8:	sar    $0x3,%rax
    1ecc:	cmp    %rsi,%rax
    1ecf:	je     2162 <main+0xed2>
    1ed5:	cmp    %rbx,%r12
    1ed8:	je     201a <main+0xd8a>
    1ede:	lea    (%rax,%rax,1),%rdi
    1ee2:	mov    %rdi,0x38(%rsp)
    1ee7:	cmp    %rax,%rdi
    1eea:	jb     2090 <main+0xe00>
    1ef0:	xor    %ecx,%ecx
    1ef2:	test   %rdi,%rdi
    1ef5:	jne    20ff <main+0xe6f>
    1efb:	movsd  0x8(%rsp),%xmm2
    1f01:	lea    0x8(%rcx,%r13,1),%r8
    1f06:	movsd  %xmm2,(%rcx,%r13,1)
    1f0c:	test   %r13,%r13
    1f0f:	jg     1fd8 <main+0xd48>
    1f15:	test   %rbx,%rbx
    1f18:	jne    1ff3 <main+0xd63>
    1f1e:	mov    0x38(%rsp),%rax
    1f23:	mov    %rcx,0xd0(%rsp)
    1f2b:	mov    %r8,0xd8(%rsp)
    1f33:	add    %rax,%rcx
    1f36:	mov    %rcx,0xe0(%rsp)
    1f3e:	jmp    1c8e <main+0x9fe>
    1f43:	mov    0xf0(%rsp),%rbx
    1f4b:	movabs $0xfffffffffffffff,%rdi
    1f55:	sub    %rbx,%rax
    1f58:	mov    %rax,%r13
    1f5b:	sar    $0x3,%rax
    1f5f:	cmp    %rdi,%rax
    1f62:	je     2143 <main+0xeb3>
    1f68:	cmp    %rbx,%rbp
    1f6b:	je     209c <main+0xe0c>
    1f71:	lea    (%rax,%rax,1),%rdx
    1f75:	cmp    %rax,%rdx
    1f78:	jb     20d0 <main+0xe40>
    1f7e:	test   %rdx,%rdx
    1f81:	jne    2111 <main+0xe81>
    1f87:	xor    %eax,%eax
    1f89:	xor    %ecx,%ecx
    1f8b:	mov    %rax,0x38(%rsp)
    1f90:	movsd  0x8(%rsp),%xmm7
    1f96:	lea    0x8(%rcx,%r13,1),%r8
    1f9b:	movsd  %xmm7,(%rcx,%r13,1)
    1fa1:	test   %r13,%r13
    1fa4:	jg     204e <main+0xdbe>
    1faa:	test   %rbx,%rbx
    1fad:	jne    2069 <main+0xdd9>
    1fb3:	mov    0x38(%rsp),%rax
    1fb8:	mov    %rcx,0xf0(%rsp)
    1fc0:	mov    %r8,0xf8(%rsp)
    1fc8:	add    %rax,%rcx
    1fcb:	mov    %rcx,0x100(%rsp)
    1fd3:	jmp    1df6 <main+0xb66>
    1fd8:	mov    %rcx,%rdi
    1fdb:	mov    %r13,%rdx
    1fde:	mov    %rbx,%rsi
    1fe1:	mov    %r8,0x8(%rsp)
    1fe6:	call   1150 <memmove@plt>
    1feb:	mov    0x8(%rsp),%r8
    1ff0:	mov    %rax,%rcx
    1ff3:	mov    %r12,%rsi
    1ff6:	mov    %rbx,%rdi
    1ff9:	mov    %rcx,0x50(%rsp)
    1ffe:	sub    %rbx,%rsi
    2001:	mov    %r8,0x8(%rsp)
    2006:	call   1110 <operator delete(void*, unsigned long)@plt>
    200b:	mov    0x50(%rsp),%rcx
    2010:	mov    0x8(%rsp),%r8
    2015:	jmp    1f1e <main+0xc8e>
    201a:	movabs $0xfffffffffffffff,%rdx
    2024:	add    $0x1,%rax
    2028:	jb     2031 <main+0xda1>
    202a:	cmp    %rdx,%rax
    202d:	cmovbe %rax,%rdx
    2031:	lea    0x0(,%rdx,8),%rax
    2039:	mov    %rax,%rdi
    203c:	mov    %rax,0x38(%rsp)
    2041:	call   1100 <operator new(unsigned long)@plt>
    2046:	mov    %rax,%rcx
    2049:	jmp    1efb <main+0xc6b>
    204e:	mov    %rcx,%rdi
    2051:	mov    %r13,%rdx
    2054:	mov    %rbx,%rsi
    2057:	mov    %r8,0x8(%rsp)
    205c:	call   1150 <memmove@plt>
    2061:	mov    0x8(%rsp),%r8
    2066:	mov    %rax,%rcx
    2069:	mov    %rbp,%rsi
    206c:	mov    %rbx,%rdi
    206f:	mov    %rcx,0x50(%rsp)
    2074:	sub    %rbx,%rsi
    2077:	mov    %r8,0x8(%rsp)
    207c:	call   1110 <operator delete(void*, unsigned long)@plt>
    2081:	mov    0x50(%rsp),%rcx
    2086:	mov    0x8(%rsp),%r8
    208b:	jmp    1fb3 <main+0xd23>
    2090:	movabs $0xfffffffffffffff,%rdx
    209a:	jmp    2031 <main+0xda1>
    209c:	movabs $0xfffffffffffffff,%rdx
    20a6:	add    $0x1,%rax
    20aa:	jb     20b3 <main+0xe23>
    20ac:	cmp    %rdx,%rax
    20af:	cmovbe %rax,%rdx
    20b3:	lea    0x0(,%rdx,8),%rax
    20bb:	mov    %rax,%rdi
    20be:	mov    %rax,0x38(%rsp)
    20c3:	call   1100 <operator new(unsigned long)@plt>
    20c8:	mov    %rax,%rcx
    20cb:	jmp    1f90 <main+0xd00>
    20d0:	movabs $0xfffffffffffffff,%rdx
    20da:	jmp    20b3 <main+0xe23>
    20dc:	movabs $0xfffffffffffffff,%rax
    20e6:	cmp    %rax,%rdx
    20e9:	cmova  %rax,%rdx
    20ed:	lea    0x0(,%rdx,8),%rax
    20f5:	mov    %rax,0x38(%rsp)
    20fa:	jmp    1ba8 <main+0x918>
    20ff:	movabs $0xfffffffffffffff,%rdx
    2109:	mov    %rdi,%rax
    210c:	jmp    202a <main+0xd9a>
    2111:	movabs $0xfffffffffffffff,%rax
    211b:	cmp    %rax,%rdx
    211e:	cmova  %rax,%rdx
    2122:	jmp    20b3 <main+0xe23>
    2124:	mov    0xbf8(%rsp),%rax
    212c:	sub    %fs:0x28,%rax
    2135:	jne    21a0 <main+0xf10>
    2137:	lea    0xee7(%rip),%rdi        # 3025 <_IO_stdin_used+0x25>
    213e:	call   10f0 <std::__throw_length_error(char const*)@plt>
    2143:	mov    0xbf8(%rsp),%rax
    214b:	sub    %fs:0x28,%rax
    2154:	jne    21a0 <main+0xf10>
    2156:	lea    0xec8(%rip),%rdi        # 3025 <_IO_stdin_used+0x25>
    215d:	call   10f0 <std::__throw_length_error(char const*)@plt>
    2162:	mov    0xbf8(%rsp),%rax
    216a:	sub    %fs:0x28,%rax
    2173:	jne    21a0 <main+0xf10>
    2175:	lea    0xea9(%rip),%rdi        # 3025 <_IO_stdin_used+0x25>
    217c:	call   10f0 <std::__throw_length_error(char const*)@plt>
    2181:	mov    0xbf8(%rsp),%rax
    2189:	sub    %fs:0x28,%rax
    2192:	jne    21a0 <main+0xf10>
    2194:	lea    0xe8a(%rip),%rdi        # 3025 <_IO_stdin_used+0x25>
    219b:	call   10f0 <std::__throw_length_error(char const*)@plt>
    21a0:	call   1120 <__stack_chk_fail@plt>
    21a5:	endbr64
    21a9:	mov    %rax,%rbx
    21ac:	jmp    122e <main.cold>
    21b1:	endbr64
    21b5:	mov    %rax,%rbx
    21b8:	jmp    1276 <main.cold+0x48>
    21bd:	endbr64
    21c1:	mov    %rax,%rbx
    21c4:	jmp    123b <main.cold+0xd>
    21c9:	endbr64
    21cd:	mov    %rax,%rbx
    21d0:	jmp    1282 <main.cold+0x54>
    21d5:	endbr64
    21d9:	mov    %rax,%rbx
    21dc:	jmp    1265 <main.cold+0x37>
    21e1:	cs nopw 0x0(%rax,%rax,1)
    21eb:	nopl   0x0(%rax,%rax,1)

00000000000021f0 <_start>:
    21f0:	endbr64
    21f4:	xor    %ebp,%ebp
    21f6:	mov    %rdx,%r9
    21f9:	pop    %rsi
    21fa:	mov    %rsp,%rdx
    21fd:	and    $0xfffffffffffffff0,%rsp
    2201:	push   %rax
    2202:	push   %rsp
    2203:	xor    %r8d,%r8d
    2206:	xor    %ecx,%ecx
    2208:	lea    -0xf7f(%rip),%rdi        # 1290 <main>
    220f:	call   *0x2dcb(%rip)        # 4fe0 <__libc_start_main@GLIBC_2.34>
    2215:	hlt
    2216:	cs nopw 0x0(%rax,%rax,1)

0000000000002220 <deregister_tm_clones>:
    2220:	lea    0x2df1(%rip),%rdi        # 5018 <__TMC_END__>
    2227:	lea    0x2dea(%rip),%rax        # 5018 <__TMC_END__>
    222e:	cmp    %rdi,%rax
    2231:	je     2248 <deregister_tm_clones+0x28>
    2233:	mov    0x2dae(%rip),%rax        # 4fe8 <_ITM_deregisterTMCloneTable@Base>
    223a:	test   %rax,%rax
    223d:	je     2248 <deregister_tm_clones+0x28>
    223f:	jmp    *%rax
    2241:	nopl   0x0(%rax)
    2248:	ret
    2249:	nopl   0x0(%rax)

0000000000002250 <register_tm_clones>:
    2250:	lea    0x2dc1(%rip),%rdi        # 5018 <__TMC_END__>
    2257:	lea    0x2dba(%rip),%rsi        # 5018 <__TMC_END__>
    225e:	sub    %rdi,%rsi
    2261:	mov    %rsi,%rax
    2264:	shr    $0x3f,%rsi
    2268:	sar    $0x3,%rax
    226c:	add    %rax,%rsi
    226f:	sar    $1,%rsi
    2272:	je     2288 <register_tm_clones+0x38>
    2274:	mov    0x2d7d(%rip),%rax        # 4ff8 <_ITM_registerTMCloneTable@Base>
    227b:	test   %rax,%rax
    227e:	je     2288 <register_tm_clones+0x38>
    2280:	jmp    *%rax
    2282:	nopw   0x0(%rax,%rax,1)
    2288:	ret
    2289:	nopl   0x0(%rax)

0000000000002290 <__do_global_dtors_aux>:
    2290:	endbr64
    2294:	cmpb   $0x0,0x2d8d(%rip)        # 5028 <completed.0>
    229b:	jne    22c8 <__do_global_dtors_aux+0x38>
    229d:	push   %rbp
    229e:	cmpq   $0x0,0x2d32(%rip)        # 4fd8 <__cxa_finalize@GLIBC_2.2.5>
    22a6:	mov    %rsp,%rbp
    22a9:	je     22b7 <__do_global_dtors_aux+0x27>
    22ab:	mov    0x2d56(%rip),%rdi        # 5008 <__dso_handle>
    22b2:	call   10d0 <__cxa_finalize@plt>
    22b7:	call   2220 <deregister_tm_clones>
    22bc:	movb   $0x1,0x2d65(%rip)        # 5028 <completed.0>
    22c3:	pop    %rbp
    22c4:	ret
    22c5:	nopl   (%rax)
    22c8:	ret
    22c9:	nopl   0x0(%rax)

00000000000022d0 <frame_dummy>:
    22d0:	endbr64
    22d4:	jmp    2250 <register_tm_clones>
    22d9:	nopl   0x0(%rax)

00000000000022e0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]>:
    22e0:	push   %r12
    22e2:	mov    %rsi,%rax
    22e5:	push   %rbp
    22e6:	sub    %rdi,%rax
    22e9:	mov    %rdi,%rbp
    22ec:	push   %rbx
    22ed:	sub    $0x10,%rsp
    22f1:	cmp    $0x80,%rax
    22f7:	jle    2583 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x2a3>
    22fd:	mov    %rdx,%r12
    2300:	mov    %rsi,%rcx
    2303:	test   %rdx,%rdx
    2306:	je     258c <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x2ac>
    230c:	mov    %rsi,%rdi
    230f:	lea    0x8(%rbp),%rbx
    2313:	movupd 0x0(%rbp),%xmm0
    2318:	sar    $0x4,%rax
    231c:	sub    $0x1,%r12
    2320:	movsd  -0x8(%rdi),%xmm3
    2325:	lea    0x0(%rbp,%rax,8),%rax
    232a:	movsd  (%rax),%xmm2
    232e:	movapd %xmm0,%xmm5
    2332:	movapd %xmm0,%xmm4
    2336:	unpckhpd %xmm5,%xmm5
    233a:	shufpd $0x1,%xmm0,%xmm4
    233f:	comisd %xmm5,%xmm2
    2343:	movapd %xmm5,%xmm1
    2347:	jbe    243b <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x15b>
    234d:	comisd %xmm2,%xmm3
    2351:	ja     2468 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x188>
    2357:	comisd %xmm5,%xmm3
    235b:	ja     244b <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x16b>
    2361:	movups %xmm4,0x0(%rbp)
    2365:	movsd  -0x8(%rdi),%xmm2
    236a:	comisd %xmm0,%xmm1
    236e:	mov    %rbx,%rsi
    2371:	mov    %rdi,%rdx
    2374:	lea    0x8(%rsi),%rax
    2378:	jbe    23db <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xfb>
    237a:	nopw   0x0(%rax,%rax,1)
    2380:	mov    %rax,%rcx
    2383:	movsd  (%rax),%xmm0
    2387:	add    $0x8,%rax
    238b:	comisd %xmm0,%xmm1
    238f:	ja     2380 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xa0>
    2391:	comisd %xmm1,%xmm2
    2395:	lea    -0x10(%rdx),%rax
    2399:	jbe    23f0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x110>
    239b:	nopl   0x0(%rax,%rax,1)
    23a0:	mov    %rax,%rdx
    23a3:	movsd  (%rax),%xmm2
    23a7:	sub    $0x8,%rax
    23ab:	comisd %xmm1,%xmm2
    23af:	ja     23a0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xc0>
    23b1:	cmp    %rdx,%rcx
    23b4:	jae    2400 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x120>
    23b6:	movsd  %xmm2,(%rcx)
    23ba:	lea    0x8(%rcx),%rsi
    23be:	movsd  -0x8(%rdx),%xmm2
    23c3:	movsd  %xmm0,(%rdx)
    23c7:	movsd  0x8(%rcx),%xmm0
    23cc:	movsd  0x0(%rbp),%xmm1
    23d1:	lea    0x8(%rsi),%rax
    23d5:	comisd %xmm0,%xmm1
    23d9:	ja     2380 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xa0>
    23db:	comisd %xmm1,%xmm2
    23df:	mov    %rsi,%rcx
    23e2:	lea    -0x10(%rdx),%rax
    23e6:	ja     23a0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xc0>
    23e8:	nopl   0x0(%rax,%rax,1)
    23f0:	sub    $0x8,%rdx
    23f4:	cmp    %rdx,%rcx
    23f7:	jb     23b6 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xd6>
    23f9:	nopl   0x0(%rax)
    2400:	mov    %rdi,%rsi
    2403:	mov    %r12,%rdx
    2406:	mov    %rcx,%rdi
    2409:	mov    %rcx,0x8(%rsp)
    240e:	call   22e0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]>
    2413:	mov    0x8(%rsp),%rcx
    2418:	mov    %rcx,%rax
    241b:	sub    %rbp,%rax
    241e:	cmp    $0x80,%rax
    2424:	jle    2583 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x2a3>
    242a:	test   %r12,%r12
    242d:	je     258c <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x2ac>
    2433:	mov    %rcx,%rdi
    2436:	jmp    2313 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x33>
    243b:	comisd %xmm5,%xmm3
    243f:	ja     2361 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x81>
    2445:	comisd %xmm2,%xmm3
    2449:	jbe    2468 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x188>
    244b:	movsd  %xmm3,0x0(%rbp)
    2450:	movapd %xmm0,%xmm2
    2454:	movsd  %xmm0,-0x8(%rdi)
    2459:	movsd  0x0(%rbp),%xmm1
    245e:	movsd  0x8(%rbp),%xmm0
    2463:	jmp    236a <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x8a>
    2468:	movsd  %xmm2,0x0(%rbp)
    246d:	movsd  %xmm0,(%rax)
    2471:	movsd  0x8(%rbp),%xmm0
    2476:	movsd  0x0(%rbp),%xmm1
    247b:	movsd  -0x8(%rdi),%xmm2
    2480:	jmp    236a <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x8a>
    2485:	sub    $0x8,%rcx
    2489:	nopl   0x0(%rax)
    2490:	mov    %rcx,%rdi
    2493:	movsd  0x0(%rbp),%xmm0
    2498:	movsd  (%rcx),%xmm2
    249c:	sub    %rbp,%rdi
    249f:	mov    %rdi,%r11
    24a2:	movsd  %xmm0,(%rcx)
    24a6:	sar    $0x3,%r11
    24aa:	lea    -0x1(%r11),%rax
    24ae:	mov    %r11,%rbx
    24b1:	mov    %rax,%r10
    24b4:	and    $0x1,%ebx
    24b7:	shr    $0x3f,%r10
    24bb:	add    %rax,%r10
    24be:	sar    $1,%r10
    24c1:	cmp    $0x10,%rdi
    24c5:	jle    270a <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x42a>
    24cb:	xor    %esi,%esi
    24cd:	jmp    24d3 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x1f3>
    24cf:	nop
    24d0:	mov    %rdx,%rsi
    24d3:	lea    0x1(%rsi),%rax
    24d7:	lea    (%rax,%rax,1),%rdx
    24db:	shl    $0x4,%rax
    24df:	lea    -0x1(%rdx),%r8
    24e3:	add    %rbp,%rax
    24e6:	lea    0x0(%rbp,%r8,8),%r9
    24eb:	movsd  (%rax),%xmm0
    24ef:	movsd  (%r9),%xmm1
    24f4:	comisd %xmm0,%xmm1
    24f8:	jbe    2504 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x224>
    24fa:	movapd %xmm1,%xmm0
    24fe:	mov    %r9,%rax
    2501:	mov    %r8,%rdx
    2504:	movsd  %xmm0,0x0(%rbp,%rsi,8)
    250a:	cmp    %r10,%rdx
    250d:	jl     24d0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x1f0>
    250f:	test   %rbx,%rbx
    2512:	je     26b4 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x3d4>
    2518:	lea    -0x1(%rdx),%r8
    251c:	mov    %r8,%rsi
    251f:	shr    $0x3f,%rsi
    2523:	add    %r8,%rsi
    2526:	sar    $1,%rsi
    2529:	test   %rdx,%rdx
    252c:	jne    255c <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x27c>
    252e:	jmp    275d <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x47d>
    2533:	nopl   0x0(%rax,%rax,1)
    2538:	lea    -0x1(%rsi),%rdx
    253c:	movsd  %xmm0,(%rax)
    2540:	mov    %rdx,%rax
    2543:	shr    $0x3f,%rax
    2547:	add    %rdx,%rax
    254a:	mov    %rsi,%rdx
    254d:	sar    $1,%rax
    2550:	test   %rsi,%rsi
    2553:	je     269a <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x3ba>
    2559:	mov    %rax,%rsi
    255c:	lea    0x0(%rbp,%rsi,8),%r8
    2561:	lea    0x0(%rbp,%rdx,8),%rax
    2566:	movsd  (%r8),%xmm0
    256b:	comisd %xmm0,%xmm2
    256f:	ja     2538 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x258>
    2571:	movsd  %xmm2,(%rax)
    2575:	sub    $0x8,%rcx
    2579:	cmp    $0x8,%rdi
    257d:	jg     2490 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x1b0>
    2583:	add    $0x10,%rsp
    2587:	pop    %rbx
    2588:	pop    %rbp
    2589:	pop    %r12
    258b:	ret
    258c:	sar    $0x3,%rax
    2590:	lea    -0x2(%rax),%r11
    2594:	lea    -0x1(%rax),%r9
    2598:	not    %rax
    259b:	sar    $1,%r11
    259e:	mov    %eax,%r8d
    25a1:	sar    $1,%r9
    25a4:	lea    0x0(%rbp,%r11,8),%r10
    25a9:	mov    %r11,%rdi
    25ac:	and    $0x1,%r8d
    25b0:	movsd  (%r10),%xmm2
    25b5:	mov    %r10,%rdx
    25b8:	cmp    %r9,%rdi
    25bb:	jge    268d <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x3ad>
    25c1:	mov    %rdi,%rsi
    25c4:	jmp    25d3 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x2f3>
    25c6:	cs nopw 0x0(%rax,%rax,1)
    25d0:	mov    %rax,%rsi
    25d3:	lea    0x1(%rsi),%rdx
    25d7:	lea    (%rdx,%rdx,1),%rax
    25db:	shl    $0x4,%rdx
    25df:	lea    -0x1(%rax),%rbx
    25e3:	add    %rbp,%rdx
    25e6:	lea    0x0(%rbp,%rbx,8),%r12
    25eb:	movsd  (%rdx),%xmm0
    25ef:	movsd  (%r12),%xmm1
    25f5:	comisd %xmm0,%xmm1
    25f9:	jbe    2605 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x325>
    25fb:	movapd %xmm1,%xmm0
    25ff:	mov    %r12,%rdx
    2602:	mov    %rbx,%rax
    2605:	movsd  %xmm0,0x0(%rbp,%rsi,8)
    260b:	cmp    %r9,%rax
    260e:	jl     25d0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x2f0>
    2610:	cmp    %rax,%r11
    2613:	jne    261e <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x33e>
    2615:	test   %r8b,%r8b
    2618:	jne    2730 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x450>
    261e:	lea    -0x1(%rax),%rsi
    2622:	sar    $1,%rsi
    2625:	cmp    %rax,%rdi
    2628:	jl     2653 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x373>
    262a:	jmp    2754 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x474>
    262f:	nop
    2630:	lea    -0x1(%rsi),%rdx
    2634:	movsd  %xmm0,(%rax)
    2638:	mov    %rdx,%rax
    263b:	shr    $0x3f,%rax
    263f:	add    %rdx,%rax
    2642:	sar    $1,%rax
    2645:	mov    %rax,%rdx
    2648:	mov    %rsi,%rax
    264b:	cmp    %rsi,%rdi
    264e:	jge    2695 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x3b5>
    2650:	mov    %rdx,%rsi
    2653:	lea    0x0(%rbp,%rsi,8),%rbx
    2658:	lea    0x0(%rbp,%rax,8),%rax
    265d:	movsd  (%rbx),%xmm0
    2661:	comisd %xmm0,%xmm2
    2665:	ja     2630 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x350>
    2667:	movsd  %xmm2,(%rax)
    266b:	test   %rdi,%rdi
    266e:	je     2485 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x1a5>
    2674:	sub    $0x8,%r10
    2678:	sub    $0x1,%rdi
    267c:	movsd  (%r10),%xmm2
    2681:	mov    %r10,%rdx
    2684:	cmp    %r9,%rdi
    2687:	jl     25c1 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x2e1>
    268d:	mov    %rdi,%rax
    2690:	jmp    2610 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x330>
    2695:	mov    %rbx,%rax
    2698:	jmp    2667 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x387>
    269a:	mov    %r8,%rax
    269d:	sub    $0x8,%rcx
    26a1:	movsd  %xmm2,(%rax)
    26a5:	cmp    $0x8,%rdi
    26a9:	jg     2490 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x1b0>
    26af:	jmp    2583 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x2a3>
    26b4:	lea    -0x2(%r11),%rsi
    26b8:	sar    $1,%rsi
    26bb:	cmp    %rdx,%rsi
    26be:	je     26ef <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x40f>
    26c0:	lea    -0x1(%rdx),%r8
    26c4:	mov    %r8,%rsi
    26c7:	shr    $0x3f,%rsi
    26cb:	add    %r8,%rsi
    26ce:	sar    $1,%rsi
    26d1:	test   %rdx,%rdx
    26d4:	jne    255c <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x27c>
    26da:	jmp    2571 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x291>
    26df:	nop
    26e0:	cmp    $0x2,%rax
    26e4:	mov    %rbp,%rax
    26e7:	ja     2571 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x291>
    26ed:	xor    %edx,%edx
    26ef:	lea    0x1(%rdx,%rdx,1),%r8
    26f4:	mov    %rdx,%rsi
    26f7:	movsd  0x0(%rbp,%r8,8),%xmm0
    26fe:	mov    %r8,%rdx
    2701:	movsd  %xmm0,(%rax)
    2705:	jmp    255c <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x27c>
    270a:	test   %rbx,%rbx
    270d:	je     26e0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x400>
    270f:	mov    %rbp,%rax
    2712:	sub    $0x8,%rcx
    2716:	movsd  %xmm2,(%rax)
    271a:	cmp    $0x8,%rdi
    271e:	jg     2490 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x1b0>
    2724:	jmp    2583 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x2a3>
    2729:	nopl   0x0(%rax)
    2730:	lea    (%rax,%rax,1),%rsi
    2734:	lea    0x1(%rsi),%rax
    2738:	sar    $1,%rsi
    273b:	lea    0x0(%rbp,%rax,8),%rbx
    2740:	movsd  (%rbx),%xmm0
    2744:	movsd  %xmm0,(%rdx)
    2748:	mov    %rbx,%rdx
    274b:	cmp    %rax,%rdi
    274e:	jl     2653 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x373>
    2754:	movsd  %xmm2,(%rdx)
    2758:	jmp    2674 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x394>
    275d:	movsd  %xmm2,(%rax)
    2761:	sub    $0x8,%rcx
    2765:	jmp    2490 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x1b0>
    276a:	nopw   0x0(%rax,%rax,1)

0000000000002770 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]>:
    2770:	cmp    %rsi,%rdi
    2773:	je     2970 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x200>
    2779:	push   %r14
    277b:	mov    %rdi,%r14
    277e:	push   %r13
    2780:	push   %r12
    2782:	mov    %rsi,%r12
    2785:	push   %rbp
    2786:	sub    %rdi,%r12
    2789:	mov    %rsi,%rbp
    278c:	push   %rbx
    278d:	mov    %r12,%rax
    2790:	sub    $0x10,%rsp
    2794:	sar    $0x3,%rax
    2798:	je     28b1 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x141>
    279e:	bsr    %rax,%rdx
    27a2:	lea    0x8(%r14),%rbx
    27a6:	movslq %edx,%rdx
    27a9:	add    %rdx,%rdx
    27ac:	call   22e0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]>
    27b1:	cmp    $0x80,%r12
    27b8:	jle    28c1 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x151>
    27be:	lea    0x80(%r14),%r12
    27c5:	mov    $0x8,%r13d
    27cb:	jmp    2808 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x98>
    27cd:	nopl   (%rax)
    27d0:	sub    %r14,%rdx
    27d3:	cmp    $0x8,%rdx
    27d7:	jle    2979 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x209>
    27dd:	mov    %r13,%rdi
    27e0:	mov    %r14,%rsi
    27e3:	movsd  %xmm1,0x8(%rsp)
    27e9:	sub    %rdx,%rdi
    27ec:	add    %rbx,%rdi
    27ef:	call   1150 <memmove@plt>
    27f4:	movsd  0x8(%rsp),%xmm1
    27fa:	add    $0x8,%rbx
    27fe:	movsd  %xmm1,(%r14)
    2803:	cmp    %rbx,%r12
    2806:	je     2854 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xe4>
    2808:	movsd  (%rbx),%xmm1
    280c:	movsd  (%r14),%xmm0
    2811:	mov    %rbx,%rdx
    2814:	comisd %xmm1,%xmm0
    2818:	ja     27d0 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x60>
    281a:	movsd  -0x8(%rbx),%xmm0
    281f:	lea    -0x8(%rbx),%rax
    2823:	comisd %xmm1,%xmm0
    2827:	jbe    2847 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xd7>
    2829:	nopl   0x0(%rax)
    2830:	movsd  %xmm0,0x8(%rax)
    2835:	mov    %rax,%rdx
    2838:	movsd  -0x8(%rax),%xmm0
    283d:	sub    $0x8,%rax
    2841:	comisd %xmm1,%xmm0
    2845:	ja     2830 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xc0>
    2847:	add    $0x8,%rbx
    284b:	movsd  %xmm1,(%rdx)
    284f:	cmp    %rbx,%r12
    2852:	jne    2808 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x98>
    2854:	cmp    %r12,%rbp
    2857:	je     28a4 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x134>
    2859:	nopl   0x0(%rax)
    2860:	movsd  (%r12),%xmm1
    2866:	movsd  -0x8(%r12),%xmm0
    286d:	lea    -0x8(%r12),%rax
    2872:	comisd %xmm1,%xmm0
    2876:	jbe    2950 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x1e0>
    287c:	nopl   0x0(%rax)
    2880:	movsd  %xmm0,0x8(%rax)
    2885:	mov    %rax,%rdx
    2888:	movsd  -0x8(%rax),%xmm0
    288d:	sub    $0x8,%rax
    2891:	comisd %xmm1,%xmm0
    2895:	ja     2880 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x110>
    2897:	add    $0x8,%r12
    289b:	movsd  %xmm1,(%rdx)
    289f:	cmp    %r12,%rbp
    28a2:	jne    2860 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xf0>
    28a4:	add    $0x10,%rsp
    28a8:	pop    %rbx
    28a9:	pop    %rbp
    28aa:	pop    %r12
    28ac:	pop    %r13
    28ae:	pop    %r14
    28b0:	ret
    28b1:	mov    $0xfffffffffffffffe,%rdx
    28b8:	lea    0x8(%r14),%rbx
    28bc:	call   22e0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]>
    28c1:	cmp    %rbx,%rbp
    28c4:	je     28a4 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x134>
    28c6:	mov    $0x8,%r12d
    28cc:	jmp    2908 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x198>
    28ce:	xchg   %ax,%ax
    28d0:	sub    %r14,%rdx
    28d3:	cmp    $0x8,%rdx
    28d7:	jle    2971 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x201>
    28dd:	mov    %r12,%rdi
    28e0:	mov    %r14,%rsi
    28e3:	movsd  %xmm1,0x8(%rsp)
    28e9:	sub    %rdx,%rdi
    28ec:	add    %rbx,%rdi
    28ef:	call   1150 <memmove@plt>
    28f4:	movsd  0x8(%rsp),%xmm1
    28fa:	movsd  %xmm1,(%r14)
    28ff:	add    $0x8,%rbx
    2903:	cmp    %rbx,%rbp
    2906:	je     28a4 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x134>
    2908:	movsd  (%rbx),%xmm1
    290c:	movsd  (%r14),%xmm0
    2911:	mov    %rbx,%rdx
    2914:	comisd %xmm1,%xmm0
    2918:	ja     28d0 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x160>
    291a:	movsd  -0x8(%rbx),%xmm0
    291f:	lea    -0x8(%rbx),%rax
    2923:	comisd %xmm1,%xmm0
    2927:	jbe    2947 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x1d7>
    2929:	nopl   0x0(%rax)
    2930:	movsd  %xmm0,0x8(%rax)
    2935:	mov    %rax,%rdx
    2938:	movsd  -0x8(%rax),%xmm0
    293d:	sub    $0x8,%rax
    2941:	comisd %xmm1,%xmm0
    2945:	ja     2930 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x1c0>
    2947:	movsd  %xmm1,(%rdx)
    294b:	jmp    28ff <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x18f>
    294d:	nopl   (%rax)
    2950:	mov    %r12,%rdx
    2953:	add    $0x8,%r12
    2957:	movsd  %xmm1,(%rdx)
    295b:	cmp    %r12,%rbp
    295e:	jne    2860 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xf0>
    2964:	jmp    28a4 <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x134>
    2969:	nopl   0x0(%rax)
    2970:	ret
    2971:	jne    28fa <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x18a>
    2973:	movsd  %xmm0,(%rbx)
    2977:	jmp    28fa <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x18a>
    2979:	jne    27fa <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x8a>
    297f:	movsd  %xmm0,(%rbx)
    2983:	jmp    27fa <void std::__sort<__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__normal_iterator<double*, std::vector<double, std::allocator<double> > >, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x8a>
    2988:	nopl   0x0(%rax,%rax,1)

0000000000002990 <scan(std::vector<Tick, std::allocator<Tick> > const&, int)>:
    2990:	endbr64
    2994:	push   %r14
    2996:	pxor   %xmm0,%xmm0
    299a:	push   %r13
    299c:	push   %r12
    299e:	push   %rbp
    299f:	mov    %rdi,%rbp
    29a2:	push   %rbx
    29a3:	mov    (%rsi),%rbx
    29a6:	mov    0x8(%rsi),%r12
    29aa:	movq   $0x0,0x20(%rdi)
    29b2:	movups %xmm0,(%rdi)
    29b5:	movups %xmm0,0x10(%rdi)
    29b9:	cmp    %rbx,%r12
    29bc:	je     2a0e <scan(std::vector<Tick, std::allocator<Tick> > const&, int)+0x7e>
    29be:	mov    %edx,%r14d
    29c1:	lea    0x63c(%rip),%r13        # 3004 <_IO_stdin_used+0x4>
    29c8:	jmp    29e7 <scan(std::vector<Tick, std::allocator<Tick> > const&, int)+0x57>
    29ca:	nopw   0x0(%rax,%rax,1)
    29d0:	add    %rax,0x0(%rbp)
    29d4:	cmp    %r14d,%ecx
    29d7:	jl     29de <scan(std::vector<Tick, std::allocator<Tick> > const&, int)+0x4e>
    29d9:	addq   $0x1,0x10(%rbp)
    29de:	add    $0x10,%rbx
    29e2:	cmp    %rbx,%r12
    29e5:	je     2a0e <scan(std::vector<Tick, std::allocator<Tick> > const&, int)+0x7e>
    29e7:	mov    0x8(%rbx),%ecx
    29ea:	test   %ecx,%ecx
    29ec:	jle    2a20 <scan(std::vector<Tick, std::allocator<Tick> > const&, int)+0x90>
    29ee:	cmpb   $0x0,0xc(%rbx)
    29f2:	movslq %ecx,%rax
    29f5:	je     29d0 <scan(std::vector<Tick, std::allocator<Tick> > const&, int)+0x40>
    29f7:	add    %rax,0x8(%rbp)
    29fb:	cmp    %r14d,%ecx
    29fe:	jl     29de <scan(std::vector<Tick, std::allocator<Tick> > const&, int)+0x4e>
    2a00:	add    $0x10,%rbx
    2a04:	addq   $0x1,0x18(%rbp)
    2a09:	cmp    %rbx,%r12
    2a0c:	jne    29e7 <scan(std::vector<Tick, std::allocator<Tick> > const&, int)+0x57>
    2a0e:	pop    %rbx
    2a0f:	mov    %rbp,%rax
    2a12:	pop    %rbp
    2a13:	pop    %r12
    2a15:	pop    %r13
    2a17:	pop    %r14
    2a19:	ret
    2a1a:	nopw   0x0(%rax,%rax,1)
    2a20:	mov    0x25f9(%rip),%rdi        # 5020 <stderr@GLIBC_2.2.5>
    2a27:	mov    %r13,%rdx
    2a2a:	mov    $0x2,%esi
    2a2f:	xor    %eax,%eax
    2a31:	call   1160 <__fprintf_chk@plt>
    2a36:	addq   $0x1,0x20(%rbp)
    2a3b:	jmp    29de <scan(std::vector<Tick, std::allocator<Tick> > const&, int)+0x4e>
    2a3d:	nopl   (%rax)

0000000000002a40 <k_general(std::vector<Tick, std::allocator<Tick> > const&, int)>:
    2a40:	endbr64
    2a44:	push   %rbx
    2a45:	mov    %rdi,%rbx
    2a48:	sub    $0x10,%rsp
    2a4c:	mov    %fs:0x28,%rax
    2a55:	mov    %rax,0x8(%rsp)
    2a5a:	xor    %eax,%eax
    2a5c:	call   2990 <scan(std::vector<Tick, std::allocator<Tick> > const&, int)>
    2a61:	mov    0x8(%rsp),%rax
    2a66:	sub    %fs:0x28,%rax
    2a6f:	jne    2a7a <k_general(std::vector<Tick, std::allocator<Tick> > const&, int)+0x3a>
    2a71:	add    $0x10,%rsp
    2a75:	mov    %rbx,%rax
    2a78:	pop    %rbx
    2a79:	ret
    2a7a:	call   1120 <__stack_chk_fail@plt>
    2a7f:	nop

0000000000002a80 <k_hot(Tick const*, unsigned long, long)>:
    2a80:	endbr64
    2a84:	push   %r15
    2a86:	mov    %rdi,%r8
    2a89:	push   %r14
    2a8b:	push   %r13
    2a8d:	push   %r12
    2a8f:	push   %rbp
    2a90:	push   %rbx
    2a91:	sub    $0x28,%rsp
    2a95:	test   %rdx,%rdx
    2a98:	je     2b28 <k_hot(Tick const*, unsigned long, long)+0xa8>
    2a9e:	lea    0x8(%rsi),%rbx
    2aa2:	mov    %rdx,%r9
    2aa5:	xor    %r14d,%r14d
    2aa8:	xor    %r12d,%r12d
    2aab:	xor    %r15d,%r15d
    2aae:	xor    %r13d,%r13d
    2ab1:	xor    %esi,%esi
    2ab3:	xor    %ebp,%ebp
    2ab5:	nopl   (%rax)
    2ab8:	movslq (%rbx),%rdx
    2abb:	mov    %rdx,%rdi
    2abe:	test   %rdx,%rdx
    2ac1:	jle    119c <k_hot(Tick const*, unsigned long, long) [clone .cold]>
    2ac7:	movzbl 0x4(%rbx),%eax
    2acb:	xor    %edi,%edi
    2acd:	neg    %rax
    2ad0:	cmp    %rdx,%rcx
    2ad3:	setle  %dil
    2ad7:	add    %rdx,%r13
    2ada:	and    %rax,%rdx
    2add:	and    %rdi,%rax
    2ae0:	add    %rdx,%r15
    2ae3:	add    %rdi,%r12
    2ae6:	add    %rax,%r14
    2ae9:	add    $0x1,%rbp
    2aed:	add    $0x10,%rbx
    2af1:	cmp    %rbp,%r9
    2af4:	jne    2ab8 <k_hot(Tick const*, unsigned long, long)+0x38>
    2af6:	sub    %r15,%r13
    2af9:	sub    %r14,%r12
    2afc:	mov    %r13,(%r8)
    2aff:	mov    %r8,%rax
    2b02:	mov    %r15,0x8(%r8)
    2b06:	mov    %r12,0x10(%r8)
    2b0a:	mov    %r14,0x18(%r8)
    2b0e:	mov    %rsi,0x20(%r8)
    2b12:	add    $0x28,%rsp
    2b16:	pop    %rbx
    2b17:	pop    %rbp
    2b18:	pop    %r12
    2b1a:	pop    %r13
    2b1c:	pop    %r14
    2b1e:	pop    %r15
    2b20:	ret
    2b21:	nopl   0x0(%rax)
    2b28:	xor    %r12d,%r12d
    2b2b:	xor    %r13d,%r13d
    2b2e:	xor    %r14d,%r14d
    2b31:	xor    %r15d,%r15d
    2b34:	xor    %esi,%esi
    2b36:	jmp    2afc <k_hot(Tick const*, unsigned long, long)+0x7c>
    2b38:	nopl   0x0(%rax,%rax,1)

0000000000002b40 <k_bc(Tick const*, unsigned long, int)>:
    2b40:	endbr64
    2b44:	push   %r15
    2b46:	mov    %rdi,%r15
    2b49:	push   %r14
    2b4b:	push   %r13
    2b4d:	push   %r12
    2b4f:	push   %rbp
    2b50:	push   %rbx
    2b51:	sub    $0x28,%rsp
    2b55:	test   %rdx,%rdx
    2b58:	je     2bf0 <k_bc(Tick const*, unsigned long, int)+0xb0>
    2b5e:	mov    %rdx,%rbp
    2b61:	mov    %ecx,%r12d
    2b64:	add    $0x8,%rsi
    2b68:	xor    %r13d,%r13d
    2b6b:	xor    %edx,%edx
    2b6d:	xor    %r14d,%r14d
    2b70:	xor    %ecx,%ecx
    2b72:	xor    %r8d,%r8d
    2b75:	xor    %ebx,%ebx
    2b77:	jmp    2b9b <k_bc(Tick const*, unsigned long, int)+0x5b>
    2b79:	nopl   0x0(%rax)
    2b80:	add    %rax,%rcx
    2b83:	xor    %eax,%eax
    2b85:	cmp    %edi,%r12d
    2b88:	setle  %al
    2b8b:	add    %rax,%r14
    2b8e:	add    $0x1,%rbx
    2b92:	add    $0x10,%rsi
    2b96:	cmp    %rbx,%rbp
    2b99:	je     2bc9 <k_bc(Tick const*, unsigned long, int)+0x89>
    2b9b:	mov    (%rsi),%edi
    2b9d:	test   %edi,%edi
    2b9f:	jle    11d0 <k_bc(Tick const*, unsigned long, int) [clone .cold]>
    2ba5:	cmpb   $0x0,0x4(%rsi)
    2ba9:	movslq %edi,%rax
    2bac:	je     2b80 <k_bc(Tick const*, unsigned long, int)+0x40>
    2bae:	add    %rax,%rdx
    2bb1:	xor    %eax,%eax
    2bb3:	cmp    %edi,%r12d
    2bb6:	setle  %al
    2bb9:	add    $0x1,%rbx
    2bbd:	add    $0x10,%rsi
    2bc1:	add    %rax,%r13
    2bc4:	cmp    %rbx,%rbp
    2bc7:	jne    2b9b <k_bc(Tick const*, unsigned long, int)+0x5b>
    2bc9:	mov    %rcx,(%r15)
    2bcc:	mov    %r15,%rax
    2bcf:	mov    %rdx,0x8(%r15)
    2bd3:	mov    %r14,0x10(%r15)
    2bd7:	mov    %r13,0x18(%r15)
    2bdb:	mov    %r8,0x20(%r15)
    2bdf:	add    $0x28,%rsp
    2be3:	pop    %rbx
    2be4:	pop    %rbp
    2be5:	pop    %r12
    2be7:	pop    %r13
    2be9:	pop    %r14
    2beb:	pop    %r15
    2bed:	ret
    2bee:	xchg   %ax,%ax
    2bf0:	xor    %r13d,%r13d
    2bf3:	xor    %edx,%edx
    2bf5:	xor    %r14d,%r14d
    2bf8:	xor    %ecx,%ecx
    2bfa:	xor    %r8d,%r8d
    2bfd:	jmp    2bc9 <k_bc(Tick const*, unsigned long, int)+0x89>
    2bff:	nop

0000000000002c00 <k_lut(Tick const*, unsigned long, int)>:
    2c00:	endbr64
    2c04:	push   %r12
    2c06:	pxor   %xmm0,%xmm0
    2c0a:	push   %rbp
    2c0b:	mov    %rdi,%rbp
    2c0e:	push   %rbx
    2c0f:	sub    $0x50,%rsp
    2c13:	mov    %fs:0x28,%rax
    2c1c:	mov    %rax,0x48(%rsp)
    2c21:	xor    %eax,%eax
    2c23:	movaps %xmm0,0x20(%rsp)
    2c28:	movaps %xmm0,0x30(%rsp)
    2c2d:	test   %rdx,%rdx
    2c30:	je     2cb0 <k_lut(Tick const*, unsigned long, int)+0xb0>
    2c32:	add    $0x8,%rsi
    2c36:	xor    %r12d,%r12d
    2c39:	xor    %ebx,%ebx
    2c3b:	nopl   0x0(%rax,%rax,1)
    2c40:	mov    (%rsi),%edi
    2c42:	test   %edi,%edi
    2c44:	jle    1204 <k_lut(Tick const*, unsigned long, int) [clone .cold]>
    2c4a:	movzbl 0x4(%rsi),%eax
    2c4e:	movslq %edi,%r8
    2c51:	add    %r8,0x20(%rsp,%rax,8)
    2c56:	cmp    %edi,%ecx
    2c58:	setle  %dil
    2c5c:	movzbl %dil,%edi
    2c60:	add    %rdi,0x30(%rsp,%rax,8)
    2c65:	add    $0x1,%rbx
    2c69:	add    $0x10,%rsi
    2c6d:	cmp    %rbx,%rdx
    2c70:	jne    2c40 <k_lut(Tick const*, unsigned long, int)+0x40>
    2c72:	movdqa 0x20(%rsp),%xmm1
    2c78:	movdqa 0x30(%rsp),%xmm0
    2c7e:	mov    %r12,0x20(%rbp)
    2c82:	movups %xmm1,0x0(%rbp)
    2c86:	movups %xmm0,0x10(%rbp)
    2c8a:	mov    0x48(%rsp),%rax
    2c8f:	sub    %fs:0x28,%rax
    2c98:	jne    2cbd <k_lut(Tick const*, unsigned long, int)+0xbd>
    2c9a:	add    $0x50,%rsp
    2c9e:	mov    %rbp,%rax
    2ca1:	pop    %rbx
    2ca2:	pop    %rbp
    2ca3:	pop    %r12
    2ca5:	ret
    2ca6:	cs nopw 0x0(%rax,%rax,1)
    2cb0:	pxor   %xmm0,%xmm0
    2cb4:	xor    %r12d,%r12d
    2cb7:	movdqa %xmm0,%xmm1
    2cbb:	jmp    2c7e <k_lut(Tick const*, unsigned long, int)+0x7e>
    2cbd:	call   1120 <__stack_chk_fail@plt>
    2cc2:	cs nopw 0x0(%rax,%rax,1)
    2ccc:	nopl   0x0(%rax)

0000000000002cd0 <std::mersenne_twister_engine<unsigned long, 64ul, 312ul, 156ul, 31ul, 13043109905998158313ul, 29ul, 6148914691236517205ul, 17ul, 8202884508482404352ul, 37ul, 18444473444759240704ul, 43ul, 6364136223846793005ul>::_M_gen_rand()>:
    2cd0:	endbr64
    2cd4:	movdqa 0x444(%rip),%xmm7        # 3120 <_IO_stdin_used+0x120>
    2cdc:	mov    %rdi,%r9
    2cdf:	mov    %rdi,%rdx
    2ce2:	movdqa 0x446(%rip),%xmm6        # 3130 <_IO_stdin_used+0x130>
    2cea:	movdqa 0x44e(%rip),%xmm5        # 3140 <_IO_stdin_used+0x140>
    2cf2:	movdqa 0x456(%rip),%xmm4        # 3150 <_IO_stdin_used+0x150>
    2cfa:	mov    %rdi,%rax
    2cfd:	pxor   %xmm3,%xmm3
    2d01:	lea    0x4e0(%rdi),%rcx
    2d08:	nopl   0x0(%rax,%rax,1)
    2d10:	movdqu (%rax),%xmm0
    2d14:	movdqu 0x8(%rax),%xmm1
    2d19:	add    $0x10,%rax
    2d1d:	movdqu 0x4d0(%rax),%xmm2
    2d25:	pand   %xmm6,%xmm1
    2d29:	pand   %xmm7,%xmm0
    2d2d:	por    %xmm1,%xmm0
    2d31:	movdqa %xmm0,%xmm1
    2d35:	pand   %xmm5,%xmm0
    2d39:	psrlq  $0x1,%xmm1
    2d3e:	pxor   %xmm2,%xmm1
    2d42:	movdqa %xmm3,%xmm2
    2d46:	psubq  %xmm0,%xmm2
    2d4a:	pand   %xmm4,%xmm2
    2d4e:	movdqa %xmm2,%xmm0
    2d52:	pxor   %xmm1,%xmm0
    2d56:	movups %xmm0,-0x10(%rax)
    2d5a:	cmp    %rcx,%rax
    2d5d:	jne    2d10 <std::mersenne_twister_engine<unsigned long, 64ul, 312ul, 156ul, 31ul, 13043109905998158313ul, 29ul, 6148914691236517205ul, 17ul, 8202884508482404352ul, 37ul, 18444473444759240704ul, 43ul, 6364136223846793005ul>::_M_gen_rand()+0x40>
    2d5f:	mov    0x4e0(%r9),%rsi
    2d66:	lea    0x4d8(%r9),%r8
    2d6d:	movabs $0xb5026f5aa96619e9,%rdi
    2d77:	nopw   0x0(%rax,%rax,1)
    2d80:	and    $0xffffffff80000000,%rsi
    2d87:	add    $0x8,%rdx
    2d8b:	mov    %rsi,%rcx
    2d8e:	mov    0x4e0(%rdx),%rsi
    2d95:	mov    %rsi,%rax
    2d98:	and    $0x7fffffff,%eax
    2d9d:	or     %rcx,%rax
    2da0:	mov    %rax,%rcx
    2da3:	and    $0x1,%eax
    2da6:	neg    %rax
    2da9:	shr    $1,%rcx
    2dac:	xor    -0x8(%rdx),%rcx
    2db0:	and    %rdi,%rax
    2db3:	xor    %rcx,%rax
    2db6:	mov    %rax,0x4d8(%rdx)
    2dbd:	cmp    %r8,%rdx
    2dc0:	jne    2d80 <std::mersenne_twister_engine<unsigned long, 64ul, 312ul, 156ul, 31ul, 13043109905998158313ul, 29ul, 6148914691236517205ul, 17ul, 8202884508482404352ul, 37ul, 18444473444759240704ul, 43ul, 6364136223846793005ul>::_M_gen_rand()+0xb0>
    2dc2:	mov    0x9b8(%r9),%rax
    2dc9:	mov    (%r9),%rdx
    2dcc:	movq   $0x0,0x9c0(%r9)
    2dd7:	and    $0x7fffffff,%edx
    2ddd:	and    $0xffffffff80000000,%rax
    2de3:	or     %rdx,%rax
    2de6:	mov    %rax,%rdx
    2de9:	and    $0x1,%eax
    2dec:	neg    %rax
    2def:	shr    $1,%rdx
    2df2:	xor    0x4d8(%r9),%rdx
    2df9:	and    %rdi,%rax
    2dfc:	xor    %rdx,%rax
    2dff:	mov    %rax,0x9b8(%r9)
    2e06:	ret
    2e07:	nopw   0x0(%rax,%rax,1)

0000000000002e10 <std::mersenne_twister_engine<unsigned long, 64ul, 312ul, 156ul, 31ul, 13043109905998158313ul, 29ul, 6148914691236517205ul, 17ul, 8202884508482404352ul, 37ul, 18444473444759240704ul, 43ul, 6364136223846793005ul>::operator()()>:
    2e10:	endbr64
    2e14:	mov    0x9c0(%rdi),%rax
    2e1b:	push   %rbx
    2e1c:	mov    %rdi,%rbx
    2e1f:	cmp    $0x137,%rax
    2e25:	ja     2e90 <std::mersenne_twister_engine<unsigned long, 64ul, 312ul, 156ul, 31ul, 13043109905998158313ul, 29ul, 6148914691236517205ul, 17ul, 8202884508482404352ul, 37ul, 18444473444759240704ul, 43ul, 6364136223846793005ul>::operator()()+0x80>
    2e27:	movabs $0x5555555555555555,%rcx
    2e31:	lea    0x1(%rax),%rdx
    2e35:	mov    (%rbx,%rax,8),%rax
    2e39:	mov    %rdx,0x9c0(%rbx)
    2e40:	pop    %rbx
    2e41:	mov    %rax,%rdx
    2e44:	shr    $0x1d,%rdx
    2e48:	and    %rcx,%rdx
    2e4b:	movabs $0x71d67fffeda60000,%rcx
    2e55:	xor    %rax,%rdx
    2e58:	mov    %rdx,%rax
    2e5b:	shl    $0x11,%rax
    2e5f:	and    %rcx,%rax
    2e62:	movabs $0xfff7eee000000000,%rcx
    2e6c:	xor    %rdx,%rax
    2e6f:	mov    %rax,%rdx
    2e72:	shl    $0x25,%rdx
    2e76:	and    %rcx,%rdx
    2e79:	xor    %rax,%rdx
    2e7c:	mov    %rdx,%rax
    2e7f:	shr    $0x2b,%rax
    2e83:	xor    %rdx,%rax
    2e86:	ret
    2e87:	nopw   0x0(%rax,%rax,1)
    2e90:	call   2cd0 <std::mersenne_twister_engine<unsigned long, 64ul, 312ul, 156ul, 31ul, 13043109905998158313ul, 29ul, 6148914691236517205ul, 17ul, 8202884508482404352ul, 37ul, 18444473444759240704ul, 43ul, 6364136223846793005ul>::_M_gen_rand()>
    2e95:	mov    0x9c0(%rbx),%rax
    2e9c:	jmp    2e27 <std::mersenne_twister_engine<unsigned long, 64ul, 312ul, 156ul, 31ul, 13043109905998158313ul, 29ul, 6148914691236517205ul, 17ul, 8202884508482404352ul, 37ul, 18444473444759240704ul, 43ul, 6364136223846793005ul>::operator()()+0x17>
    2e9e:	xchg   %ax,%ax

0000000000002ea0 <std::vector<double, std::allocator<double> >::~vector()>:
    2ea0:	endbr64
    2ea4:	mov    (%rdi),%rax
    2ea7:	test   %rax,%rax
    2eaa:	je     2ec0 <std::vector<double, std::allocator<double> >::~vector()+0x20>
    2eac:	mov    0x10(%rdi),%rsi
    2eb0:	mov    %rax,%rdi
    2eb3:	sub    %rax,%rsi
    2eb6:	jmp    1110 <operator delete(void*, unsigned long)@plt>
    2ebb:	nopl   0x0(%rax,%rax,1)
    2ec0:	ret

Disassembly of section .fini:

0000000000002ec4 <_fini>:
    2ec4:	endbr64
    2ec8:	sub    $0x8,%rsp
    2ecc:	add    $0x8,%rsp
    2ed0:	ret
