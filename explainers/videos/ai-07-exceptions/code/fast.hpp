// RIGHT: the hot-path version. Returns a reject code; the reject path is [[unlikely]] and out of line.
#pragma once
#include <cstdio>
#include "common.hpp"
namespace fast {
enum class Rej : std::uint8_t { None, Qty, Px };
struct Gateway {
  Limits lim_; Out out_;
  Rej check(const Order& o) const;
  bool on_order(const Order& o);
  [[gnu::cold, gnu::noinline]] void reject(const Order& o, Rej r);
};
inline Rej Gateway::check(const Order& o) const {
  if (o.qty <= 0 || o.qty > lim_.max_qty)
    [[unlikely]] return Rej::Qty;
  if (o.px < lim_.px_lo || o.px > lim_.px_hi)
    [[unlikely]] return Rej::Px;
  return Rej::None;
}
bool Gateway::on_order(const Order& o) {
  if (Rej r = check(o); r != Rej::None)
    [[unlikely]] { reject(o, r); return false; }
  out_.send(o);
  return true;
}
// (end of on-screen snippet)
// Cold path: formats the same text as the LEFT version, off the hot path.
void Gateway::reject(const Order& o, Rej r) {
  char buf[64];
  int n = r == Rej::Qty ? std::snprintf(buf, sizeof buf, "bad qty %d", o.qty)
                        : std::snprintf(buf, sizeof buf, "px outside band %lld", (long long)o.px);
  out_.reject(o, std::string_view(buf, std::size_t(n)));
}
}  // namespace fast
