#ifndef AMPL_FORMAT_H_
#define AMPL_FORMAT_H_
#include <fmt/core.h>
#include <fmt/format.h>
#include "ampl/cstringref.h"
#include <cstdarg>
#include <cassert>
#include <iterator>

namespace fmt {

class Writer {
 public:
  fmt::memory_buffer buffer;
  Writer &operator<<(const char *str) {
    buffer.append(str, str + strlen(str));
    return *this;
  }
  Writer &operator<<(std::string str) {
    buffer.append(str.data(), str.data() + str.size());
    return *this;
  }
  Writer &operator<<(char chr) {
    buffer.push_back(chr);
    return *this;
  }
  Writer &operator<<(int value) {
    fmt::format_to(std::back_inserter(buffer), "{}", value);
    return *this;
  }
  Writer &operator<<(std::size_t value) {
    fmt::format_to(std::back_inserter(buffer), "{}", value);
    return *this;
  }
  Writer &operator<<(double value) {
    fmt::format_to(std::back_inserter(buffer), "{}", value);
    return *this;
  }
  Writer &operator<<(fmt::StringRef str) {
    buffer.append(str.data(), str.data() + str.size());
    return *this;
  }
  Writer &operator<<(fmt::CStringRef str) {
    buffer.append(str.c_str(), str.c_str() + strlen(str.c_str()));
    return *this;
  }
  void clear() { buffer.clear(); }
  std::size_t size() const { return buffer.size(); }
  const char *data() const { return buffer.data(); }
  const char *c_str() {
    buffer.reserve(buffer.size() + 1);
    buffer[buffer.size()] = '\0';
    return buffer.data();
  }
  template <typename... Args>
  void write(const char *format, Args... args) {
    fmt::format_to(std::back_inserter(buffer), format, args...);
  }
  std::string str() const { return std::string(buffer.data(), buffer.size()); }
};

typedef Writer MemoryWriter;

}  // namespace fmt

namespace fmt {

template <>
struct formatter<fmt::CStringRef> {
  constexpr auto parse(format_parse_context &ctx) const
      -> decltype(ctx.begin()) {
    return ctx.end();
  }
  template <typename FormatContext>
  auto format(const fmt::CStringRef &str, FormatContext &ctx) const
      -> decltype(ctx.out()) {
    return fmt::format_to(ctx.out(), "{}", str.c_str());
  }
};

template <>
struct formatter<fmt::StringRef> {
  constexpr auto parse(format_parse_context &ctx) const
      -> decltype(ctx.begin()) {
    return ctx.end();
  }
  template <typename FormatContext>
  auto format(const fmt::StringRef &str, FormatContext &ctx) const
      -> decltype(ctx.out()) {
    return fmt::format_to(ctx.out(), "{0:.{1}}", str.data(), str.size());
  }
};

}  // namespace fmt


#endif  // AMPL_FORMAT_H_
