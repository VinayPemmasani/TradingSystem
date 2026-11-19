#include "ai.hpp"
#include "fast.hpp"
#include "msg.hpp"
__attribute__((noinline)) void ai_push(BlockingQueue<Tick>& q, const Tick& t) { q.push(t); }
__attribute__((noinline)) Tick ai_pop(BlockingQueue<Tick>& q) { return q.pop(); }
__attribute__((noinline)) bool f_push(SpscRing<Tick, 1024>& q, const Tick& t) { return q.try_push(t); }
__attribute__((noinline)) bool f_pop(SpscRing<Tick, 1024>& q, Tick& t) { return q.try_pop(t); }
