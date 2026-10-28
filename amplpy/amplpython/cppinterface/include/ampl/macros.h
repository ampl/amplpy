#ifndef AMPL_MACROS_H_
#define AMPL_MACROS_H_

#include <stdexcept>

#include "ampl/ampl_c.h"
#include "ampl/amplexception.h"


  /**
  Represents a generic system exception with message
  */
  class StdException : public std::exception {
    std::string message_;

   public:
    ~StdException() noexcept {}
    StdException(fmt::CStringRef cause) : message_(cause.c_str()) {}
    const char *what() const noexcept { return message_.c_str(); }
  };

#define AMPL_DISALLOW_COPY_AND_ASSIGN(TypeName) \
  TypeName(const TypeName &) = delete;         \
  TypeName &operator=(const TypeName &) = delete

#if defined(_WIN32) && !defined(__MINGW32__)
// Fix warnings about deprecated symbols.
#define AMPL_POSIX(call) _##call
#else
#define AMPL_POSIX(call) call
#endif

// Calls to system functions are wrapped in AMPL_SYSTEM for testability.
#ifdef AMPL_SYSTEM
#define AMPL_POSIX_CALL(call) AMPL_SYSTEM(call)
#else
#define AMPL_SYSTEM(call) call
#ifdef _WIN32
// Fix warnings about deprecated symbols.
#define AMPL_POSIX_CALL(call) ::_##call
#else
#define AMPL_POSIX_CALL(call) ::call
#endif
#endif

class AMPL_ErrorInfoHandle {
  AMPL_ERRORINFO* errorInfo_;

public:
  explicit AMPL_ErrorInfoHandle(AMPL_ERRORINFO* errorInfo) : errorInfo_(errorInfo) {}
  ~AMPL_ErrorInfoHandle() {
    if (errorInfo_) {
      AMPL_ErrorInfoFree(&errorInfo_);
    }
  }

  AMPL_ERRORINFO* get() const { return errorInfo_; }

  // Disable copy semantics
  AMPL_ErrorInfoHandle(const AMPL_ErrorInfoHandle&) = delete;
  AMPL_ErrorInfoHandle& operator=(const AMPL_ErrorInfoHandle&) = delete;

  // Enable move semantics
  AMPL_ErrorInfoHandle(AMPL_ErrorInfoHandle&& other) noexcept : errorInfo_(other.errorInfo_) {
    other.errorInfo_ = nullptr;
  }

  AMPL_ErrorInfoHandle& operator=(AMPL_ErrorInfoHandle&& other) noexcept {
    if (this != &other) {
      if (errorInfo_) {
        AMPL_ErrorInfoFree(&errorInfo_);
      }
      errorInfo_ = other.errorInfo_;
      other.errorInfo_ = nullptr;
    }
    return *this;
  }
};

#define AMPL_CALL_CPP(x) \
  do{ \
    AMPL_ErrorInfoHandle callHandle_((x)); \
    AMPL_ERRORINFO *call = callHandle_.get(); \
    if (call) { \
    switch (AMPL_ErrorInfoGetError(call)) { \
    case AMPL_INFEASIBILITY_EXCEPTION: \
      throw InfeasibilityException(AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_PRESOLVE_EXCEPTION: \
      throw PresolveException(AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_LICENSE_EXCEPTION: \
      throw LicenseException(AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_FILE_IO_EXCEPTION: \
      throw FileIOException(AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_UNSUPPORTED_OPERATION_EXCEPTION: \
      throw UnsupportedOperationException(AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_INVALID_SUBSCRIPT_EXCEPTION: \
      throw InvalidSubscriptException(AMPL_ErrorInfoGetSource(call), AMPL_ErrorInfoGetLine(call), AMPL_ErrorInfoGetOffset(call), \
                                      AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_SYNTAX_ERROR_EXCEPTION: \
      throw SyntaxErrorException(AMPL_ErrorInfoGetSource(call), AMPL_ErrorInfoGetLine(call), AMPL_ErrorInfoGetOffset(call), \
                                 AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_NO_DATA_EXCEPTION: \
      throw NoDataException(AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_EXCEPTION: \
      throw AMPLException(AMPL_ErrorInfoGetSource(call), AMPL_ErrorInfoGetLine(call), AMPL_ErrorInfoGetOffset(call), \
                          AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_RUNTIME_ERROR: \
      throw std::runtime_error(AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_LOGIC_ERROR: \
      throw std::logic_error(AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_OUT_OF_RANGE: \
      throw std::out_of_range(AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_INVALID_ARGUMENT: \
       throw std::invalid_argument(AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_STD_EXCEPTION: { \
      throw StdException(AMPL_ErrorInfoGetMessage(call)); \
    } } \
  } } while (0)


#define AMPL_CALL_CPP_W_FREE(x) \
  do { \
    AMPL_ErrorInfoHandle callHandle((x)); \
    AMPL_ERRORINFO* call = callHandle.get(); \
    if (call) { \
    switch (AMPL_ErrorInfoGetError(call)) { \
    case AMPL_INFEASIBILITY_EXCEPTION: \
      throw InfeasibilityException(AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_PRESOLVE_EXCEPTION: \
      throw PresolveException(AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_LICENSE_EXCEPTION: \
      throw LicenseException(AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_FILE_IO_EXCEPTION: \
      throw FileIOException(AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_UNSUPPORTED_OPERATION_EXCEPTION: \
      throw UnsupportedOperationException(AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_INVALID_SUBSCRIPT_EXCEPTION: \
      throw InvalidSubscriptException(AMPL_ErrorInfoGetSource(call), AMPL_ErrorInfoGetLine(call), AMPL_ErrorInfoGetOffset(call), \
                                      AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_SYNTAX_ERROR_EXCEPTION: \
      throw SyntaxErrorException(AMPL_ErrorInfoGetSource(call), AMPL_ErrorInfoGetLine(call), AMPL_ErrorInfoGetOffset(call), \
                                 AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_NO_DATA_EXCEPTION: \
      throw NoDataException(AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_EXCEPTION: \
      throw AMPLException(AMPL_ErrorInfoGetSource(call), AMPL_ErrorInfoGetLine(call), AMPL_ErrorInfoGetOffset(call), \
                          AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_RUNTIME_ERROR: \
      throw std::runtime_error(AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_LOGIC_ERROR: \
      throw std::logic_error(AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_OUT_OF_RANGE: \
      throw std::out_of_range(AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_INVALID_ARGUMENT: \
       throw std::invalid_argument(AMPL_ErrorInfoGetMessage(call)); \
    case AMPL_STD_EXCEPTION: { \
      throw StdException(AMPL_ErrorInfoGetMessage(call)); \
    } } \
  } } while (0)


#endif  // AMPL_MACROS_H_
