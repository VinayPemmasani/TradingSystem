// Step 5: the "just use a bool" handoff. A data race: undefined behaviour.
#include "common.hpp"
Msg slot;
bool ready = false;
void publish(const Msg& m) {     // feed thread
  slot = m;
  ready = true;
}
std::int64_t consume() {         // strategy thread
  while (!ready) {}              // spin until published
  ready = false;
  return slot.price;
}
