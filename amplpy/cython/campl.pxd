# pip install autopxd2
# autopxd -I amplpy/amplpython/cppinterface/include/ amplpy/amplpython/cppinterface/include/ampl/ampl_c.h
from libcpp cimport bool
cdef extern from "ampl/ampl_c.h":

    ctypedef enum AMPL_ENTITYTYPE:
        AMPL_VARIABLE
        AMPL_CONSTRAINT
        AMPL_OBJECTIVE
        AMPL_PARAMETER
        AMPL_SET
        AMPL_TABLE
        AMPL_PROBLEM
        AMPL_UNDEFINED

    ctypedef enum AMPL_STRINGSUFFIX:
        astatus
        sstatus
        status
        message
        result
        sense

    ctypedef enum AMPL_NUMERICSUFFIX:
        VALUE
        DEFEQN
        DUAL
        INIT
        INIT0
        LB
        UB
        LB0
        UB0
        LB1
        UB1
        LB2
        UB2
        LRC
        URC
        LSLACK
        USLACK
        RC
        SLACK
        BODY
        DEFVAR
        DINIT
        DINIT0
        LBS
        UBS
        LDUAL
        UDUAL
        VAL
        EXITCODE

    const char* NUMERICSUFFIXES[29]

    const char* STRINGSUFFIXES[6]

#    ctypedef AMPL_Environment AMPL_ENVIRONMENT

#    ctypedef AMPL_EnvironmentRefPointer AMPL_ENVIRONMENTREFPOINTER

    ctypedef struct AMPL_ENVIRONMENT:
        pass 

    ctypedef struct AMPL_ENVIRONMENTREFPOINTER:
        pass 

    int AMPL_EnvironmentCreate(AMPL_ENVIRONMENT** env)

    int AMPL_EnvironmentCreateWithBin(AMPL_ENVIRONMENT** env, const char* binaryDirectory, const char* binaryName)

    int AMPL_EnvironmentDestroy(AMPL_ENVIRONMENT** env)

    int AMPL_EnvironmentCopy(AMPL_ENVIRONMENT** env, AMPL_ENVIRONMENT* copy)

    int AMPL_EnvironmentAddEnvironmentVariable(AMPL_ENVIRONMENT* env, const char* name, const char* value)

    int AMPL_EnvironmentGetBinaryDirectory(AMPL_ENVIRONMENT* env, const char** binaryDirectory)

    int AMPL_EnvironmentSetBinaryDirectory(AMPL_ENVIRONMENT* env, const char* binaryDirectory)

    int AMPL_EnvironmentGetBinaryName(AMPL_ENVIRONMENT* env, const char** binaryName)

    int AMPL_EnvironmentSetBinaryName(AMPL_ENVIRONMENT* env, const char* binaryName)

    int AMPL_EnvironmentGetAMPLCommand(AMPL_ENVIRONMENT* env, const char** command)

    int AMPL_EnvironmentToString(AMPL_ENVIRONMENT* env, const char** str)

    int AMPL_EnvironmentGetSize(AMPL_ENVIRONMENT* env, size_t* size)

    int AMPL_Environment_begin(AMPL_ENVIRONMENT* env, AMPL_ENVIRONMENTREFPOINTER** refpointer)

    int AMPL_Environment_end(AMPL_ENVIRONMENT* env, AMPL_ENVIRONMENTREFPOINTER** refpointer)

    int AMPL_Environment_find(AMPL_ENVIRONMENT* env, const char* name, AMPL_ENVIRONMENTREFPOINTER** refpointer)

    void AMPL_Environment_iterator_increment(AMPL_ENVIRONMENTREFPOINTER* refpointer)

    size_t AMPL_Environment_iterator_get_count(AMPL_ENVIRONMENTREFPOINTER* refpointer)

    void AMPL_Environment_iterator_increment_count(AMPL_ENVIRONMENTREFPOINTER* refpointer)

    void AMPL_Environment_iterator_decrement_count(AMPL_ENVIRONMENTREFPOINTER* refpointer)

    void AMPL_Environment_iterator_delete(AMPL_ENVIRONMENTREFPOINTER* refpointer)

    bool AMPL_Environment_iterator_equal(AMPL_ENVIRONMENTREFPOINTER* refpointer1, AMPL_ENVIRONMENTREFPOINTER* refpointer2)

    void AMPL_Environment_iterator_getPointer(AMPL_ENVIRONMENTREFPOINTER* refpointer, const char** first, const char** second)

    ctypedef void (*ErrorHandlerCbPtr)(bool isWarning, const char* filename, int row, int offset, const char* message, void* errorHandler)

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
        AMPL_OUTPUT__WRITETABLE
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

    ctypedef void (*OutputHandlerCbPtr)(AMPL_OUTPUTKIND, const char*, void*)

    ctypedef enum AMPL_TYPE:
        AMPL_EMPTY
        AMPL_NUMERIC
        AMPL_STRING

    cdef struct AMPL_Args:
        size_t count
        AMPL_TYPE type
        const double* dbl_values
        const char* const* str_values

    ctypedef AMPL_Args AMPL_ARGS

    cdef struct AMPL_Str:
        size_t count
        char data[]

    ctypedef AMPL_Str AMPL_STR

    cdef struct AMPL_Variant:
        size_t count
        AMPL_TYPE type
        double nvalue
        AMPL_STR* str

    ctypedef AMPL_Variant AMPL_VARIANT

    cdef struct AMPL_Tuple:
        size_t count
        AMPL_VARIANT** data
        size_t size

    ctypedef AMPL_Tuple AMPL_TUPLE

    cdef struct AMPL_TupleArray:
        AMPL_TUPLE** data
        size_t size

    ctypedef AMPL_TupleArray AMPL_TUPLEARRAY

#    ctypedef AMPL_DataFrame AMPL_DATAFRAME
    ctypedef struct AMPL_DATAFRAME:
        pass 

#    ctypedef Amplptr AMPLPtr
    ctypedef struct AMPLPtr:
        pass 

    void retainVariant(AMPL_VARIANT* v)

    void retainTuple(AMPL_TUPLE* t)

    void releaseVariant(AMPL_VARIANT* v)

    void releaseTuple(AMPL_TUPLE* t)

    int AMPL_VariantCreateEmpty(AMPL_VARIANT** v)

    int AMPL_VariantCreateNumeric(AMPL_VARIANT** v, double value)

    int AMPL_VariantCreateString(AMPL_VARIANT** v, const char* cstr)

    int AMPL_VariantCopy(AMPL_VARIANT** v, AMPL_VARIANT* copy)

    int AMPL_VariantDestroy(AMPL_VARIANT** v)

    int AMPL_VariantCompare(AMPL_VARIANT* v1, AMPL_VARIANT* v2)

    int AMPL_VariantGetNumericValue(AMPL_VARIANT* v, double* value)

    int AMPL_VariantGetStringValue(AMPL_VARIANT* v, char** value)

    int AMPL_VariantGetType(AMPL_VARIANT* v, AMPL_TYPE* type)

    int AMPL_VariantFormat(AMPL_VARIANT* v, char** cstr)

    int AMPL_VariantDeleteArray(size_t size, AMPL_VARIANT** variant)

    int AMPL_VariantCreateArray(size_t size, AMPL_VARIANT** variant)

    void retainArgs(AMPL_ARGS* args)

    void releaseArgs(AMPL_ARGS* args)

    int AMPL_ArgsCreateNumeric(AMPL_ARGS** args, const double* values)

    int AMPL_ArgsCreateString(AMPL_ARGS** args, const char* const* values)

    int AMPL_ArgsDestroy(AMPL_ARGS** args)

    int AMPL_TupleCreate(AMPL_TUPLE** t, size_t size, AMPL_VARIANT** v)

    int AMPL_TupleCopy(AMPL_TUPLE** t, AMPL_TUPLE* copy)

    int AMPL_TupleDestroy(AMPL_TUPLE** t)

    int AMPL_TupleCompare(AMPL_TUPLE* t1, AMPL_TUPLE* t2)

    int AMPL_TupleGetSize(AMPL_TUPLE* t, size_t* size)

    int AMPL_TupleGetVariantPtr(AMPL_TUPLE* t, AMPL_VARIANT*** v)

    int AMPL_TupleGetVariant(AMPL_TUPLE* t, size_t index, AMPL_VARIANT** v)

    int AMPL_TupleToString(AMPL_TUPLE* t, char** cstr)

    int AMPL_TupleArrayCreate(AMPL_TUPLEARRAY** t, size_t size, AMPL_TUPLE** tuples)

    int AMPL_TupleArrayDestroy(AMPL_TUPLEARRAY** t)

    int AMPL_StringFree(char* string)

    int AMPL_ManyStringsFree(char** strings, size_t size)

    int AMPL_DataFrameCreate(AMPL_DATAFRAME** dataframe, size_t numberOfIndexColumns, size_t numberOfDataColumns, const char* const* headers)

    int AMPL_DataFrameCreate2(AMPL_DATAFRAME** dataframe, size_t numberOfIndexColumns)

    int AMPL_DataFrameCreate3(AMPL_DATAFRAME** dataframe, AMPLPtr* ampl, const char* const* args, size_t nargs)

    int AMPL_DataFrameCopy(AMPL_DATAFRAME** dataframe, AMPL_DATAFRAME* copy)

    int AMPL_DataFrameDestroy(AMPL_DATAFRAME** dataframe)

    int AMPL_DataFrameGetHeaders(AMPL_DATAFRAME* dataframe, char*** headers, size_t* size)

    int AMPL_DataFrameEquals(AMPL_DATAFRAME* df1, AMPL_DATAFRAME* df2, int* equals)

    int AMPL_DataFrameToString(AMPL_DATAFRAME* dataframe, char** output)

    int AMPL_DataFrameReserve(AMPL_DATAFRAME* dataframe, size_t numRows)

    int AMPL_DataFrameAddRow(AMPL_DATAFRAME* dataframe, AMPL_TUPLE* value)

    int AMPL_DataFrameSetColumnArg(AMPL_DATAFRAME* dataframe, const char* header, AMPL_ARGS* column, size_t n)

    int AMPL_DataFrameSetColumnArgDouble(AMPL_DATAFRAME* dataframe, const char* header, const double* column, size_t n)

    int AMPL_DataFrameSetColumnArgString(AMPL_DATAFRAME* dataframe, const char* header, const char* const* column, size_t n)

    int AMPL_DataFrameSetValue(AMPL_DATAFRAME* dataframe, AMPL_TUPLE* rowIndex, const char* header, AMPL_VARIANT* value)

    int AMPL_DataFrameSetValueByIndex(AMPL_DATAFRAME* dataframe, size_t rowNumber, size_t colNumber, AMPL_VARIANT* value)

    int AMPL_DataFrameAddColumn(AMPL_DATAFRAME* dataframe, const char* header, AMPL_ARGS* values)

    int AMPL_DataFrameAddColumnDouble(AMPL_DATAFRAME* dataframe, const char* header, const double* values)

    int AMPL_DataFrameAddEmptyColumn(AMPL_DATAFRAME* dataframe, const char* header)

    int AMPL_DataFrameGetNumCols(AMPL_DATAFRAME* dataframe, size_t* num)

    int AMPL_DataFrameGetNumRows(AMPL_DATAFRAME* dataframe, size_t* num)

    int AMPL_DataFrameGetNumIndices(AMPL_DATAFRAME* dataframe, size_t* num)

    int AMPL_DataFrameSetArray(AMPL_DATAFRAME* dataframe, const double* values, size_t l0, AMPL_ARGS* indices0)

    int AMPL_DataFrameSetArrayString(AMPL_DATAFRAME* dataframe, const char* const* values, size_t l0, AMPL_ARGS* indices0)

    int AMPL_DataFrameSetMatrix(AMPL_DATAFRAME* dataframe, const double* values, size_t l0, AMPL_ARGS* indices0, size_t l1, AMPL_ARGS* indices1)

    int AMPL_DataFrameSetMatrixStringString(AMPL_DATAFRAME* dataframe, const double* values, size_t l0, const char* const* indices0, size_t l1, const char* const* indices1)

    int AMPL_DataFrameSetMatrixString(AMPL_DATAFRAME* dataframe, const char* const* values, size_t l0, AMPL_ARGS* indices0, size_t l1, AMPL_ARGS* indices1)

    int AMPL_DataFrameGetColumnIndex(AMPL_DATAFRAME* dataframe, const char* name, size_t* columnindex)

    int AMPL_DataFrameGetIndexingTuple(AMPL_DATAFRAME* dataframe, size_t rowindex, AMPL_TUPLE** index)

    int AMPL_DataFrameGetRowIndex(AMPL_DATAFRAME* dataframe, AMPL_TUPLE* index, size_t* rowindex)

    int AMPL_DataFrameElement(AMPL_DATAFRAME* dataframe, size_t rowindex, size_t colindex, AMPL_VARIANT** v)

    int AMPL_Create(AMPLPtr** ampl)

    int AMPL_CreateWithEnv(AMPLPtr** ampl, AMPL_ENVIRONMENT* env)

    int AMPL_Destroy(AMPLPtr** ampl)

    int AMPL_Eval(AMPLPtr* ampl, const char* statement)

    int AMPL_Reset(AMPLPtr* ampl)

    int AMPL_Close(AMPLPtr* ampl)

    int AMPL_IsRunning(AMPLPtr* ampl, bool* running)

    int AMPL_IsBusy(AMPLPtr* ampl, bool* busy)

    int AMPL_Solve(AMPLPtr* ampl, const char* problem, const char* solver)

    int AMPL_Interrupt(AMPLPtr* ampl)

    int AMPL_Snapshot(AMPLPtr* ampl, const char* fileName, int model, int data, int options, char** output)

    int AMPL_ExportModel(AMPLPtr* ampl, const char* fileName, char** output)

    int AMPL_ExportData(AMPLPtr* ampl, const char* fileName, char** output)

    int AMPL_Cd(AMPLPtr* ampl, char** output)

    int AMPL_Cd2(AMPLPtr* ampl, const char* path, char** output)

    int AMPL_GetCurrentObjective(AMPLPtr* ampl, char** currentObjective)

    int AMPL_SetOption(AMPLPtr* ampl, const char* name, const char* value)

    int AMPL_GetOption(AMPLPtr* ampl, const char* name, bool* exists, char** value)

    int AMPL_GetIntOption(AMPLPtr* ampl, const char* name, bool* exists, int* value)

    int AMPL_GetDblOption(AMPLPtr* ampl, const char* name, bool* exists, double* value)

    int AMPL_SetDblOption(AMPLPtr* ampl, const char* name, double value)

    int AMPL_Read(AMPLPtr* ampl, const char* fileName)

    int AMPL_ReadData(AMPLPtr* ampl, const char* fileName)

    int AMPL_GetData(AMPLPtr* ampl, const char* const* displayStatements, size_t n, AMPL_DATAFRAME** output)

    int AMPL_SetDataAndSet(AMPLPtr* ampl, AMPL_DATAFRAME* df, const char* setName)

    int AMPL_ToString(AMPLPtr* ampl, char** output)

    int AMPL_ReadTable(AMPLPtr* ampl, const char* tableName)

    int AMPL_WriteTable(AMPLPtr* ampl, const char* tableName)

    int AMPL_Write(AMPLPtr* ampl, const char* filename, const char* auxfiles)

    int AMPL_GetValue(AMPLPtr* ampl, const char* scalarExpression, AMPL_VARIANT** v)

    int AMPL_GetOutput(AMPLPtr* ampl, const char* amplstatement, char** output)

    int AMPL_CallVisualisationCommandOnNames(AMPLPtr* ampl, const char* command, const char* const* args, size_t nargs)

    int AMPL_SetOutputHandler(AMPLPtr* ampl, void* outputhandler, OutputHandlerCbPtr callback)

    int AMPL_SetErrorHandler(AMPLPtr* ampl, void* errorhandler, ErrorHandlerCbPtr callback)

    void* AMPL_GetOutputHandler(AMPLPtr* ampl)

    void* AMPL_GetErrorHandler(AMPLPtr* ampl)

    int AMPL_GetVariables(AMPLPtr* ampl, size_t* size, char*** names)

    int AMPL_GetConstraints(AMPLPtr* ampl, size_t* size, char*** names)

    int AMPL_GetParameters(AMPLPtr* ampl, size_t* size, char*** names)

    int AMPL_GetObjectives(AMPLPtr* ampl, size_t* size, char*** names)

    int AMPL_GetSets(AMPLPtr* ampl, size_t* size, char*** names)

    int AMPL_GetTables(AMPLPtr* ampl, size_t* size, char*** names)

    int AMPL_GetProblems(AMPLPtr* ampl, size_t* size, char*** names)

    int AMPL_ParameterSetValue(AMPLPtr* ampl, const char* scalarExpression, AMPL_VARIANT* v)

    int AMPL_ParameterIsSymbolic(AMPLPtr* ampl, const char* name, bool* isSymbolic)

    int AMPL_ParameterHasDefault(AMPLPtr* ampl, const char* name, bool* hasDefault)

    int AMPL_ParameterIdxSetValue(AMPLPtr* ampl, const char* name, AMPL_TUPLE* index, AMPL_VARIANT* v)

    int AMPL_ParameterIdxSetNumericValue(AMPLPtr* ampl, const char* name, AMPL_TUPLE* index, double value)

    int AMPL_ParameterIdxSetStringValue(AMPLPtr* ampl, const char* name, AMPL_TUPLE* index, const char* value)

    int AMPL_ParameterIdxSetValues(AMPLPtr* ampl, const char* name, size_t indexarity, AMPL_TUPLE** index, AMPL_VARIANT** v)

    int AMPL_ParameterIdxSetArgsValues(AMPLPtr* ampl, const char* name, size_t size, AMPL_TUPLE** index, AMPL_ARGS* args)

    int AMPL_ParameterSetArgsDoubleValues(AMPLPtr* ampl, const char* name, size_t size, const double* args)

    int AMPL_ParameterSetArgsValues(AMPLPtr* ampl, const char* name, size_t size, AMPL_ARGS* args)

    int AMPL_ParameterSetValuesMatrix(AMPLPtr* ampl, const char* name, size_t nrows, AMPL_ARGS* row_indices, size_t ncols, AMPL_ARGS* col_indices, const double* data, bool transpose)

    int AMPL_EntityGetIndexarity(AMPLPtr* ampl, const char* name, size_t* arity)

    int AMPL_EntityGetXref(AMPLPtr* ampl, const char* name, const char*** xref, size_t* size)

    int AMPL_EntityGetNumInstances(AMPLPtr* ampl, const char* name, AMPL_ENTITYTYPE type, size_t* size)

    int AMPL_EntityGetTuples(AMPLPtr* ampl, const char* name, AMPL_ENTITYTYPE type, AMPL_TUPLE*** tuples, size_t* size)

    int AMPL_EntityGetIndexingSets(AMPLPtr* ampl, const char* name, const char* declaration, const char*** indexingsets, size_t* size)

    int AMPL_EntityGetType(AMPLPtr* ampl, const char* name, AMPL_ENTITYTYPE* type)

    int AMPL_EntityGetTypeString(AMPLPtr* ampl, const char* name, AMPL_ENTITYTYPE type, const char** typestr)

    int AMPL_EntityGetDeclaration(AMPLPtr* ampl, const char* name, char** declaration)

    int AMPL_EntityDrop(AMPLPtr* ampl, const char* name)

    int AMPL_EntityRestore(AMPLPtr* ampl, const char* name)

    int AMPL_EntityGetValues(AMPLPtr* ampl, const char* name, const char* const* suffixes, size_t n, AMPL_DATAFRAME** output)

    int AMPL_EntitySetValues(AMPLPtr* ampl, const char* name, AMPL_DATAFRAME* data)

    int AMPL_VariableFix(AMPLPtr* ampl, const char* name)

    int AMPL_VariableFixWithValue(AMPLPtr* ampl, const char* name, double value)

    int AMPL_VariableUnfix(AMPLPtr* ampl, const char* name)

    int AMPL_VariableSetValue(AMPLPtr* ampl, const char* name, double value)

    int AMPL_VariableGetIntegrality(AMPLPtr* ampl, const char* name, int* integrality)

    int AMPL_ConstraintIsLogical(AMPLPtr* ampl, const char* name, bool* isLogical)

    int AMPL_ConstraintSetDual(AMPLPtr* ampl, const char* name, double dual)

    int AMPL_ObjectiveSense(AMPLPtr* ampl, const char* name, int* sense)

    int AMPL_SetGetArity(AMPLPtr* ampl, const char* name, size_t* arity)

    int AMPL_TableRead(AMPLPtr* ampl, const char* name)

    int AMPL_TableWrite(AMPLPtr* ampl, const char* name)

    int AMPL_InstanceGetDoubleSuffix(AMPLPtr* ampl, const char* name, AMPL_NUMERICSUFFIX suffix, double* value)

    int AMPL_InstanceGetIntSuffix(AMPLPtr* ampl, const char* name, AMPL_NUMERICSUFFIX suffix, int* value)

    int AMPL_InstanceGetStringSuffix(AMPLPtr* ampl, const char* name, AMPL_STRINGSUFFIX suffix, char** value)

    int AMPL_InstanceGetName(AMPLPtr* ampl, const char* entityname, AMPL_TUPLE* tuple, char** name)

    int AMPL_InstanceToString(AMPLPtr* ampl, const char* name, char** str)

    int AMPL_InstanceDrop(AMPLPtr* ampl, const char* name)

    int AMPL_InstanceRestore(AMPLPtr* ampl, const char* name)

    int AMPL_VariableInstanceFix(AMPLPtr* ampl, const char* name)

    int AMPL_VariableInstanceFixToValue(AMPLPtr* ampl, const char* name, double value)

    int AMPL_VariableInstanceUnfix(AMPLPtr* ampl, const char* name)

    int AMPL_VariableInstanceSetValue(AMPLPtr* ampl, const char* name, double value)

    int AMPL_VariableInstanceToString(AMPLPtr* ampl, const char* name, const char* entityname, char** str)

    int AMPL_ConstraintInstanceSetDual(AMPLPtr* ampl, const char* name, double dual)

    int AMPL_SetInstanceGetSize(AMPLPtr* ampl, const char* name, size_t* size)

    int AMPL_SetInstanceContains(AMPLPtr* ampl, const char* name, AMPL_TUPLE* tuple, bool* contains)

    int AMPL_SetInstanceGetValues(AMPLPtr* ampl, const char* name, AMPL_TUPLE*** tuples, size_t* size)

    int AMPL_SetInstanceGetValuesDataframe(AMPLPtr* ampl, const char* name, AMPL_DATAFRAME** dataframe)

    int AMPL_SetInstanceSetValues(AMPLPtr* ampl, const char* name, const char* entityname, AMPL_ARGS* args, size_t size)

    int AMPL_SetInstanceSetValuesTuples(AMPLPtr* ampl, const char* name, const char* entityname, AMPL_TUPLE** tuples, size_t size)

    int AMPL_SetInstanceSetValuesDataframe(AMPLPtr* ampl, const char* name, const char* entityname, AMPL_DATAFRAME* data)

    int AMPL_SetInstanceToString(AMPLPtr* ampl, const char* name, char** str)

    int AMPL_TableInstanceRead(AMPLPtr* ampl, const char* name)

    int AMPL_TableInstanceWrite(AMPLPtr* ampl, const char* name)