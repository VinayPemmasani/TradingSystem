// Every version must produce the same signals and the same final state.
#include <cstdio>
#include <memory>
#include "all.hpp"
template <class H> void run(const char* name, const std::vector<Msg>& feed) {
  auto h = std::make_unique<H>();
  std::uint64_t sig = 0x1234; long cnt[3] = {0, 0, 0};
  for (const Msg& m : feed) { int s = h->on_msg(m); sig = mix(sig, std::uint64_t(s + 2)); ++cnt[s + 1]; }
  std::printf("%-12s sell %7ld  hold %7ld  buy %7ld  signals %016llx  state %016llx\n", name, cnt[0], cnt[1], cnt[2],
              (unsigned long long)sig, (unsigned long long)h->report());
}
int main(int argc, char** argv) {
  std::size_t n = argc > 1 ? std::strtoull(argv[1], nullptr, 10) : 2000000;
  auto feed = make_feed(n);
  run<v0::Handler>("v0 naive", feed);
  run<v1::Handler>("v1 ds", feed);
  run<v1h::Handler>("v1h table", feed);
  run<v2a::Handler>("v2a ilp", feed);
  run<v2::Handler>("v2 pipe", feed);
  run<v3::Handler>("v3 branch", feed);
  run<v4::Handler>("v4 alloc", feed);
}
// sizes quoted on screen
#include <map>
static_assert(sizeof(v0::State) == 80);
static_assert(sizeof(v0::Trade) == 48);
