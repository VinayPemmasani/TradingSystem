#include <cstdio>
#include <string>
#include <cstdint>
int main(){ int n=0; for (int w=1; w<300 && n<15; ++w) for (int c=0; c<100; ++c) { char s[32]; std::snprintf(s,32,"%d.%02d",w,c); double d=std::stod(s); uint64_t v=uint64_t(d*10000); if (v != uint64_t(w)*10000+c*100) { std::printf("%s -> %llu  (%.17g)\n", s, (unsigned long long)v, d*10000); ++n; } } }
