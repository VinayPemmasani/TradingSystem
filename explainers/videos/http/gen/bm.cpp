#include <chrono>
#include <cstdio>
#include <algorithm>
#include <vector>
#include "lab/vendor/json.hpp"
#include "lab/itch/codec.hpp"
using namespace lab;
volatile std::int64_t sink;
int main(){
  std::string msg = R"([{"ID":3,"Type":"Update","UpdateType":"Quote","SeqNumber":1842,"Fields":{"BID":101.25,"BIDSIZE":300,"QUOTIM_NS":"14:30:05.123456789"}}])";
  itch::AddOrder a{}; a.header.stock_locate=7; a.header.timestamp=52205123456789ull; a.order_reference_number=1; a.buy_sell_indicator='B'; a.shares=300; a.stock=itch::make_symbol("ACME"); a.price=1012500;
  std::byte buf[36]; itch::encode(a, buf);
  const int N=200000; std::vector<double> rj, ri;
  for(int rep=0;rep<15;++rep){
    auto t0=std::chrono::steady_clock::now();
    for(int i=0;i<N;++i){ auto v=vendor::json::parse(msg); const auto* f=v->items[0].get("Fields"); auto p=vendor::json::parse_price(f->get("BID")->text); sink=*p; }
    auto t1=std::chrono::steady_clock::now();
    for(int i=0;i<N;++i){ asm volatile("" : : "r"(buf) : "memory"); itch::AddOrder m; itch::decode(buf, m); sink=m.price+m.shares; }
    auto t2=std::chrono::steady_clock::now();
    rj.push_back(std::chrono::duration<double,std::nano>(t1-t0).count()/N); ri.push_back(std::chrono::duration<double,std::nano>(t2-t1).count()/N);
  }
  std::sort(rj.begin(),rj.end()); std::sort(ri.begin(),ri.end());
  printf("json parse+BID median %.1f ns (min %.1f)\nitch AddOrder decode median %.2f ns (min %.2f)\n", rj[7], rj[0], ri[7], ri[0]);
}
