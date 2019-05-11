# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## 0.6.6 - 2019-05-11
- Update internal library.
- Add AMPL.exportModel.
- AMPL.exportData now supports indexed sets.

## 0.6.5 - 2019-04-14
- Improve AMPL.exportGurobiModel and AMPL.importGurobiSolution.
- Add verbose option to AMPL.exportGurobiModel.
- Add register_magics to register `%%ampl` and `%%ampl_eval`.

## 0.6.4 - 2019-02-13
- Fix dll loading issue with python versions that come with conda.

## 0.6.3 - 2018-12-04
- Fix issue with indexed sets (by updating the internal library).

## 0.6.2 - 2018-11-20
- Add support for Pandas Series.
- Add optional gurobiDriver parameter to AMPL.exportGurobiModel.

## 0.6.1 - 2018-11-13
- Improve robustness of AMPL.exportGurobiModel.
- Improve error message when AMPL is not in the search path.

## 0.6.0 - 2018-11-03
- Upgrade internal API to v2.0.
- Add experimental methods AMPL._startRecording and AMPL._stopRecording.
- Add experimental method AMPL._loadSession.
- Add method AMPL.getCurrentObjective.
- Add support to Python 3.7.
- Fix truncated values in sets (amplapi#337).
- Add method AMPL.importGurobiSolution.
- Add method AMPL.getOutput.

## 0.5.0 - 2018-05-06
- Breaking: AMPL errors raise exceptions by default.
- Breaking: Drop support for Python 3.3 on Linux.
- Add AMPL.exportData.
- Add AMPL.exportGurobiModel.

## 0.4.1 - 2018-04-12
- Fix: compatibility issues with multiple python versions.

## 0.4.0 - 2018-04-10
- Improve interaction with Pandas and Numpy.
- Add DataFrame.fromNumpy.
- Entity.setValues now accepts Pandas DataFrames.
- Parameter.setValues and Set.setValues now accept Numpy arrays and matrices.
- Breaking: DataFrame.toList and DataFrame.doDict do not wrap scalar values into lists anymore.

## 0.3.4 - 2018-02-24
- Fix: error messages not being shown in Jupyter Notebooks.
- Breaking: AMPL errors no longer raise exceptions by default.

## 0.3.3 - 2018-01-09
- Fix issues related to the passing of infinity to AMPL.

## 0.3.2 - 2017-12-13
- Fix issue with DataFrames created with pandas.read_table.

## 0.3.1 - 2017-11-17
- Fix precision issue in parameters.

## 0.3.0 - 2017-10-13
- Introduce alternative method to access entities.

## 0.2.0 - 2017-08-05
- Add DataFrame.fromPandas and DataFrame.toPandas.

## 0.1.2 - 2017-08-04
- Improve DataFrame initialization.
- Fix issue with stdout in jupyter notebooks.

## 0.1.1 - 2017-07-30
- Fix issues with strings in Python 3.

## 0.1.0 - 2017-07-22
- Initial release.
