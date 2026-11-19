#include <cstdio>
#include <string>
#include <cstdint>
int main(){ int n=0; for (int w=0; w<1000 && n<12; ++w) for (int f=0; f<10000 && n<12; f+= (w<2?1:97)) { char s[32]; std::snprintf(s,32,"%d.%04d",w,f); std::string t=s; while(t.back()=='0') t.pop_back(); if(t.back()=='.') t.pop_back(); double d=std::stod(t); uint64_t v=uint64_t(d*10000); if (v != uint64_t(w)*10000+f) { std::printf("%s -> %llu  (%.17g)\n", t.c_str(), (unsigned long long)v, d*10000); ++n; } } }
