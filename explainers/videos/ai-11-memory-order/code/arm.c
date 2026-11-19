// clang --target=aarch64-linux-gnu -O2 -S arm.c : what the same orders cost on ARM
unsigned long head;
void st_seq(unsigned long v) { __atomic_store_n(&head, v, __ATOMIC_SEQ_CST); }
void st_rel(unsigned long v) { __atomic_store_n(&head, v, __ATOMIC_RELEASE); }
void st_rlx(unsigned long v) { __atomic_store_n(&head, v, __ATOMIC_RELAXED); }
unsigned long ld_seq(void) { return __atomic_load_n(&head, __ATOMIC_SEQ_CST); }
unsigned long ld_acq(void) { return __atomic_load_n(&head, __ATOMIC_ACQUIRE); }
unsigned long ld_rlx(void) { return __atomic_load_n(&head, __ATOMIC_RELAXED); }
