// Compiled with -S to show real g++ -O2 output for the on-screen snippets.
#include "all.hpp"
int on_msg_v1(v1::Handler& h, const Msg& m) { return h.on_msg(m); }
int on_msg_v2a(v2a::Handler& h, const Msg& m) { return h.on_msg(m); }
int on_msg_v2(v2::Handler& h, const Msg& m) { return h.on_msg(m); }
int on_msg_v3(v3::Handler& h, const Msg& m) { return h.on_msg(m); }
int on_msg_v4(v4::Handler& h, const Msg& m) { return h.on_msg(m); }
