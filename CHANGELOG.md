# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## 20260624

### 0.17.0
- Add `AMPL.expand()` and `AMPL.show()` methods.
- Add `Entity.expand()` method (dispatches to instance-level expand when indexed).

## 20250513

### 0.16.1
- Fix get() function.

## 20251208

### 0.16.0
- Add type hints to amplpy.
- Add Python 3.14 and Python 3.14t support.

## 20250709

### 0.15.2
- Fix Environment object issue when an ampl directory exists.
- Fix AMPLException object issue when the exception is printed.

## 20250620

### 0.15.1
- [Breaking] Support options times or gentimes.
- Add option "_throw_on_warnings" to control whether warnings raise exceptions.

## 20250618

### 0.15.0
- Migrated to Cython for generating extension modules, improving performance and maintainability.
- Add __str__ for AMPL objects.
- Add ampls methods into AMPL object, i.e., AMPL.to_ampls() and AMPL.import_ampls_solution().
- Add logging to exceptions thrown by ErrorHandler.
- [Breaking] Update AMPL warnings to throw an exception.
- [Breaking] Throw if options times or gentimes are set.
- Allow setting options as dict in AMPL, e.g., AMPL.option = {"solver": "gurobi", "var_bounds": 1, "gurobi_options": {"outlev": True, "timelim": 1}}

## 20240521

### 0.14.1
- Add flat argument to AMPL.get_iis.

## 20240521

### 0.14.0
- Allow assigning values to indexed sets from a dictionary with the lists of members
  for every index.
- Add AMPL.get_iis() to return dictionaries with variables and constraints in IIS.
- Add AMPL.get_solution() to return a dictionary with the solution.

## 20240220

### 0.13.3
- Fix issues with AMPL.solve(verbose=False) when the solver argument was not set.

## 20240105

### 0.13.2
- OutputHandler: Flush standard output after every message.

## 20231229

### 0.13.1
- Upgrade libampl to 2.3.7-20231229.
- Upgrade ampltools to 0.7.3 adding amplpy.bundle command.
- Fix issue with environment variables on Windows in a generic way.
- Add return_output and solvername_options arguments to AMPL.solve
  - You can now do `ampl.solve(solver="gurobi", gurobi_options="outlev=1")`.

## 20231226

### 0.13.0
- [Breaking] amplpy.modules now have priority in the PATH.
- Fix ampl_libpath issue on Windows.

## 20231211

### 0.12.2
- Upgrade libampl to 2.3.6-20231130.
- Add solver argument to AMPL.solve.

## 20230921

### 0.12.1
- Fix Parameter.set_values with np.ndarray objects.

## 20230829

### 0.12.0
- Upgrade libampl to 2.2.0-20230825.
- Use x-ampl by default if available.
- Add properties AMPL.solve_result/AMPL.solve_result_num.
- Add arguments to AMPL.solve to specify problem name and verbosity.
- Allow passing pandas.Series to AMPL.set_data and Parameter.set_values.
- Add AMPL.snapshot, and implement AMPL.export_model/AMPL.export_data using it.
- [Breaking] Drop Python 3.5 compatibility.
- [Breaking] Deprecate direct access methods to amplpy.DataFrame. Deprecated methods are still available with _ prefix.

## 20230711

### 0.11.2
- [Breaking] Cast floats to integers whenever possible.

## 20230704

### 0.11.1
- Add aliases Entity.get_values.to_pandas/to_list/to_dict.
- Automatically stack 2D pandas.DataFrames.

## 20230621

### 0.11.0
- Upgrade libampl to 2.1.2-20230618.
- Add AMPL.write, PresolveException, and InfeasibilityException.
- Improve handling of numpy types.
- Allow assigning values to sets from iterables.
- [Breaking] Drop async functionalities.
- [Breaking] DataFrame.to_pandas: start using multi-index by default.
- [Breaking] Drop Python 2.7 compatibility.
- [Breaking] Iterating over non-indexed sets now iterates over set members.

## 20230522

### 0.10.0
- Upgrade libampl to 2.1.0-20230522.
- Breaking: Entity names do not contain spaces in the indices anymore.

## 20230421

### 0.9.3
- Removed CamelCase from docstrings.

## 20230405

### 0.9.2
- Add message to append to AMPLException messages.

## 20230322

### 0.9.1
- Simplify ampl_notebook import: "from amplpy import ampl_notebook".

## 20230314

### 0.9.0
- Preload amplpy.modules if found (reduces need for modules.load()).
- Vendor ampltools.

## 20230123

### 0.8.6
- Add amplpy.modules.

## 20220823

### 0.8.5
- Update libampl to 2.0.11-20220823.
- Ensure times and gentimes default to disabled.

## 20220802

### 0.8.4
- Update libampl to 2.0.10-20220627.
- Disable options times and gentimes during internal operations.

## 20220623

### 0.8.3
- Improved handling of numpy types.

## 20220527

### 0.8.2
- [BREAKING] Raise RuntimeError in Entity.get_values if there are any issues with the data.
- Update libampl to 2.0.9.20220527.
- Fixed hanging when license check fails on Windows.
- Allow '-' in option names.
- Drop 32-bit support.
- Add ampltools as dependency.

## 20220121

### 0.8.1
- [BREAKING] Raise KeyError exceptions instead of TypeError exceptions when accessing entities that do not exist.

## 20211224

### 0.8.0
- Update libampl to 2.0.8-2.
- Allow users to specify the name of the AMPL executable.
- Allow users to choose between using camelCase and snake_case methods.
- Drop AMPL.exportGurobi model. It is now part of amplpy_gurobi.

## 20211201

### 0.7.2
- Improve performance of many operations by moving code to the C++ layer.

## 20210726

### 0.7.1
- Update libampl to 2.0.6-0.
- Add Entity.xref.
- Include complete license error message in license error exceptions.

## 20210125

### 0.7.0
- Fix bug when assigning sets with mixed types.
- Add support for pathlib.Path paths.
- Basic support for MSYS, CYGWIN, and MINGW.
- Support for linux-ppc64le and linux-aarch64.
- Update libampl to 2.0.4-0.

## 20200228

### 0.6.11
- Add support for ppc64le.

## 20191116

### 0.6.10
- Fix "ImportError: DLL load failed" not fixed in the previous version.

## 20191116

### 0.6.9
- Fix "ImportError: No module named _amplpython" introduced in the previous version.

## 20191116

### 0.6.8
- Add Python 3.8 support.

## 20190622

### 0.6.7
- Add optional parameter index_names to DataFrame.fromPandas.
- Add DataFrame.fromDict to load data from dictionaries.
- Allow setting entity values directly from dictionaries.

## 20190511

### 0.6.6
- Update internal library.
- Add AMPL.exportModel.
- AMPL.exportData now supports indexed sets.

## 20190414

### 0.6.5
- Improve AMPL.exportGurobiModel and AMPL.importGurobiSolution.
- Add verbose option to AMPL.exportGurobiModel.
- Add register_magics to register `%%ampl` and `%%ampl_eval`.

## 20190213

### 0.6.4
- Fix dll loading issue with python versions that come with conda.

## 20181204

### 0.6.3
- Fix issue with indexed sets (by updating the internal library).

## 20181120

### 0.6.2
- Add support for Pandas Series.
- Add optional gurobiDriver parameter to AMPL.exportGurobiModel.

## 20181113

### 0.6.1
- Improve robustness of AMPL.exportGurobiModel.
- Improve error message when AMPL is not in the search path.

## 20181103

### 0.6.0
- Upgrade internal API to v2.0.
- Add experimental methods AMPL._startRecording and AMPL._stopRecording.
- Add experimental method AMPL._loadSession.
- Add method AMPL.getCurrentObjective.
- Add support to Python 3.7.
- Fix truncated values in sets (amplapi#337).
- Add method AMPL.importGurobiSolution.
- Add method AMPL.getOutput.

## 20180506

### 0.5.0
- Breaking: AMPL errors raise exceptions by default.
- Breaking: Drop support for Python 3.3 on Linux.
- Add AMPL.exportData.
- Add AMPL.exportGurobiModel.

## 20180412

### 0.4.1
- Fix: compatibility issues with multiple python versions.

## 20180410

### 0.4.0
- Improve interaction with Pandas and Numpy.
- Add DataFrame.fromNumpy.
- Entity.setValues now accepts Pandas DataFrames.
- Parameter.setValues and Set.setValues now accept Numpy arrays and matrices.
- Breaking: DataFrame.toList and DataFrame.doDict do not wrap scalar values into lists anymore.

## 20180224

### 0.3.4
- Fix: error messages not being shown in Jupyter Notebooks.
- Breaking: AMPL errors no longer raise exceptions by default.

## 20180109

### 0.3.3
- Fix issues related to the passing of infinity to AMPL.

## 20171213

### 0.3.2
- Fix issue with DataFrames created with pandas.read_table.

## 20171117

### 0.3.1
- Fix precision issue in parameters.

## 20171013

### 0.3.0
- Introduce alternative method to access entities.

## 20170805

### 0.2.0
- Add DataFrame.fromPandas and DataFrame.toPandas.

## 20170804

### 0.1.2
- Improve DataFrame initialization.
- Fix issue with stdout in jupyter notebooks.

## 20170730

### 0.1.1
- Fix issues with strings in Python 3.

## 20170722

### 0.1.0
- Initial release.