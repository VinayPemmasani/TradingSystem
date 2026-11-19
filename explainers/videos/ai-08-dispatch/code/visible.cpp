// Out-of-line instantiations of the templates, for inspecting/counting with objdump.
#include "fast.hpp"
template void fast::quote_all<fast::Clamp>(fast::Clamp, const Prices&, Prices&);
template int fast::run_serial<fast::Clamp>(fast::Clamp, const int*, int);
