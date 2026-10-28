#ifndef AMPL_RUNNABLE_H
#define AMPL_RUNNABLE_H

namespace ampl {
/**
 * Represent an object with only one function, which is called
 * as a callback after an async execution has finished.
 * Inherit from this class and use an instance in AMPL::evalAsync(),
 * AMPL::readAsync(), AMPL::readDataAsync(), AMPL::solveAsync().
 */
class Runnable {
 public:
  /**
   * Destructor
   */
  virtual ~Runnable() {}

  /**
   * Function called when the execution of the async operation
   * is finished
   */
  virtual void run() = 0;
};

}  // namespace ampl

#endif  // AMPL_RUNNABLE_H
