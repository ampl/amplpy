# pip install autopxd2
# autopxd -I amplpy/amplpython/cppinterface/include/ amplpy/amplpython/cppinterface/include/ampl/ampl_c.h

# add except * to the end of ctypedef void (*ErrorHandlerCbPtr)(bool isWarning, const char* filename, int row, int offset, const char* message, void* errorHandler) except *
# add except * to the end of ctypedef void (*AMPL_OutputHandlerCb)(AMPL_OUTPUTKIND, const char*, void*) except *
# add except * to the end of AMPL_Eval(AMPL* ampl, const char* statement) except *

from libcpp cimport bool # add this line

cdef extern from "ampl/ampl_c.h":

    ctypedef enum AMPL_TYPE:
        AMPL_EMPTY
        AMPL_NUMERIC
        AMPL_STRING

    ctypedef enum AMPL_STRINGSUFFIX:
        AMPL_ASTATUS
        AMPL_SSTATUS
        AMPL_STATUS
        AMPL_MESSAGE
        AMPL_RESULT
        AMPL_SENSE

    ctypedef enum AMPL_NUMERICSUFFIX:
        AMPL_VALUE
        AMPL_DEFEQN
        AMPL_DUAL
        AMPL_INIT
        AMPL_INIT0
        AMPL_LB
        AMPL_UB
        AMPL_LB0
        AMPL_UB0
        AMPL_LB1
        AMPL_UB1
        AMPL_LB2
        AMPL_UB2
        AMPL_LRC
        AMPL_URC
        AMPL_LSLACK
        AMPL_USLACK
        AMPL_RC
        AMPL_SLACK
        AMPL_BODY
        AMPL_DEFVAR
        AMPL_DINIT
        AMPL_DINIT0
        AMPL_LBS
        AMPL_UBS
        AMPL_LDUAL
        AMPL_UDUAL
        AMPL_VAL
        AMPL_EXITCODE

    const char* NUMERICSUFFIXES[29]

    const char* STRINGSUFFIXES[6]

    #ctypedef AMPL_Args AMPL_ARGS
    ctypedef struct AMPL_ARGS:
        pass

    void retainArgs(AMPL_ARGS* args)

    void releaseArgs(AMPL_ARGS* args)

    int AMPL_ArgsCreateNumeric(AMPL_ARGS** args, const double* values)

    int AMPL_ArgsCreateString(AMPL_ARGS** args, const char* const* values)

    int AMPL_ArgsCopy(AMPL_ARGS** args, AMPL_ARGS* copy)

    int AMPL_ArgsDestroy(AMPL_ARGS** args)

    int AMPL_ArgsGetType(AMPL_ARGS* args, AMPL_TYPE* type)

    int AMPL_ArgsGetDblValues(AMPL_ARGS* args, const double** values)

    int AMPL_ArgsGetStrValues(AMPL_ARGS* args, const char* const** values)

    ctypedef enum AMPL_ERRORCODE:
        AMPL_EXCEPTION
        AMPL_LICENSE_EXCEPTION
        AMPL_FILE_IO_EXCEPTION
        AMPL_UNSUPPORTED_OPERATION_EXCEPTION
        AMPL_INVALID_SUBSCRIPT_EXCEPTION
        AMPL_SYNTAX_ERROR_EXCEPTION
        AMPL_NO_DATA_EXCEPTION
        AMPL_LOGIC_ERROR
        AMPL_RUNTIME_ERROR
        AMPL_INVALID_ARGUMENT
        AMPL_OUT_OF_RANGE
        AMPL_STD_EXCEPTION
        AMPL_PRESOLVE_EXCEPTION
        AMPL_INFEASIBILITY_EXCEPTION

    #ctypedef AMPL_ErrorInfo AMPL_ERRORINFO
    ctypedef struct AMPL_ERRORINFO:
        pass

    AMPL_ERRORCODE AMPL_ErrorInfoGetError(AMPL_ERRORINFO* error)

    char* AMPL_ErrorInfoGetMessage(AMPL_ERRORINFO* error)

    int AMPL_ErrorInfoGetLine(AMPL_ERRORINFO* error)

    int AMPL_ErrorInfoGetOffset(AMPL_ERRORINFO* error)

    char* AMPL_ErrorInfoGetSource(AMPL_ERRORINFO* error)

    ctypedef void (*ErrorHandlerCbPtr)(bool isWarning, const char* filename, int row, int offset, const char* message, void* errorHandler) except *

    #ctypedef AMPL_Variant AMPL_VARIANT
    ctypedef struct AMPL_VARIANT:
        pass

    void retainVariant(AMPL_VARIANT* v)

    void releaseVariant(AMPL_VARIANT* v)

    int AMPL_VariantCreateEmpty(AMPL_VARIANT** v)

    int AMPL_VariantCreateNumeric(AMPL_VARIANT** v, double value)

    int AMPL_VariantCreateString(AMPL_VARIANT** v, const char* cstr)

    int AMPL_VariantCopy(AMPL_VARIANT** v, AMPL_VARIANT* copy)

    int AMPL_VariantFree(AMPL_VARIANT** v)

    int AMPL_VariantCompare(AMPL_VARIANT* v1, AMPL_VARIANT* v2)

    int AMPL_VariantGetNumericValue(AMPL_VARIANT* v, double* value)

    int AMPL_VariantGetStringValue(AMPL_VARIANT* v, char** value)

    int AMPL_VariantGetType(AMPL_VARIANT* v, AMPL_TYPE* type)

    int AMPL_VariantFormat(AMPL_VARIANT* v, char** cstr)

    #ctypedef AMPL_Tuple AMPL_TUPLE
    ctypedef struct AMPL_TUPLE:
        pass

    void retainTuple(AMPL_TUPLE* t)

    void releaseTuple(AMPL_TUPLE* t)

    int AMPL_TupleCreate(AMPL_TUPLE** t, size_t size, AMPL_VARIANT** v)

    int AMPL_TupleCreateNumeric(AMPL_TUPLE** t, size_t size, double* v)

    int AMPL_TupleCreateString(AMPL_TUPLE** t, size_t size, const char* const* v)

    int AMPL_TupleCopy(AMPL_TUPLE** t, AMPL_TUPLE* copy)

    int AMPL_TupleFree(AMPL_TUPLE** t)

    int AMPL_TupleCompare(AMPL_TUPLE* t1, AMPL_TUPLE* t2)

    int AMPL_TupleGetSize(AMPL_TUPLE* t, size_t* size)

    int AMPL_TupleGetVariantPtr(AMPL_TUPLE* t, AMPL_VARIANT*** v)

    int AMPL_TupleGetVariant(AMPL_TUPLE* t, size_t index, AMPL_VARIANT** v)

    int AMPL_TupleToString(AMPL_TUPLE* t, char** cstr)

    #ctypedef AMPL_DataFrame AMPL_DATAFRAME
    ctypedef struct AMPL_DATAFRAME:
        pass

    AMPL_ERRORINFO* AMPL_DataFrameCreate(AMPL_DATAFRAME** dataframe, size_t numberOfIndexColumns, size_t numberOfDataColumns, const char* const* headers)

    AMPL_ERRORINFO* AMPL_DataFrameCreate2(AMPL_DATAFRAME** dataframe, size_t numberOfIndexColumns)

    AMPL_ERRORINFO* AMPL_DataFrameCopy(AMPL_DATAFRAME** dataframe, AMPL_DATAFRAME* copy)

    void AMPL_DataFrameFree(AMPL_DATAFRAME** dataframe)

    AMPL_ERRORINFO* AMPL_DataFrameGetHeaders(AMPL_DATAFRAME* dataframe, size_t* size, char*** headers)

    AMPL_ERRORINFO* AMPL_DataFrameEquals(AMPL_DATAFRAME* df1, AMPL_DATAFRAME* df2, int* equals)

    AMPL_ERRORINFO* AMPL_DataFrameToString(AMPL_DATAFRAME* dataframe, char** output)

    AMPL_ERRORINFO* AMPL_DataFrameReserve(AMPL_DATAFRAME* dataframe, size_t numRows)

    AMPL_ERRORINFO* AMPL_DataFrameAddRow(AMPL_DATAFRAME* dataframe, AMPL_TUPLE* value)

    AMPL_ERRORINFO* AMPL_DataFrameSetColumnArg(AMPL_DATAFRAME* dataframe, const char* header, AMPL_ARGS* column, size_t n)

    AMPL_ERRORINFO* AMPL_DataFrameSetColumnArgDouble(AMPL_DATAFRAME* dataframe, const char* header, const double* column, size_t n)

    AMPL_ERRORINFO* AMPL_DataFrameSetColumnArgString(AMPL_DATAFRAME* dataframe, const char* header, const char* const* column, size_t n)

    AMPL_ERRORINFO* AMPL_DataFrameSetValue(AMPL_DATAFRAME* dataframe, AMPL_TUPLE* rowIndex, const char* header, AMPL_VARIANT* value)

    AMPL_ERRORINFO* AMPL_DataFrameSetValueByIndex(AMPL_DATAFRAME* dataframe, size_t rowNumber, size_t colNumber, AMPL_VARIANT* value)

    AMPL_ERRORINFO* AMPL_DataFrameAddColumn(AMPL_DATAFRAME* dataframe, const char* header, AMPL_ARGS* values)

    AMPL_ERRORINFO* AMPL_DataFrameAddColumnDouble(AMPL_DATAFRAME* dataframe, const char* header, const double* values)

    AMPL_ERRORINFO* AMPL_DataFrameAddColumnString(AMPL_DATAFRAME* dataframe, const char* header, const char** values)

    AMPL_ERRORINFO* AMPL_DataFrameAddEmptyColumn(AMPL_DATAFRAME* dataframe, const char* header)

    AMPL_ERRORINFO* AMPL_DataFrameGetNumCols(AMPL_DATAFRAME* dataframe, size_t* num)

    AMPL_ERRORINFO* AMPL_DataFrameGetNumRows(AMPL_DATAFRAME* dataframe, size_t* num)

    AMPL_ERRORINFO* AMPL_DataFrameGetNumIndices(AMPL_DATAFRAME* dataframe, size_t* num)

    AMPL_ERRORINFO* AMPL_DataFrameSetArray(AMPL_DATAFRAME* dataframe, const double* values, size_t l0, AMPL_ARGS* indices0)

    AMPL_ERRORINFO* AMPL_DataFrameSetArrayString(AMPL_DATAFRAME* dataframe, const char* const* values, size_t l0, AMPL_ARGS* indices0)

    AMPL_ERRORINFO* AMPL_DataFrameSetMatrix(AMPL_DATAFRAME* dataframe, const double* values, size_t l0, AMPL_ARGS* indices0, size_t l1, AMPL_ARGS* indices1)

    AMPL_ERRORINFO* AMPL_DataFrameSetMatrixStringString(AMPL_DATAFRAME* dataframe, const double* values, size_t l0, const char* const* indices0, size_t l1, const char* const* indices1)

    AMPL_ERRORINFO* AMPL_DataFrameSetMatrixString(AMPL_DATAFRAME* dataframe, const char* const* values, size_t l0, AMPL_ARGS* indices0, size_t l1, AMPL_ARGS* indices1)

    AMPL_ERRORINFO* AMPL_DataFrameGetColumnIndex(AMPL_DATAFRAME* dataframe, const char* name, size_t* columnindex)

    AMPL_ERRORINFO* AMPL_DataFrameGetIndexingTuple(AMPL_DATAFRAME* dataframe, size_t rowindex, AMPL_TUPLE** index)

    AMPL_ERRORINFO* AMPL_DataFrameGetRowIndex(AMPL_DATAFRAME* dataframe, AMPL_TUPLE* index, size_t* rowindex)

    AMPL_ERRORINFO* AMPL_DataFrameElement(AMPL_DATAFRAME* dataframe, size_t rowindex, size_t colindex, AMPL_VARIANT** v)

    ctypedef struct AMPL_ENVIRONMENTVAR:
        char* name
        char* value

    int AMPL_EnvironmentVarGetName(AMPL_ENVIRONMENTVAR* envvar, char** name)

    int AMPL_EnvironmentVarGetValue(AMPL_ENVIRONMENTVAR* envvar, char** value)

    #ctypedef AMPL_Environment AMPL_ENVIRONMENT
    ctypedef struct AMPL_ENVIRONMENT:
        pass

    int AMPL_EnvironmentCreate(AMPL_ENVIRONMENT** env, const char* binaryDirectory, const char* binaryName)

    int AMPL_EnvironmentFree(AMPL_ENVIRONMENT** env)

    int AMPL_EnvironmentCopy(AMPL_ENVIRONMENT** copy, AMPL_ENVIRONMENT* src)

    int AMPL_EnvironmentAddEnvironmentVariable(AMPL_ENVIRONMENT* env, const char* name, const char* value)

    int AMPL_EnvironmentGetBinaryDirectory(AMPL_ENVIRONMENT* env, char** binaryDirectory)

    int AMPL_EnvironmentGetAMPLCommand(AMPL_ENVIRONMENT* env, char** amplCommand)

    int AMPL_EnvironmentSetBinaryDirectory(AMPL_ENVIRONMENT* env, const char* binaryDirectory)

    int AMPL_EnvironmentGetBinaryName(AMPL_ENVIRONMENT* env, char** binaryName)

    int AMPL_EnvironmentSetBinaryName(AMPL_ENVIRONMENT* env, const char* binaryName)

    int AMPL_EnvironmentToString(AMPL_ENVIRONMENT* env, char** str)

    int AMPL_EnvironmentGetSize(AMPL_ENVIRONMENT* env, size_t* size)

    int AMPL_EnvironmentGetEnvironmentVar(AMPL_ENVIRONMENT* env, AMPL_ENVIRONMENTVAR** envvar)

    int AMPL_EnvironmentFindEnvironmentVar(AMPL_ENVIRONMENT* env, const char* name, AMPL_ENVIRONMENTVAR** envvar)

    ctypedef enum AMPL_OUTPUTKIND:
        AMPL_OUTPUT_WAITING
        AMPL_OUTPUT_BREAK
        AMPL_OUTPUT_CD
        AMPL_OUTPUT_DISPLAY
        AMPL_OUTPUT_EXIT
        AMPL_OUTPUT_EXPAND
        AMPL_OUTPUT_LOAD
        AMPL_OUTPUT_OPTION
        AMPL_OUTPUT_PRINT
        AMPL_OUTPUT_PROMPT
        AMPL_OUTPUT_SOLUTION
        AMPL_OUTPUT_SOLVE
        AMPL_OUTPUT_SHOW
        AMPL_OUTPUT_XREF
        AMPL_OUTPUT_SHELL_OUTPUT
        AMPL_OUTPUT_SHELL_MESSAGE
        AMPL_OUTPUT_MISC
        AMPL_OUTPUT_WRITE_TABLE
        AMPL_OUTPUT_READ_TABLE
        AMPL_OUTPUT_READTABLE
        AMPL_OUTPUT_WRITETABLE
        AMPL_OUTPUT_BREAKPOINT
        AMPL_OUTPUT_CALL
        AMPL_OUTPUT_CHECK
        AMPL_OUTPUT_CLOSE
        AMPL_OUTPUT_COMMANDS
        AMPL_OUTPUT_CONTINUE
        AMPL_OUTPUT_DATA
        AMPL_OUTPUT_DELETECMD
        AMPL_OUTPUT_DROP
        AMPL_OUTPUT_DROP_OR_RESTORE_ALL
        AMPL_OUTPUT_ELSE
        AMPL_OUTPUT_ELSE_CHECK
        AMPL_OUTPUT_ENDIF
        AMPL_OUTPUT_ENVIRON
        AMPL_OUTPUT_FIX
        AMPL_OUTPUT_FOR
        AMPL_OUTPUT_IF
        AMPL_OUTPUT_LET
        AMPL_OUTPUT_LOOPEND
        AMPL_OUTPUT_OBJECTIVE
        AMPL_OUTPUT_OPTION_RESET
        AMPL_OUTPUT_PRINTF
        AMPL_OUTPUT_PROBLEM
        AMPL_OUTPUT_PURGE
        AMPL_OUTPUT_RBRACE
        AMPL_OUTPUT_READ
        AMPL_OUTPUT_RELOAD
        AMPL_OUTPUT_REMOVE
        AMPL_OUTPUT_REPEAT
        AMPL_OUTPUT_REPEAT_END
        AMPL_OUTPUT_RESET
        AMPL_OUTPUT_RESTORE
        AMPL_OUTPUT_RUN_ARGS
        AMPL_OUTPUT_SEMICOLON
        AMPL_OUTPUT_SSTEP
        AMPL_OUTPUT_THEN
        AMPL_OUTPUT_UNFIX
        AMPL_OUTPUT_UNLOAD
        AMPL_OUTPUT_UPDATE
        AMPL_OUTPUT_WRITE

    ctypedef void (*AMPL_OutputHandlerCb)(AMPL_OUTPUTKIND, const char*, void*) except *

    ctypedef void (*RunnablePtr)(void* runnable)

    int AMPL_StringFree(char** string)

    int AMPL_ErrorInfoFree(AMPL_ERRORINFO** error)

    void AMPL_AddToPath(const char* newPath)

    #ctypedef Ampl AMPL
    ctypedef struct AMPL:
        pass

    AMPL_ERRORINFO* AMPL_Create(AMPL** ampl)

    AMPL_ERRORINFO* AMPL_CreateWithEnv(AMPL** ampl, AMPL_ENVIRONMENT* env)

    void AMPL_Free(AMPL** ampl)

    AMPL_ERRORINFO* AMPL_Eval(AMPL* ampl, const char* statement) except *

    AMPL_ERRORINFO* AMPL_EvalAsync(AMPL* ampl, const char* statement, RunnablePtr function, void* cb)

    AMPL_ERRORINFO* AMPL_SolveAsync(AMPL* ampl, RunnablePtr function, void* cb)

    AMPL_ERRORINFO* AMPL_ReadAsync(AMPL* ampl, const char* filename, RunnablePtr function, void* cb)

    AMPL_ERRORINFO* AMPL_ReadDataAsync(AMPL* ampl, const char* filename, RunnablePtr function, void* cb)

    AMPL_ERRORINFO* AMPL_Reset(AMPL* ampl)

    AMPL_ERRORINFO* AMPL_Close(AMPL* ampl)

    AMPL_ERRORINFO* AMPL_IsRunning(AMPL* ampl, bool* running)

    AMPL_ERRORINFO* AMPL_IsBusy(AMPL* ampl, bool* busy)

    AMPL_ERRORINFO* AMPL_Solve(AMPL* ampl, const char* problem, const char* solver)

    AMPL_ERRORINFO* AMPL_Interrupt(AMPL* ampl)

    AMPL_ERRORINFO* AMPL_Snapshot(AMPL* ampl, const char* fileName, bool model, bool data, bool options, char** output)

    AMPL_ERRORINFO* AMPL_ExportModel(AMPL* ampl, const char* fileName, char** output)

    AMPL_ERRORINFO* AMPL_ExportData(AMPL* ampl, const char* fileName, char** output)

    AMPL_ERRORINFO* AMPL_Cd(AMPL* ampl, char** output)

    AMPL_ERRORINFO* AMPL_Cd2(AMPL* ampl, const char* path, char** output)

    AMPL_ERRORINFO* AMPL_GetCurrentObjective(AMPL* ampl, char** currentObjective)

    AMPL_ERRORINFO* AMPL_SetOption(AMPL* ampl, const char* name, const char* value)

    AMPL_ERRORINFO* AMPL_GetOption(AMPL* ampl, const char* name, bool* exists, char** value)

    AMPL_ERRORINFO* AMPL_GetIntOption(AMPL* ampl, const char* name, bool* exists, int* value)

    AMPL_ERRORINFO* AMPL_GetDblOption(AMPL* ampl, const char* name, bool* exists, double* value)

    AMPL_ERRORINFO* AMPL_SetDblOption(AMPL* ampl, const char* name, double value)

    AMPL_ERRORINFO* AMPL_SetIntOption(AMPL* ampl, const char* name, int value)

    AMPL_ERRORINFO* AMPL_GetBoolOption(AMPL* ampl, const char* name, bool* exists, bool* value)

    AMPL_ERRORINFO* AMPL_SetBoolOption(AMPL* ampl, const char* name, bool value)

    AMPL_ERRORINFO* AMPL_Read(AMPL* ampl, const char* fileName)

    AMPL_ERRORINFO* AMPL_ReadData(AMPL* ampl, const char* fileName)

    AMPL_ERRORINFO* AMPL_GetData(AMPL* ampl, const char* const* displayStatements, size_t n, AMPL_DATAFRAME** output)

    AMPL_ERRORINFO* AMPL_SetData(AMPL* ampl, AMPL_DATAFRAME* df, const char* setName)

    AMPL_ERRORINFO* AMPL_ToString(AMPL* ampl, char** output)

    AMPL_ERRORINFO* AMPL_ReadTable(AMPL* ampl, const char* tableName)

    AMPL_ERRORINFO* AMPL_WriteTable(AMPL* ampl, const char* tableName)

    AMPL_ERRORINFO* AMPL_Write(AMPL* ampl, const char* filename, const char* auxfiles)

    AMPL_ERRORINFO* AMPL_GetValue(AMPL* ampl, const char* scalarExpression, AMPL_VARIANT** v)

    AMPL_ERRORINFO* AMPL_GetValueString(AMPL* ampl, const char* scalarExpression, char** value)

    AMPL_ERRORINFO* AMPL_GetValueNumeric(AMPL* ampl, const char* scalarExpression, double* value)

    AMPL_ERRORINFO* AMPL_GetOutput(AMPL* ampl, const char* amplstatement, char** output)

    AMPL_ERRORINFO* AMPL_CallVisualisationCommandOnNames(AMPL* ampl, const char* command, const char* const* args, size_t nargs)

    AMPL_ERRORINFO* AMPL_SetOutputHandler(AMPL* ampl, AMPL_OutputHandlerCb callback, void* usrdata)

    AMPL_ERRORINFO* AMPL_SetErrorHandler(AMPL* ampl, ErrorHandlerCbPtr callback, void* usrdata)

    AMPL_ERRORINFO *AMPL_GetOutputHandler(AMPL *ampl, void **usrdata);

    AMPL_ERRORINFO *AMPL_GetErrorHandler(AMPL *ampl, void **usrdata);

    AMPL_ERRORINFO* AMPL_GetVariables(AMPL* ampl, size_t* size, char*** names)

    AMPL_ERRORINFO* AMPL_GetConstraints(AMPL* ampl, size_t* size, char*** names)

    AMPL_ERRORINFO* AMPL_GetParameters(AMPL* ampl, size_t* size, char*** names)

    AMPL_ERRORINFO* AMPL_GetObjectives(AMPL* ampl, size_t* size, char*** names)

    AMPL_ERRORINFO* AMPL_GetSets(AMPL* ampl, size_t* size, char*** names)

    AMPL_ERRORINFO* AMPL_GetTables(AMPL* ampl, size_t* size, char*** names)

    AMPL_ERRORINFO* AMPL_GetProblems(AMPL* ampl, size_t* size, char*** names)

    AMPL_ERRORINFO* AMPL_DataFrameCreate3(AMPL_DATAFRAME** dataframe, AMPL* ampl, const char* const* args, size_t nargs)

    ctypedef enum AMPL_ENTITYTYPE:
        AMPL_VARIABLE
        AMPL_CONSTRAINT
        AMPL_OBJECTIVE
        AMPL_PARAMETER
        AMPL_SET
        AMPL_TABLE
        AMPL_PROBLEM
        AMPL_UNDEFINED

    AMPL_ERRORINFO* AMPL_EntityGetIndexarity(AMPL* ampl, const char* name, size_t* arity)

    AMPL_ERRORINFO* AMPL_EntityGetXref(AMPL* ampl, const char* name, char*** xref, size_t* size)

    AMPL_ERRORINFO* AMPL_EntityGetNumInstances(AMPL* ampl, const char* name, size_t* size)

    AMPL_ERRORINFO* AMPL_EntityGetTuples(AMPL* ampl, const char* name, AMPL_TUPLE*** tuples, size_t* size)

    AMPL_ERRORINFO* AMPL_EntityGetIndexingSets(AMPL* ampl, const char* name, char*** indexingsets, size_t* size)

    AMPL_ERRORINFO* AMPL_EntityGetType(AMPL* ampl, const char* name, AMPL_ENTITYTYPE* type)

    AMPL_ERRORINFO* AMPL_EntityGetTypeString(AMPL* ampl, const char* name, const char** typestr)

    AMPL_ERRORINFO* AMPL_EntityGetDeclaration(AMPL* ampl, const char* name, char** declaration)

    AMPL_ERRORINFO* AMPL_EntityDrop(AMPL* ampl, const char* name)

    AMPL_ERRORINFO* AMPL_EntityRestore(AMPL* ampl, const char* name)

    AMPL_ERRORINFO* AMPL_EntityGetValues(AMPL* ampl, const char* name, const char* const* suffixes, size_t n, AMPL_DATAFRAME** output)

    AMPL_ERRORINFO* AMPL_EntitySetValues(AMPL* ampl, const char* name, AMPL_DATAFRAME* data)

    AMPL_ERRORINFO* AMPL_ParameterSetValue(AMPL* ampl, const char* scalarExpression, AMPL_VARIANT* v)

    AMPL_ERRORINFO* AMPL_ParameterSetNumeric(AMPL* ampl, const char* scalarExpression, double value)

    AMPL_ERRORINFO* AMPL_ParameterSetString(AMPL* ampl, const char* scalarExpression, const char* value)

    AMPL_ERRORINFO* AMPL_ParameterIsSymbolic(AMPL* ampl, const char* name, bool* isSymbolic)

    AMPL_ERRORINFO* AMPL_ParameterHasDefault(AMPL* ampl, const char* name, bool* hasDefault)

    AMPL_ERRORINFO* AMPL_ParameterSetArgsDoubleValues(AMPL* ampl, const char* name, size_t size, const double* args)

    AMPL_ERRORINFO* AMPL_ParameterSetArgsStringValues(AMPL* ampl, const char* name, size_t size, const char* const* args)

    AMPL_ERRORINFO* AMPL_ParameterSetArgsValues(AMPL* ampl, const char* name, size_t size, AMPL_ARGS* args)

    AMPL_ERRORINFO* AMPL_ParameterSetValuesMatrix(AMPL* ampl, const char* name, size_t nrows, AMPL_ARGS* row_indices, size_t ncols, AMPL_ARGS* col_indices, const double* data, bool transpose)

    AMPL_ERRORINFO* AMPL_ParameterSetSomeValues(AMPL* ampl, const char* name, size_t size, AMPL_TUPLE** index, AMPL_VARIANT** v)

    AMPL_ERRORINFO* AMPL_ParameterSetSomeArgsValues(AMPL* ampl, const char* name, size_t size, AMPL_TUPLE** index, AMPL_ARGS* args)

    AMPL_ERRORINFO *AMPL_ParameterSetSomeStringValues(AMPL *ampl, const char *name, size_t size, AMPL_TUPLE **index, char **str_values)

    AMPL_ERRORINFO *AMPL_ParameterSetSomeDoubleValues(AMPL *ampl, const char *name, size_t size, AMPL_TUPLE **index, double *dbl_values)

    AMPL_ERRORINFO* AMPL_VariableGetValue(AMPL* ampl, const char* name, double* value)

    AMPL_ERRORINFO* AMPL_VariableFix(AMPL* ampl, const char* name)

    AMPL_ERRORINFO* AMPL_VariableFixWithValue(AMPL* ampl, const char* name, double value)

    AMPL_ERRORINFO* AMPL_VariableUnfix(AMPL* ampl, const char* name)

    AMPL_ERRORINFO* AMPL_VariableSetValue(AMPL* ampl, const char* name, double value)

    AMPL_ERRORINFO* AMPL_VariableGetIntegrality(AMPL* ampl, const char* name, int* integrality)

    AMPL_ERRORINFO* AMPL_ConstraintIsLogical(AMPL* ampl, const char* name, bool* isLogical)

    AMPL_ERRORINFO* AMPL_ConstraintSetDual(AMPL* ampl, const char* name, double dual)

    AMPL_ERRORINFO* AMPL_ObjectiveSense(AMPL* ampl, const char* name, int* sense)

    AMPL_ERRORINFO* AMPL_SetGetArity(AMPL* ampl, const char* name, size_t* arity)

    AMPL_ERRORINFO* AMPL_TableRead(AMPL* ampl, const char* name)

    AMPL_ERRORINFO* AMPL_TableWrite(AMPL* ampl, const char* name)

    AMPL_ERRORINFO* AMPL_InstanceGetDoubleSuffix(AMPL* ampl, const char* entityname, AMPL_TUPLE* tuple, AMPL_NUMERICSUFFIX suffix, double* value)

    AMPL_ERRORINFO* AMPL_InstanceGetIntSuffix(AMPL* ampl, const char* entityname, AMPL_TUPLE* tuple, AMPL_NUMERICSUFFIX suffix, int* value)

    AMPL_ERRORINFO* AMPL_InstanceGetStringSuffix(AMPL* ampl, const char* entityname, AMPL_TUPLE* tuple, AMPL_STRINGSUFFIX suffix, char** value)

    AMPL_ERRORINFO* AMPL_InstanceGetName(AMPL* ampl, const char* entityname, AMPL_TUPLE* tuple, char** name)

    AMPL_ERRORINFO* AMPL_InstanceToString(AMPL* ampl, const char* entityname, AMPL_TUPLE* tuple, char** str)

    AMPL_ERRORINFO* AMPL_InstanceDrop(AMPL* ampl, const char* entityname, AMPL_TUPLE* tuple)

    AMPL_ERRORINFO* AMPL_InstanceRestore(AMPL* ampl, const char* entityname, AMPL_TUPLE* tuple)

    AMPL_ERRORINFO* AMPL_VariableInstanceFix(AMPL* ampl, const char* entityname, AMPL_TUPLE* tuple)

    AMPL_ERRORINFO* AMPL_VariableInstanceFixToValue(AMPL* ampl, const char* entityname, AMPL_TUPLE* tuple, double value)

    AMPL_ERRORINFO* AMPL_VariableInstanceUnfix(AMPL* ampl, const char* entityname, AMPL_TUPLE* tuple)

    AMPL_ERRORINFO* AMPL_VariableInstanceSetValue(AMPL* ampl, const char* entityname, AMPL_TUPLE* tuple, double value)

    AMPL_ERRORINFO* AMPL_VariableInstanceToString(AMPL* ampl, const char* entityname, AMPL_TUPLE* tuple, char** str)

    AMPL_ERRORINFO* AMPL_ConstraintInstanceSetDual(AMPL* ampl, const char* entityname, AMPL_TUPLE* tuple, double dual)

    AMPL_ERRORINFO* AMPL_SetInstanceGetSize(AMPL* ampl, const char* entityname, AMPL_TUPLE* tuple, size_t* size)

    AMPL_ERRORINFO* AMPL_SetInstanceContains(AMPL* ampl, const char* entityname, AMPL_TUPLE* index, AMPL_TUPLE* tuple, bool* contains)

    AMPL_ERRORINFO* AMPL_SetInstanceGetValues(AMPL* ampl, const char* entityname, AMPL_TUPLE* tuple, AMPL_TUPLE*** tuples, size_t* size)

    AMPL_ERRORINFO* AMPL_SetInstanceGetValuesDataframe(AMPL* ampl, const char* entityname, AMPL_TUPLE* tuple, AMPL_DATAFRAME** dataframe)

    AMPL_ERRORINFO* AMPL_SetInstanceSetValues(AMPL* ampl, const char* entityname, AMPL_TUPLE* tuple, AMPL_ARGS* args, size_t size)

    AMPL_ERRORINFO* AMPL_SetInstanceSetValuesTuples(AMPL* ampl, const char* entityname, AMPL_TUPLE* tuple, AMPL_TUPLE** tuples, size_t size)

    AMPL_ERRORINFO* AMPL_SetInstanceSetValuesDataframe(AMPL* ampl, const char* entityname, AMPL_TUPLE* tuple, AMPL_DATAFRAME* data)

    AMPL_ERRORINFO* AMPL_SetInstanceToString(AMPL* ampl, const char* entityname, AMPL_TUPLE* tuple, char** str)

    AMPL_ERRORINFO* AMPL_ParameterInstanceSetValue(AMPL* ampl, const char* name, AMPL_TUPLE* index, AMPL_VARIANT* v)

    AMPL_ERRORINFO* AMPL_ParameterInstanceSetNumericValue(AMPL* ampl, const char* name, AMPL_TUPLE* index, double value)

    AMPL_ERRORINFO* AMPL_ParameterInstanceSetStringValue(AMPL* ampl, const char* name, AMPL_TUPLE* index, const char* value)

    AMPL_ERRORINFO* AMPL_TableInstanceRead(AMPL* ampl, const char* entityname, AMPL_TUPLE* tuple)

    AMPL_ERRORINFO* AMPL_TableInstanceWrite(AMPL* ampl, const char* entityname, AMPL_TUPLE* tuple)
