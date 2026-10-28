#ifndef AMPL_STRINGREF_H_
#define AMPL_STRINGREF_H_
#include <string>
#include <cstring>
#include <stdarg.h>

namespace fmt {

/**
  \rst
  A string reference. It can be constructed from a C string or
  ``std::basic_string``.

  You can use one of the following typedefs for common character types:

  +------------+-------------------------+
  | Type       | Definition              |
  +============+=========================+
  | StringRef  | BasicStringRef<char>    |
  +------------+-------------------------+
  | WStringRef | BasicStringRef<wchar_t> |
  +------------+-------------------------+

  This class is most useful as a parameter type to allow passing
  different types of strings to a function, for example::

    template <typename... Args>
    std::string format(StringRef format_str, const Args & ... args);

  format("{}", 42);
  format(std::string("{}"), 42);
  \endrst
          */
template <typename Char>
class BasicStringRef {
 private:
  const Char *data_;
  std::size_t size_;

 public:
  /** Constructs a string reference object from a C string and a size. */
  BasicStringRef(const Char *s, std::size_t size) : data_(s), size_(size) {}

  /**
    \rst
    Constructs a string reference object from a C string computing
    the size with ``std::char_traits<Char>::length``.
    \endrst
   */
  BasicStringRef(const Char *s)
      : data_(s), size_(std::char_traits<Char>::length(s)) {}

  /**
    \rst
    Constructs a string reference from a ``std::basic_string`` object.
    \endrst
   */
  template <typename Allocator>
  BasicStringRef(
      const std::basic_string<Char, std::char_traits<Char>, Allocator> &s)
      : data_(s.c_str()), size_(s.size()) {}

  /**
    \rst
    Converts a string reference to an ``std::string`` object.
    \endrst
   */
  std::basic_string<Char> to_string() const {
    return std::basic_string<Char>(data_, size_);
  }

  /** Returns a pointer to the string data. */
  const Char *data() const { return data_; }

  /** Returns the string size. */
  std::size_t size() const { return size_; }

  // Lexicographically compare this string reference to other.
  int compare(BasicStringRef other) const {
    std::size_t size = size_ < other.size_ ? size_ : other.size_;
    int result = std::char_traits<Char>::compare(data_, other.data_, size);
    if (result == 0)
      result = size_ == other.size_ ? 0 : (size_ < other.size_ ? -1 : 1);
    return result;
  }

  friend bool operator==(BasicStringRef lhs, BasicStringRef rhs) {
    return lhs.compare(rhs) == 0;
  }
  friend bool operator!=(BasicStringRef lhs, BasicStringRef rhs) {
    return lhs.compare(rhs) != 0;
  }
  friend bool operator<(BasicStringRef lhs, BasicStringRef rhs) {
    return lhs.compare(rhs) < 0;
  }
  friend bool operator<=(BasicStringRef lhs, BasicStringRef rhs) {
    return lhs.compare(rhs) <= 0;
  }
  friend bool operator>(BasicStringRef lhs, BasicStringRef rhs) {
    return lhs.compare(rhs) > 0;
  }
  friend bool operator>=(BasicStringRef lhs, BasicStringRef rhs) {
    return lhs.compare(rhs) >= 0;
  }
};

typedef BasicStringRef<char> StringRef;
typedef BasicStringRef<wchar_t> WStringRef;

/**
  \rst
  A reference to a null terminated string. It can be constructed from a C
  string or ``std::basic_string``.

  You can use one of the following typedefs for common character types:

  +-------------+--------------------------+
  | Type        | Definition               |
  +=============+==========================+
  | CStringRef  | BasicCStringRef<char>    |
  +-------------+--------------------------+
  | WCStringRef | BasicCStringRef<wchar_t> |
  +-------------+--------------------------+

  This class is most useful as a parameter type to allow passing
  different types of strings to a function, for example::

    template <typename... Args>
    std::string format(CStringRef format_str, const Args & ... args);

  format("{}", 42);
  format(std::string("{}"), 42);
  \endrst
          */
template <typename Char>
class BasicCStringRef {
 private:
  const Char *data_;

 public:
  BasicCStringRef() : data_(NULL) {}
  /** Constructs a string reference object from a C string. */
  BasicCStringRef(const Char *s) : data_(s) {}

  /**
    \rst
    Constructs a string reference from a ``std::basic_string`` object.
    \endrst
   */
  template <typename Allocator>
  BasicCStringRef(
      const std::basic_string<Char, std::char_traits<Char>, Allocator> &s)
      : data_(s.c_str()) {}

  /** Returns the pointer to a C string. */
  const Char *c_str() const { return data_; }
};

typedef BasicCStringRef<char> CStringRef;
typedef BasicCStringRef<wchar_t> WCStringRef;

}  // namespace fmt

#endif  // AMPL_STRINGREF_H_
