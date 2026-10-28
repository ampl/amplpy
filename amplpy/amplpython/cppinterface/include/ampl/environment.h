#ifndef AMPL_ENVIRONMENT_H
#define AMPL_ENVIRONMENT_H

#include "ampl/cstringref.h"
#include "ampl/environment_c.h"
#include "ampl/ampl_c.h"

namespace ampl {

/**
 * This class provides access to the environment variables and provides
 * facilities to specify where to load the underlying %AMPL interpreter.
 */
class Environment {
  friend class AMPL;

 private:
  AMPL_ENVIRONMENT *impl_;

 public:
  /**
   * \rst
   * Default constructor
   * \endrst
   */
  Environment() {
    AMPL_EnvironmentCreate(&impl_, "", "");
  }

  /**
   * \rst
   * Copy constructor
   * \endrst
   */
  Environment(const Environment& other) {
    AMPL_EnvironmentCopy(&impl_, other.impl_);
  }

  /**
   * Assignment operator
   */
  Environment& operator=(const Environment& other) {
    AMPL_ENVIRONMENT *newimpl;
    AMPL_EnvironmentCopy(&newimpl, other.impl_);
    AMPL_EnvironmentFree(&impl_);
    impl_ = newimpl;
    return (*this);
  }

  /**
   * \rst
   * Constructor with ability to select the location of the AMPL binary.
   * Note that if this constructor is used, the automatic lookup for an AMPL
   * executable
   * will not be executed.
   * \endrst
   * \param binaryDirectory The directory in which look for the %AMPL Binary
   * \param binaryName The name of the %AMPL executable if other than "ampl"
   */
  explicit Environment(fmt::CStringRef binaryDirectory,
                       fmt::CStringRef binaryName = "") {
    AMPL_EnvironmentCreate(&impl_, binaryDirectory.c_str(), binaryName.c_str());
  }

  /**
   * Destructor
   */
  ~Environment() {
    if(impl_) {
      AMPL_EnvironmentFree(&impl_);
    }
   }

  /**
   * Add an environment variable to the environment, or change its value
   * if already defined
   * \param name name of the environment variable
   * \param value value to be assigned
   */
  void put(fmt::CStringRef name, fmt::CStringRef value) {
    AMPL_EnvironmentAddEnvironmentVariable(
        impl_, name.c_str(), value.c_str());
  }

  /**
   * Set the location where %AMPLAPI will search for the %AMPL executable.
   * \param binaryDirectory Directory
   */
  void setBinDir(fmt::CStringRef binaryDirectory) {
    AMPL_EnvironmentSetBinaryDirectory(
        impl_, binaryDirectory.c_str());
  }

  /**
   * Get the location where AMPLAPI will search for the %AMPL executable
   */
  std::string getBinDir() const {
    char *bindir;
    AMPL_EnvironmentGetBinaryDirectory(impl_, &bindir);
    std::string ret(bindir);
    return ret;
  }

  /**
   * Get the interpreter that will be used for an AMPL object constructed
   * using this environment
   */
  std::string getAMPLCommand() const {
    char *amplCommand;
    AMPL_EnvironmentGetAMPLCommand(impl_, &amplCommand);
    std::string ret(amplCommand);
    return ret;
  }

  /**
   * Set the name of the %AMPL executable
   * \param binaryName Executable
   */
  void setBinName(fmt::CStringRef binaryName) {
    AMPL_EnvironmentSetBinaryName(impl_, binaryName.c_str());
  }

  /**
   * Get the name of the %AMPL executable
   */
  std::string getBinName() const {
    char *binname;
    AMPL_EnvironmentGetBinaryName(impl_, &binname);
    std::string ret(binname);
    return ret;
  }

  /**
   * \rst
   * Print all variables in the map
   * \endrst
   */
  std::string toString() const {
    char *cstr;
    AMPL_EnvironmentToString(impl_, &cstr);
    std::string ret(cstr);
    AMPL_StringFree(&cstr);
    return ret;
  }

  class iterator {
    private:
      const AMPL_ENVIRONMENTVAR *current_;
    public:
      iterator() : current_() {}
      explicit iterator(const AMPL_ENVIRONMENTVAR *envVar) : current_(envVar) {}
      const AMPL_ENVIRONMENTVAR& operator*() const { return *current_; }
      const AMPL_ENVIRONMENTVAR* operator->() const { return current_; }
      iterator& operator++() { ++current_; return *this; }
      iterator operator++(int) { iterator temp = *this; ++current_; return temp; }
      bool operator==(const iterator& other) const { return current_ == other.current_; }
      bool operator!=(const iterator& other) const { return current_ != other.current_; }
      std::string getName() const { std::string name(current_->name); return name; }
      std::string getValue() const { std::string value(current_->value); return value; }
  };

  /**
   * Iterator for the map
   */

  /**
   * Returns an iterator pointing to the first environment variable in the map.
   */
  iterator begin() const {
    AMPL_ENVIRONMENTVAR *pointer;
    AMPL_EnvironmentGetEnvironmentVar(impl_, &pointer);
    return iterator(pointer);
  }

  /**
   * Returns an iterator pointing to the past-the-end element in the map.
   */
  iterator end() const {
    AMPL_ENVIRONMENTVAR *pointer;
    size_t size;
    AMPL_EnvironmentGetEnvironmentVar(impl_, &pointer);
    AMPL_EnvironmentGetSize(impl_, &size);
    return iterator(pointer+size);
  }

  /**
   * Searches the current object for an environment variable called name and
   * returns an iterator to it if found, otherwise it returns an iterator to
   * Environment::end.
   */
  iterator find(fmt::CStringRef name) const {
    AMPL_ENVIRONMENTVAR *pointer;
    AMPL_EnvironmentFindEnvironmentVar(impl_, name.c_str(), &pointer);
    return iterator(pointer);
  }

  /**
   * Returns the size of the map.
   */
  std::size_t size() const {
    size_t size;
    AMPL_EnvironmentGetSize(impl_, &size);
    return size;
  }
};
}  // namespace ampl

#endif  // AMPL_ENVIRONMENT_H
