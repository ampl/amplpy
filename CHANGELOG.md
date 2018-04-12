# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## 0.4.1 - 2018-04-12
- Fix: compatibility issues with multiple python versions.

## 0.4.0 - 2018-04-10
- Improve interaction with Pandas and Numpy.
- Add DataFrame.fromNumpy.
- Entity.setValues now accepts Pandas DataFrames.
- Parameter.setValues and Set.setValues now accept Numpy arrays and matrices.
- Breaking: DataFrame.toList and DataFrame.doDict do not wrap scalar values into lists anymore.

## 0.3.4 - 2018-02-24
- Fix: error messages not being shown in Jupyter Notebooks
- Breaking: AMPL errors no longer raise exceptions by default

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
