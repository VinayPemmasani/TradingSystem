// LEFT: the general-purpose version. Correct; rejects throw std::runtime_error, caught per order.
#pragma once
#include <stdexcept>
#include <string>
#include "common.hpp"
namespace ai {
struct Gateway {
  Limits lim_; Out out_;
  void validate(const Order& o) const;
  bool on_order(const Order& o);
};
void Gateway::validate(const Order& o) const {
  if (o.qty <= 0 || o.qty > lim_.max_qty)
    throw std::runtime_error(
        "bad qty " + std::to_string(o.qty));
  if (o.px < lim_.px_lo || o.px > lim_.px_hi)
    throw std::runtime_error(
        "px outside band " + std::to_string(o.px));
}
bool Gateway::on_order(const Order& o) {
  try { validate(o); }
  catch (const std::exception& e) {
    out_.reject(o, e.what()); return false;
  }
  out_.send(o);
  return true;
}
// (end of on-screen snippet)
}  // namespace ai
