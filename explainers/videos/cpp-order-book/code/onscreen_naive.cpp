// The naive cancel as shown on screen (asks loop written out), compiled and checked.
#include <cassert>
#include <cstdint>
#include <list>
#include <map>
struct Order { std::uint64_t id; std::uint32_t qty; };
std::map<std::uint32_t, std::list<Order>> bids, asks;
bool cancel(std::uint64_t id) {
  for (auto l = bids.begin(); l != bids.end(); ++l)          // every level
    for (auto it = l->second.begin(); it != l->second.end(); ++it)
      if (it->id == id) {                                    // every order
        l->second.erase(it);
        if (l->second.empty()) bids.erase(l);
        return true;
      }
  for (auto l = asks.begin(); l != asks.end(); ++l)
    for (auto it = l->second.begin(); it != l->second.end(); ++it)
      if (it->id == id) {
        l->second.erase(it);
        if (l->second.empty()) asks.erase(l);
        return true;
      }
  return false;
}
int main() {
  bids[100].push_back({17, 1}); bids[100].push_back({18, 1}); asks[101].push_back({64, 1});
  assert(cancel(64) && asks.empty() && !cancel(64));
  assert(cancel(17) && bids.size() == 1 && cancel(18) && bids.empty());
  return 0;
}
