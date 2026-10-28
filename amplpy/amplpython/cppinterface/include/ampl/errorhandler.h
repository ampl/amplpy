#ifndef AMPL_ERRORHANDLER_H
#define AMPL_ERRORHANDLER_H

#include "ampl/amplexception.h"

namespace ampl {
/**
 * A basic interface for %AMPL error handlers.
 *
 * If an application needs to implement customised error handling,
 * it must implement this interface and then register an instance with the
 * %AMPL API using the AMPL::setErrorHandler method. The underlying %AMPL
 * interpreter will then report all errors and warnings through this interface.
 */
class ErrorHandler {
 public:
  ErrorHandler() {}
  virtual ~ErrorHandler() {}
  /**
   * Receives notification of an error.
   */
  virtual void error(const AMPLException&) = 0;
  /**
   * Receives notification of a warning.
   */
  virtual void warning(const AMPLException&) = 0;
};

}  // namespace ampl

#endif  // AMPL_ERRORHANDLER_H
