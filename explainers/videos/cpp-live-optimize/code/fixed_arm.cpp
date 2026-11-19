// fixed.cpp's mailbox for AArch64, written with the GCC/Clang __atomic builtins
// (no aarch64 libstdc++ headers on this box). Same orders as std::atomic.
struct Msg { char type, side; unsigned short locate; unsigned qty; long price; char stock[8]; unsigned long ts; };
Msg slot;
bool ready;
void publish(const Msg& m) {
  slot = m;
  __atomic_store_n(&ready, true, __ATOMIC_RELEASE);
}
long consume() {
  while (!__atomic_load_n(&ready, __ATOMIC_ACQUIRE)) {}
  __atomic_store_n(&ready, false, __ATOMIC_RELAXED);
  return slot.price;
}
