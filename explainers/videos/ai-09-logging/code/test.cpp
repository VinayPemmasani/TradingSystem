// Both loggers must write the same lines (ignoring the leading timestamp).
// Writes t_ai.log and t_fast.log in the current directory.
#include <cstdio>
#include <fstream>
#include <string>
#include <vector>
#include "ai.hpp"
#include "fast.hpp"
static std::vector<std::string> body(const char* p) {
  std::ifstream f(p); std::vector<std::string> v; std::string s;
  while (std::getline(f, s)) v.push_back(s.substr(s.find(' ') + 1));
  return v;
}
static LogRing<1024> ring;
int main() {
  const char* syms[3] = {"AAPL", "MSFT", "NVDA"};
  { Logger lg("t_ai.log");
    for (int i = 0; i < 500; ++i) lg.fill(syms[i % 3], -5 + i * 1000003LL, i * 7u, 1ull << 40 | i); }
  FILE* f = fopen("t_fast.log", "w");
  for (int i = 0; i < 500; ++i) ring.fill(syms[i % 3], -5 + i * 1000003LL, i * 7u, 1ull << 40 | i);
  ring.drain(f, 1.0, 0, 0); fclose(f);
  auto a = body("t_ai.log"), b = body("t_fast.log");
  bool ok = a.size() == 500 && a == b;
  printf("%s: %zu vs %zu lines; first: '%s'\n", ok ? "PASS" : "FAIL", a.size(), b.size(), a.empty() ? "" : a[0].c_str());
  return ok ? 0 : 1;
}
