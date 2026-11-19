// Every snippet shown on screen, verbatim, plus a quick test.
#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <vector>
using u8 = std::uint8_t;
using std::size_t;
using std::uint32_t;
using std::uint64_t;

size_t keep_branchy(const u8* in,
                    size_t n, u8* out) {
  size_t k = 0;
  for (size_t i = 0; i < n; ++i)
    if (in[i] >= 128) out[k++] = in[i];
  return k;
}

size_t keep_branchless(const u8* in,
                       size_t n, u8* out) {
  size_t k = 0;
  for (size_t i = 0; i < n; ++i) {
    out[k] = in[i];        // always store
    k += (in[i] >= 128);   // advance 0 or 1
  }
  return k;
}

struct Order {                 // 64 bytes
  uint32_t price, qty;         // hot
  uint64_t id, ts_in, ts_ack;  // cold ...
  char account[16], symbol[8], pad[8];
};
struct Hot { uint32_t price, qty; };  // 8 bytes
static_assert(sizeof(Order) == 64 && sizeof(Hot) == 8);

int main() {
  std::vector<u8> in{5, 200, 128, 127, 255, 0, 130};
  std::vector<u8> a(in.size()), b(in.size());
  size_t ka = keep_branchy(in.data(), in.size(), a.data());
  size_t kb = keep_branchless(in.data(), in.size(), b.data());
  bool ok = ka == 4 && kb == 4;
  for (size_t i = 0; i < 4; ++i) ok = ok && a[i] == b[i];
  ok = ok && a[0] == 200 && a[1] == 128 && a[2] == 255 && a[3] == 130;
  std::puts(ok ? "screen test OK" : "screen test FAILED");
  return ok ? 0 : 1;
}
