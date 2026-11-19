#pragma once
// LEFT: the general-purpose version (on screen verbatim below the includes).
#include <sstream>
#include <string>
struct Quote {
  std::string sym; double px; int qty; };
// "ESZ6,5012.25,17" -> {"ESZ6", 5012.25, 17}
Quote parse(const std::string& line) {
  std::stringstream ss(line);
  std::string sym, px, qty;
  std::getline(ss, sym, ',');
  std::getline(ss, px, ',');
  std::getline(ss, qty, ',');
  return {sym, std::stod(px), std::stoi(qty)};
}
