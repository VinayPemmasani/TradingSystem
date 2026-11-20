#pragma once

// A small JSON reader, enough for order-trace output and scene.json: objects, arrays,
// strings (with \uXXXX to UTF-8), numbers, true, false, null.

#include <cstdlib>
#include <stdexcept>
#include <string>
#include <string_view>
#include <utility>
#include <vector>

namespace json {

struct Value {
  enum class Type { kNull, kBool, kNumber, kString, kArray, kObject } type = Type::kNull;
  bool b = false;
  double num = 0;
  std::string str;
  std::vector<Value> arr;
  std::vector<std::pair<std::string, Value>> obj;

  const Value* find(std::string_view key) const {
    for (const auto& [k, v] : obj)
      if (k == key) return &v;
    return nullptr;
  }
  const Value& operator[](std::string_view key) const {
    static const Value null;
    const Value* v = find(key);
    return v ? *v : null;
  }
  const Value& operator[](std::size_t i) const { return arr.at(i); }
  double number(double fallback = 0) const { return type == Type::kNumber ? num : fallback; }
  const std::string& string() const { return str; }
  bool is_null() const { return type == Type::kNull; }
};

class Parser {
 public:
  explicit Parser(std::string_view s) : s_{s} {}

  Value parse() {
    Value v = value();
    ws();
    if (i_ != s_.size()) fail("trailing characters");
    return v;
  }

 private:
  [[noreturn]] void fail(const char* what) {
    throw std::runtime_error(std::string("JSON: ") + what + " at byte " + std::to_string(i_));
  }
  void ws() {
    while (i_ < s_.size() && (s_[i_] == ' ' || s_[i_] == '\n' || s_[i_] == '\r' || s_[i_] == '\t'))
      ++i_;
  }
  char peek() {
    ws();
    if (i_ >= s_.size()) fail("unexpected end");
    return s_[i_];
  }
  void expect(char c) {
    if (peek() != c) fail("unexpected character");
    ++i_;
  }
  bool word(std::string_view w) {
    if (s_.substr(i_, w.size()) != w) return false;
    i_ += w.size();
    return true;
  }

  Value value() {
    Value v;
    const char c = peek();
    if (c == '{') {
      v.type = Value::Type::kObject;
      ++i_;
      if (peek() == '}') {
        ++i_;
        return v;
      }
      for (;;) {
        std::string k = string_body();
        expect(':');
        v.obj.emplace_back(std::move(k), value());
        if (peek() == ',') {
          ++i_;
          continue;
        }
        expect('}');
        return v;
      }
    }
    if (c == '[') {
      v.type = Value::Type::kArray;
      ++i_;
      if (peek() == ']') {
        ++i_;
        return v;
      }
      for (;;) {
        v.arr.push_back(value());
        if (peek() == ',') {
          ++i_;
          continue;
        }
        expect(']');
        return v;
      }
    }
    if (c == '"') {
      v.type = Value::Type::kString;
      v.str = string_body();
      return v;
    }
    if (word("true")) {
      v.type = Value::Type::kBool;
      v.b = true;
      return v;
    }
    if (word("false")) {
      v.type = Value::Type::kBool;
      return v;
    }
    if (word("null")) return v;
    const char* begin = s_.data() + i_;
    char* end = nullptr;
    v.num = std::strtod(begin, &end);
    if (end == begin) fail("bad value");
    v.type = Value::Type::kNumber;
    i_ += static_cast<std::size_t>(end - begin);
    return v;
  }

  void utf8(std::string& out, unsigned cp) {
    if (cp < 0x80) {
      out += static_cast<char>(cp);
    } else if (cp < 0x800) {
      out += static_cast<char>(0xC0 | (cp >> 6));
      out += static_cast<char>(0x80 | (cp & 0x3F));
    } else if (cp < 0x10000) {
      out += static_cast<char>(0xE0 | (cp >> 12));
      out += static_cast<char>(0x80 | ((cp >> 6) & 0x3F));
      out += static_cast<char>(0x80 | (cp & 0x3F));
    } else {
      out += static_cast<char>(0xF0 | (cp >> 18));
      out += static_cast<char>(0x80 | ((cp >> 12) & 0x3F));
      out += static_cast<char>(0x80 | ((cp >> 6) & 0x3F));
      out += static_cast<char>(0x80 | (cp & 0x3F));
    }
  }

  unsigned hex4() {
    if (i_ + 4 > s_.size()) fail("short \\u escape");
    const std::string h{s_.substr(i_, 4)};
    i_ += 4;
    return static_cast<unsigned>(std::strtoul(h.c_str(), nullptr, 16));
  }

  std::string string_body() {
    expect('"');
    std::string out;
    while (i_ < s_.size() && s_[i_] != '"') {
      char c = s_[i_++];
      if (c != '\\') {
        out += c;
        continue;
      }
      if (i_ >= s_.size()) fail("bad escape");
      c = s_[i_++];
      switch (c) {
        case 'n': out += '\n'; break;
        case 't': out += '\t'; break;
        case 'r': out += '\r'; break;
        case 'b': out += '\b'; break;
        case 'f': out += '\f'; break;
        case 'u': {
          unsigned cp = hex4();
          if (cp >= 0xD800 && cp < 0xDC00 && word("\\u")) {
            const unsigned lo = hex4();
            cp = 0x10000 + ((cp - 0xD800) << 10) + (lo - 0xDC00);
          }
          utf8(out, cp);
          break;
        }
        default: out += c;  // \" \\ \/
      }
    }
    expect('"');
    return out;
  }

  std::string_view s_;
  std::size_t i_ = 0;
};

inline Value parse(std::string_view s) { return Parser{s}.parse(); }

}  // namespace json
