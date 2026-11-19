#pragma once
#include <concepts>
#include <variant>

struct Strategy {
  virtual ~Strategy() = default;
  virtual int quote(int mid) const = 0;
};

struct Maker final : Strategy {
  int edge = 2;
  int quote(int mid) const override { return mid - edge; }
};

struct Taker final : Strategy {
  int edge = 3;
  int quote(int mid) const override { return mid + edge; }
};

template <class S>
concept Quoter = requires(const S& s, int mid) {
  { s.quote(mid) } -> std::same_as<int>;
};

using AnyStrategy = std::variant<Maker, Taker>;
