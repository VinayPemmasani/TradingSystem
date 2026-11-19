#include <cstdio>
#include "lab/vendor/omm.hpp"
#include "lab/vendor/ws.hpp"
using namespace lab::vendor;
static void hex(const std::string& s, size_t n){ for(size_t i=0;i<n && i<s.size();++i) printf("%02X ", (unsigned char)s[i]); printf("\n"); }
int main(){
  Record r{}; r.symbol = {'A','C','M','E',' ',' ',' ',' '}; r.bid=1012500; r.bid_size=300; r.ask=1013000; r.quote_ns=(14ull*3600+30*60+5)*1000000000ull+123456789ull; r.updates=1842;
  std::string out="["; omm::update(out, 2, r, field::kBid|field::kBidSize, ~0u); out+="]";
  printf("UPDATE %zu: %s\n", out.size(), out.c_str());
  std::string f; ws::append_frame(f, ws::kText, out, false); printf("server frame header: "); hex(f, 4);
  std::string login = R"({"ID":1,"Domain":"Login","Key":{"Name":"lab","Elements":)" R"({"ApplicationId":"256","Position":"127.0.0.1"}}})";
  printf("LOGIN %zu: %s\n", login.size(), login.c_str());
  std::string req = "{\"ID\":2,\"Key\":{\"Name\":[\"ACME.O\"]}}"; printf("REQ %zu %s\n", req.size(), req.c_str());
  std::string g; ws::append_frame(g, ws::kText, login, true); printf("client frame: "); hex(g, 10);
  printf("accept %s\n", ws::accept_key("dGhlIHNhbXBsZSBub25jZQ==").c_str());
}
