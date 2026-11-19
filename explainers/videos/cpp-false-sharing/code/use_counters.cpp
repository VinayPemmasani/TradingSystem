#include "counters.hpp"
int main() { Counters c; return sizeof c == 128 ? 0 : 1; }
