#ifndef AMPL_AMPL_H
#define AMPL_AMPL_H

#include "ampl/ampl_c.h"
#include "ampl/cstringref.h"
#include "ampl/dataframe.h"
#include "ampl/entity.h"
#include "ampl/entitymap.h"
#include "ampl/environment.h"
#include "ampl/declarations.h"
#include "ampl/macros.h"
#include "ampl/errorhandler.h"
#include "ampl/optional.h"
#include "ampl/output.h"
#include "ampl/runnable.h"
#include "ampl/string.h"
#include "ampl/tuple.h"

#ifdef __GNUC__
#define AMPL_DEPRECATED(func) func __attribute__((deprecated))
#else
#define AMPL_DEPRECATED(func) func
#endif

namespace ampl {
/*!
 * An %AMPL translator.
 *
 * An object of this class can be used to do the following tasks:
 *
 * <ul>
 * <li>Run %AMPL code. See eval().
 * <li>Read models and data from files. See read() and readData().
 * <li>Solve optimization problems constructed from model and data (see
 * solve()).
 * <li>Access single Elements of an optimization problem. See getVariable(),
 * getObjective(), getConstraint(), getSet() and getParameter().
 * <li>Access lists of available entities of an optimization problem. See
 * getVariables(), getObjectives(), getConstraints(), getSets() and
 * getParameters().
 * </ul>
 *
 * %AMPL stores one or more problems which may consume substantial amount of
 * memory. The AMPL object has a destructor which automaticallly closes the
 * underlying %AMPL interpreter and deletes all C++ entitites linked to it.
 * Some entities (notably all instances of DataFrame and DataFrame::Slice) are
 * not owned by the %AMPL object and are not therefore deleted. <p> The
 * initialization of the C++ representation of the %AMPL entities (any class
 * derived from ampl::Entity) is lazy and consists of two steps. When a
 * function listing available Elements is called, only a shallow list with
 * names, types and declarations of the Elements is populated. The same happens
 * when a reference to a C++ representation of one entity is obtained (through
 * a call to any other single entity factory function).
 * When accessing any instance of an entity (through the methods
 * 'get' of any class), the (memory hungry) list of instances for that entity is
 * created.
 * <p>
 * Consistency is maintained automatically. Any command issued to the translator
 * through eval and similar functions invalidates all entities,
 * and any further access to any entity will require communication between the
 * native translator and the C++ code. Conversely, any operation called through
 * the C++ equivalent function, like fixing variables or solving the model will
 * invalidate only the entities involved. A list of dependencies between
 * entities is automatically updated.
 * <p>
 * Error handling is two-faced:
 * <ul>
 * <li>Errors coming from the underlying %AMPL translator (e.g. syntax errors
 * and warnings obtained calling the eval method) are handled by the
 * ErrorHandler which can be set and get via getErrorHandler() and
 * setErrorHandler(). <li>Generic errors coming from misusing the API, which are
 * detected in C++, are thrown as exceptions.
 * </ul>
 * The default implementation of the error handler throws exceptions on errors
 * and prints to console on warnings.
 * <p>
 * The output of every user interaction with the underlying translator is
 * handled implementing the abstract class ampl::OutputHandler. The (only)
 * method is called at each block of output from the translator. The current
 * output handler can be accessed and set via AMPL::getOutputHandler()
 * and AMPL::setOutputHandler().
 */

class AMPL {
 public:
  /*!
   * Default constructor: creates a new AMPL instance with the default
   * environment.
   *
   * @throws std::runtime_error
   *             If no valid %AMPL license has been found or
   *             if the translator cannot be started for any other reason.
   */
  AMPL() { AMPL_CALL_CPP_W_FREE(AMPL_Create(&ampl_)); }

  /*!
   * Constructor: creates a new AMPL instance with the specified environment.
   * This allows the user to specify the location of the %AMPL binaries to be
   * used and to modify the environment variables in which the %AMPL interpreter
   * will run
   *
   * @throws std::runtime_error
   *             If no valid %AMPL license has been found or
   *             if the translator cannot be started for any other reason.
   */
  AMPL(const Environment& e) {
    AMPL_CALL_CPP_W_FREE(AMPL_CreateWithEnv(&ampl_, e.impl_));
  }

  /** Default destructor
   * Releases all the resources related to the AMPL instance (most notably kills
   * the underlying  interpreter.
   */
  ~AMPL() { AMPL_Free(&ampl_); }

  /**
   Get the data corresponding to the display statements. The statements can
   be %AMPL expressions, or entities. It captures the equivalent of the
   command:

   \rst
   .. code-block:: ampl

     display ds1, ..., dsn;

   where ``ds1, ..., dsn`` are the ``displayStatements`` with which the
   function is called.
   \endrst
   <p>
   As only one DataFrame is returned, the operation will fail if the results
   of the display statements cannot be indexed over the same set. As a
   result, any attempt to get data from more than one set, or to get data
   for multiple parameters with a different number of indexing sets will
   fail.

   @throws AMPLException
               if the %AMPL visualization command does not succeed for one of
               the reasons listed above.
   \param statements
              The display statements to be fetched.
   \return DataFrame capturing the output of the display
           command in tabular form.
  */
  DataFrame getData(StringArgs statements) const {
    AMPL_DATAFRAME *df;
    AMPL_CALL_CPP(AMPL_GetData(ampl_, statements.args(), statements.size(), &df));
    DataFrame output(df);

    return output;
  }

  /**
   * Take a snapshot of the AMPL session.
   * \param fileName
   *              The file where to write the snapshot to.
   * \param model
   *              Include model if set to true.
   * \param data
   *              Include data if set to true.
   * \param options
   *              Include options if set to true.
   */
  std::string snapshot(fmt::CStringRef fileName = "", bool model = true,
                       bool data = true, bool options = true) const {
    char *output;
    AMPL_CALL_CPP(AMPL_Snapshot(ampl_, fileName.c_str(), model, data, options, &output));
    std::string result(output);
    AMPL_StringFree(&output);
    return result;
  }

  /**
   * Get the declarations that were made in the current AMPL instance
   */
  std::string exportModel() const {
    char *output;
    AMPL_CALL_CPP(AMPL_ExportModel(ampl_, "", &output));
    std::string result(output);
    AMPL_StringFree(&output);
    return result;
  }

  /**
   * Write the declarations that were made in the current AMPL instance
   * to a file
   * \param fileName
   *              The file where to write the declarations to
   */
  void exportModel(fmt::CStringRef fileName) const {
    char *output;
    AMPL_CALL_CPP(AMPL_ExportModel(ampl_, fileName.c_str(), &output));
    AMPL_StringFree(&output);
  }

  /**
   * Get all data loaded in the current instance
   */
  std::string exportData() const {
    char *output;
    AMPL_CALL_CPP(AMPL_ExportData(ampl_, "", &output));
    std::string result(output);
    AMPL_StringFree(&output);
    return result;
  }

  /**
   * Write all data loaded in the current instance to a file.
   * \param dataFileName
   *              The file where to write the data to
   */
  void exportData(fmt::CStringRef dataFileName) {
    char *output;
    AMPL_CALL_CPP(AMPL_ExportData(ampl_, dataFileName.c_str(), &output));
    AMPL_StringFree(&output);
  }

  /**
   * Get entity corresponding to the specified name (looks for it in all types
   * of entities)
   *
   * \param name
   *            Name of the entity
   * \throws std::out_of_range exception if the specified entity does not exist
   * \return The %AMPL entity with the specified name
   */
  Entity getEntity(fmt::CStringRef name) const {
    return Entity(ampl_, name.c_str());
  }

  /**
   * Get the variable with the corresponding name
   * \param name Name of the variable to be found
   * \throws std::out_of_range exception if the specified variable does not
   * exist
   **/
  Variable getVariable(fmt::CStringRef name) const {
    return Variable(ampl_, name.c_str());
  }

  /**
   * Get the constraint with the corresponding name
   * \param name Name of the constraint to be found
   * \throws std::out_of_range exception if the specified constraint does not
   *exist
   **/
  Constraint getConstraint(fmt::CStringRef name) const {
    return Constraint(ampl_, name.c_str());
  }

  /**
   * Get the objective with the corresponding name
   * \param name Name of the objective to be found
   * \throws An std::out_of_range exception if the specified objective does not
   *exist
   **/
  Objective getObjective(fmt::CStringRef name) const {
    return Objective(ampl_, name.c_str());
  }

  /**
   * Get the set with the corresponding name
   * \param name Name of the set to be found
   * \throws std::out_of_range exception if the specified set does not exist
   **/
  Set getSet(fmt::CStringRef name) const {
    return Set(ampl_, name.c_str());
  }

  /**
   * Get the parameter with the corresponding name
   * \param name Name of the parameter to be found
   * \throws std::out_of_range exception if the specified parameter does not
   *exist
   **/
  Parameter getParameter(fmt::CStringRef name) const {
    return Parameter(ampl_, name.c_str());
  }

  /**
   * Parses %AMPL code and evaluates it as a possibly empty sequence of %AMPL
   * declarations and statements.
   * <p>
   * As a side effect, it invalidates all entities (as the passed statements
   * can contain any arbitrary command); the lists of entities will be
   * re-populated lazily (at first access)
   * <p>
   * The output of interpreting the statements is passed to the current
   * OutputHandler (see getOutputHandler and
   * setOutputHandler).
   * <p>
   * By default, errors are reported as exceptions and warnings are printed on
   * stdout. This behavior can be changed reassigning an
   * ErrorHandler using setErrorHandler.
   *
   * \param amplstatements
   *            A collection of %AMPL statements and declarations to be
   *            passed to the interpreter
   * @throws std::runtime_error
   *             if the input is not a complete %AMPL statement (e.g.
   *             if it does not end with semicolon) or if the underlying
   *             interpreter is not running
   */
  void eval(fmt::CStringRef amplstatements) {
    AMPL_CALL_CPP(AMPL_Eval(ampl_, amplstatements.c_str()));
  }

  /**
   * Clears all entities in the underlying %AMPL interpreter, clears all maps
   * and invalidates all entities
   */
  void reset() { AMPL_CALL_CPP(AMPL_Reset(ampl_)); }

  /**
   * Clears all data.
   */
  void resetData() { AMPL_CALL_CPP(AMPL_ResetData(ampl_)); }

  /**
   * Resets all options to their default values.
   * Equivalent to the AMPL statement: ``reset options;``
   */
  void resetOptions() { AMPL_CALL_CPP(AMPL_ResetOptions(ampl_)); }

  /**
   * Stops the underlying engine, and release all any further attempt to execute
   * optimisation
   * commands without restarting it will throw an exception.
   */
  void close() { AMPL_CALL_CPP(AMPL_Close(ampl_)); }

  /**
   * Returns true if the underlying engine is running
   */
  bool isRunning() const {
    bool running;
    AMPL_CALL_CPP(AMPL_IsRunning(ampl_, &running));
    return running;
  }

  /**
   * Returns true if the underlying engine is doing an async operation
   */
  bool isBusy() const {
    bool busy;
    AMPL_CALL_CPP(AMPL_IsBusy(ampl_, &busy));
    return busy;
  }

  /**
   * Solve the current model
   * @throws std::runtime_error If the underlying interpreter is not running
   *
   */
  void solve(fmt::CStringRef problem = "", fmt::CStringRef solver = "") { 
    AMPL_CALL_CPP(AMPL_Solve(ampl_, problem.c_str(), solver.c_str())); 
  }

  /**
   * Interprets the specified file asynchronously, interpreting it as a model
   * or a script file. As a side effect, it invalidates all entities (as the
   * passed file can contain any arbitrary command); the lists of entities
   * will be re-populated lazily (at first access)
   *
   * \param filename
   *            Path to the file (Relative to the current working directory or
   *            absolute)
   * \param cb
   *            Callback to be executed when the file has been interpreted
   */
  void readAsync(fmt::CStringRef filename, Runnable* cb) {
    auto runCallback = [](void *cb) -> void {
      static_cast<Runnable *>(cb)->run(); };
    AMPL_CALL_CPP(AMPL_ReadAsync(ampl_, filename.c_str(),
                                  runCallback, cb));
  }

  /**
   * Interprets the specified data file asynchronously. When interpreting is
   * over, the specified callback is called. The file is interpreted as data.
   * As a side effect, it invalidates all entities (as the passed file can
   * contain any arbitrary command); the lists of entities will be
   * re-populated lazily (at first access)
   *
   * \param filename
   *            Full path to the file
   * \param cb
   *            Callback to be executed when the file has been interpreted
   */
  void readDataAsync(fmt::CStringRef filename, Runnable* cb) {
    auto runCallback = [](void *cb) -> void {
      static_cast<Runnable *>(cb)->run(); };
    AMPL_CALL_CPP(AMPL_ReadDataAsync(ampl_, filename.c_str(),
                                      runCallback, cb));
  }

  /**
   * Interpret the given %AMPL statement
   * Throws runtime_error if the underlying ampl interpreter is not running
   */
  void evalAsync(fmt::CStringRef amplstatement, Runnable* cb) {
    auto runCallback = [](void *cb) -> void {
      static_cast<Runnable *>(cb)->run(); };
    AMPL_CALL_CPP(AMPL_EvalAsync(ampl_, amplstatement.c_str(),
                                  runCallback, cb));
  }

  /**
   * Solve the current model asynchronously
   *
   * \param cb
   *            Object encapsulating the function to be called when solver is
   *            done
   */
  void solveAsync(Runnable* cb) {
    auto runCallback = [](void *cb) -> void {
      static_cast<Runnable *>(cb)->run(); };
    AMPL_CALL_CPP(AMPL_SolveAsync(ampl_, runCallback, cb));
  }

  /**
   * Interrupt an underlying asynchronous operation (execution of %AMPL code by
   * the %AMPL interpreter). An asynchronous operation can be started via
   * evalAsync(), solveAsync(), readAsync() and readDataAsync(). Does nothing if
   * the engine and the solver are idle.
   */
  void interrupt() {
    AMPL_CALL_CPP(AMPL_Interrupt(ampl_));
  }

  /**
   * Get the current working directory from the underlying interpreter (see
   * https://en.wikipedia.org/wiki/Working_directory ).
   *
   * \return Current working directory
   */
  std::string cd() const {
    char *output;
    AMPL_CALL_CPP(AMPL_Cd(ampl_, &output));
    std::string result(output);
    AMPL_StringFree(&output);
    return result;
  }

  /**
   * Change or display the current working directory (see
   * https://en.wikipedia.org/wiki/Working_directory ).
   *
   * \param path
   *            New working directory or null (to display the working
   *            directory)
   * \return Current working directory
   */
  std::string cd(fmt::CStringRef path) {
    char *output;
    AMPL_CALL_CPP(AMPL_Cd2(ampl_, path.c_str(), &output));
    std::string result(output);
    AMPL_StringFree(&output);
    return result;
  }

  /**
   * Set an %AMPL option to a specified value.
   *
   * \param name
   *            Name of the option to be set (alphanumeric without spaces)
   * \param value
   *            String representing the value the option must be set to
   * @throws std::invalid_argument
   *             if the option name is not valid
   */
  void setOption(fmt::CStringRef name, fmt::CStringRef value) {
    AMPL_CALL_CPP(AMPL_SetOption(ampl_, name.c_str(), value.c_str()));
  }

  /**
   * Get the current value of the specified option. If the option does not
   * exist, the returned Optional object will not have value.
   * Usage:
   * if (auto value = ampl.getOption("solver"))
   *		value.get();
   *
   * \param name
   *            Option name (alphanumeric)
   * \return Value of the option as a string.
   * @throws std::invalid_argument
   *             if the option name is not valid
   */
  Optional<std::string> getOption(fmt::CStringRef name) const {
    bool exists;
    char *value;
    AMPL_CALL_CPP(AMPL_GetOption(ampl_, name.c_str(), &exists, &value));
    std::string result(value);
    AMPL_StringFree(&value);
    return exists ? Optional<std::string>(result) : Optional<std::string>();
  }

  /**
   * Get the current value of the specified integer option.
   * If the option does not exist, the returned Optional object will not have
   * value.
   *
   * \param name
   *            Option name (alphanumeric)
   * \return Value of the option (integer)
   * @throws std::invalid_argument
   *             if the option name is not valid
   * @throws std::invalid_argument
   *             If the option did not have a value which could be casted to
   *             integer
   */
  Optional<int> getIntOption(fmt::CStringRef name) const {
    bool exists;
    int result;
    AMPL_CALL_CPP(AMPL_GetIntOption(ampl_, name.c_str(), &exists, &result));
    return exists ? Optional<int>(result) : Optional<int>();
  }

  /**
   * Set an %AMPL option to a specified integer value.
   *
   * \param name
   *            Name of the option to be set
   * \param value
   *            The integer value the option must be set to
   * @throws std::invalid_argument
   *             if the option name is not valid
   */
  void setIntOption(fmt::CStringRef name, int value) {
    setDblOption(name, value);
  }

  /**
   * Get the current value of the specified double option
   * If the option does not exist, the returned Optional object
   * will not have value.
   * \param name
   *            Option name
   * \return Value of the option (double)
   * @throws std::invalid_argument
   *             if the option name is not valid
   * @throws std::invalid_argument
   *             If the option did not have a value which could be casted to
   *             double
   */
  Optional<double> getDblOption(fmt::CStringRef name) const {
    bool exists;
    double result;
    AMPL_CALL_CPP(AMPL_GetDblOption(ampl_, name.c_str(), &exists, &result));
    return exists ? Optional<double>(result) : Optional<double>();
  }

  /**
   * Set an %AMPL option to a specified double value.
   *
   * \param name
   *            Name of the option to be set
   * \param value
   *            The double value the option must be set to
   * @throws std::invalid_argument
   *             if the option name is not valid
   */
  void setDblOption(fmt::CStringRef name, double value) {
    AMPL_CALL_CPP(AMPL_SetDblOption(ampl_, name.c_str(), value));
  }

  /**
   * Get the current value of the specified boolean option. In AMPL, boolean
   * options are represented as integer: 0 for false, 1 for true.
   * If the option does not exist, the returned Optional object will not
   * have value.
   *
   * \param name
   *            Option name
   * \return Value of the option (boolean)
   * @throws std::invalid_argument
   *             if the option name is not valid
   * @throws std::invalid_argument
   *             If the option did not have a value which could be casted to
   *             boolean
   */
  Optional<bool> getBoolOption(fmt::CStringRef name) const {
    bool exists;
    bool result;
    AMPL_CALL_CPP(AMPL_GetBoolOption(ampl_, name.c_str(), &exists, &result));

    return exists ? Optional<bool>(result) : Optional<bool>();
  }

  /**
   * Get the name of the currently active objective
   * (see the ``objective`` command)
   * \return Current objective or empty string if no objective
   * has been declared
   */
  std::string getCurrentObjectiveName() {
    char *currentObjective;
    AMPL_CALL_CPP(AMPL_GetCurrentObjective(ampl_, &currentObjective));
    std::string result(currentObjective);
    AMPL_StringFree(&currentObjective);
    return result;
  }

  /**
   * Set an %AMPL option to a specified boolean value. Note that in AMPL,
   * boolean options are represented as integer: 0 for false, 1 for true
   *
   * \param name
   *            Name of the option to be set
   * \param value
   *            The boolean value the option must be set to
   * @throws std::invalid_argument
   *             if the option name is not valid
   */
  void setBoolOption(fmt::CStringRef name, bool value) {
    AMPL_CALL_CPP(AMPL_SetBoolOption(ampl_, name.c_str(), value));
  }

  /**
   Interprets the specified file (script or model or mixed) As a side effect,
   it invalidates all entities (as the passed file can contain any arbitrary
   command); the lists of entities will be re-populated lazily (at first
   access)
   \param	fileName	Full path to the file.
   \throws	runtime_error	In case the file does not exist.
   */
  void read(fmt::CStringRef fileName) {
    AMPL_CALL_CPP(AMPL_Read(ampl_, fileName.c_str()));
  }

  /**
   Interprets the specified file as an %AMPL data file. As a side effect, it
   invalidates all entities (as the passed file can contain any arbitrary
   command); the lists of entities will be re-populated lazily (at first
   access). After reading the file, the interpreter is put back to "model"
   mode.
   \param	fileName	Full path to the file.
   \throws	std::runtime_error	In case the file does not exist.
   */
  void readData(fmt::CStringRef fileName) {
    AMPL_CALL_CPP(AMPL_ReadData(ampl_, fileName.c_str()));
  }

  /**
   Get a scalar value from the underlying %AMPL interpreter, as a double or a
   string.
   \param	scalarExpression	An %AMPL expression which evaluates to a
   scalar value. 
   \return	A Variant which represent the value of the expression.
   */
  Variant getValue(fmt::CStringRef scalarExpression) const {
    AMPL_VARIANT *v;
    AMPL_CALL_CPP(AMPL_GetValue(ampl_, scalarExpression.c_str(), &v));
    Variant vpp = Variant::getVar(v);
    AMPL_VariantFree(&v);
    return vpp;
  }

  /**
  Equivalent to eval() but returns the output as a string.
  \return	A std::string with the output.
  */
  std::string getOutput(fmt::CStringRef amplstatement) {
    char *output;
    AMPL_CALL_CPP(AMPL_GetOutput(ampl_, amplstatement.c_str(), &output));
    std::string result(output);
    AMPL_StringFree(&output);
    return result;
  }

  /**
   Assign the data in the dataframe to the %AMPL entities with the names
   corresponding to the column names. If setName is null, only the
   parameters value will be assigned.

   \param	df	   	The dataframe containing the data to be
   assigned. \param	setName	The name of the set to which the indices values
   of the DataFrame are to be assigned. \throws	AMPLException	If the data
   assignment procedure was not successful.
   */
  void setData(const DataFrame& df, fmt::CStringRef setName = "") {
    AMPL_CALL_CPP(AMPL_SetData(ampl_, df.impl(), setName.c_str()));
  }

  /**
   Get a string describing the object. Returns the version of the API and
   either the version of the interpreter or the message "AMPL is not
   running" if the interpreter is not running (e.g. due to unexpected
   internal error or to a call AMPL::close)
   \return	A std::string that represents this object.
   */
  std::string toString() const {
    char *output;
    AMPL_CALL_CPP(AMPL_ToString(ampl_, &output));
    std::string result(output);
    AMPL_StringFree(&output);
    return result;
  }

  /**
   Get a string with the expand message of the model.
   \return	A std::string that represents the expand message.
   */
  std::string expand() const {
    char *output;
    AMPL_CALL_CPP(AMPL_Expand(ampl_, &output));
    std::string result(output);
    AMPL_StringFree(&output);
    return result;
  }

  /**
   Get a string with the show message.
   \return	A std::string that represents the show message.
   */
  std::string show() const {
    char *output;
    AMPL_CALL_CPP(AMPL_Show(ampl_, &output));
    std::string result(output);
    AMPL_StringFree(&output);
    return result;
  }

  /**
   Read the table corresponding to the specified name, equivalent to the
   %AMPL statement:

   \rst
   .. code-block:: ampl

     read table tableName;

   \endrst

   \param	tableName	Name of the table to be read.
  */
  void readTable(fmt::CStringRef tableName) {
    AMPL_CALL_CPP(AMPL_ReadTable(ampl_, tableName.c_str()));
  }

  /**
   Write the table corresponding to the specified name, equivalent to the
   %AMPL statement

   \rst
   .. code-block:: ampl

     write table tableName;

   \endrst

   \param	tableName	 Name of the table to be written.
   */
  void writeTable(fmt::CStringRef tableName) {
    AMPL_CALL_CPP(AMPL_WriteTable(ampl_, tableName.c_str()));
  }

  /**
  Write model instances. equivalent to

  \rst
  .. code-block:: ampl

    option auxfiles auxfiles;
    write filename;

  \endrst

  \param	filename	The name of the file to write; the first letter
  indicates which filetype to write (see the output of ``ampl -o?``) \param
  auxfiles   The auxiliary files to write. Most notably, 'cr' instructs %AMPL to
  write out column and row names respectively \throws	PresolveException if the
  model is not exported because of the presolver (most notably if the model is
  trivial) \throws  InfeasibilityException if the model is not exported because
  detected infeasible by the presolver
  */
  void write(fmt::CStringRef filename, fmt::CStringRef auxfiles = nullptr) {
    AMPL_CALL_CPP(AMPL_Write(ampl_, filename.c_str(), auxfiles.c_str()));
  }

  /**
   Writes on the current OutputHandler the outcome of the %AMPL statement

   \rst
   .. code-block:: ampl

     display e1, e2, .., en;

   where ``e1...en`` are the strings passed to the procedure.
   \endrst

   \param	amplExpressions	Expressions to be evaluated.
   */
  void display(StringArgs amplExpressions) {
    AMPL_CALL_CPP(AMPL_CallVisualisationCommandOnNames(ampl_, "display", amplExpressions.args(), amplExpressions.size()));
  }

  /**
  Writes on the current OutputHandler the outcome of the %AMPL statement
  \rst
  .. code-block:: ampl

    display e1, e2, .., en;

  where ``e1...en`` are the objects passed to the procedure.
  \endrst
  \param	entities	The entities to display
  */
  void display(EntityArgs entities) {
    std::vector<const char*> names(entities.size());
    for (std::size_t i = 0; i < entities.size(); i++) {
      names[i] = entities.getArgs()[i].name_.c_str();
    }
  
    AMPL_CALL_CPP(AMPL_CallVisualisationCommandOnNames(ampl_, "display", &names[0], entities.size()));
  }

  /**
  Writes on the current OutputHandler the outcome of the %AMPL statement
  \rst
  .. code-block:: ampl

    show e1, e2, .., en;

  where ``e1...en`` are the objects passed to the procedure.
  \endrst
  \param	entities	The entities to show
  */
  void show(EntityArgs entities) {
    std::vector<const char*> names(entities.size());
    for (std::size_t i = 0; i < entities.size(); i++) {
      names[i] = entities.getArgs()[i].name_.c_str();
    }
  
    AMPL_CALL_CPP(AMPL_CallVisualisationCommandOnNames(ampl_, "show", &names[0], entities.size()));
  }

  /**
   Writes on the current OutputHandler the outcome of the %AMPL statement
   \rst
   .. code-block:: ampl

     expand e1, e2, .., en;

   where ``e1...en`` are the objects passed to the procedure.
   \endrst
   \param	entities	The entities to expand
  */
  void expand(EntityArgs entities) {
    std::vector<const char*> names(entities.size());
    for (std::size_t i = 0; i < entities.size(); i++) {
      names[i] = entities.getArgs()[i].name_.c_str();
    }
  
    AMPL_CALL_CPP(AMPL_CallVisualisationCommandOnNames(ampl_, "expand", &names[0], entities.size()));
  }

  /**
   Sets a new output handler
   \param [in]	outputhandler	The function handling the %AMPL output derived
   from interpreting user commands.
   */
  void setOutputHandler(OutputHandler* outputhandler) {
    auto myCallback = [](AMPL_OUTPUTKIND kind, const char *msg, void *oh) -> void {
      static_cast<OutputHandler *>(oh)->output(static_cast<ampl::output::Kind>(kind), msg); };
    AMPL_CALL_CPP(AMPL_SetOutputHandler(ampl_, myCallback, outputhandler)); 
  }

  /**
   Sets a new error handler Note that the ownership of the error handling
   object remains of the caller.
   \param [in]	errorhandler	The object handling %AMPL errors and warnings.
   */
  void setErrorHandler(ErrorHandler* errorhandler) {
    auto myCallback = [](bool isWarning, const char *filename,
                                        int row, int offset,
                                        const char *message, void *eh) -> void {
    ampl::AMPLException e(filename, row, offset, message);
    if (isWarning)
      static_cast<ErrorHandler *>(eh)->warning(e);
    else
      static_cast<ErrorHandler *>(eh)->error(e);};

    AMPL_CALL_CPP(AMPL_SetErrorHandler(ampl_, myCallback, errorhandler));
  }

  /**
   Get the current output handler.
   \return	A pointer to the current output handler.
   */
  OutputHandler* getOutputHandler() const {
    void *usrdata;
    AMPL_CALL_CPP(AMPL_GetOutputHandler(ampl_, &usrdata));
    return static_cast<OutputHandler*>(usrdata);
  }

  /**
   Get the current error handler.
   \return	A pointer to the current error handler.
   */
  ErrorHandler* getErrorHandler() const {
    void *usrdata;
    AMPL_CALL_CPP(AMPL_GetErrorHandler(ampl_, &usrdata));
    return static_cast<ErrorHandler*>(usrdata);
  }

  /**
   * Get all the variables declared.
   */
  EntityMap<Variable> getVariables() const {
    return ampl::EntityMap<ampl::Variable>(ampl_, AMPL_VARIABLE);
  }

  /**
   * Get all the constraints declared.
   */
  EntityMap<Constraint> getConstraints() const {
    return ampl::EntityMap<ampl::Constraint>(ampl_, AMPL_CONSTRAINT);
  }

  /**
   * Get all the objectives declared.
   */
  EntityMap<Objective> getObjectives() const {
    return ampl::EntityMap<ampl::Objective>(ampl_, AMPL_OBJECTIVE);
  }

  /**
   * Get all the sets declared.
   */
  EntityMap<Set> getSets() const {
    return ampl::EntityMap<ampl::Set>(ampl_, AMPL_SET);
  }

  /**
   * Get all the parameters declared.
   */
  EntityMap<Parameter> getParameters() const {
    return ampl::EntityMap<ampl::Parameter>(ampl_, AMPL_PARAMETER);
  }

  /**
  Function to easily add a directory to the current process' system path
  */
  static void addToPath(fmt::CStringRef path) {
    AMPL_AddToPath(path.c_str());
    //internal::Util_Impl_addToPath(path.c_str(), internal::ErrorInfo());
  }

 private:
  ::AMPL *ampl_;
  // deny copy constructor and assignment
  AMPL(const AMPL&) {}
  AMPL& operator=(const AMPL&) { return *this; }
};
}  // namespace ampl

#endif  // AMPL_AMPL_H
