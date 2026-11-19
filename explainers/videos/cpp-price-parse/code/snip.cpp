// stod behaviours used in the narration
#include <cstdio>
#include <string>
#include <cstdint>
int main(){ const char* t[]={"1e3","inf"," 1.5","12abc","0x10","1.13"}; for(auto s:t){ std::size_t pos=0; double d=std::stod(s,&pos); std::printf("[%s] -> %g pos %zu  trunc %llu\n",s,d,pos,(unsigned long long)(d*10000)); } }
