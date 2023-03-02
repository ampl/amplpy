# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## 0.5.0 - 2023-03-02
- Add modules.activate and activate command.
- Add modules.preload to load modules silently.
- Add modules.unload to unload modules.
- Add modules.run.

## 0.4.6 - 2023-01-24
- Ignore ampl module since it is installed by default.
- Drop tools.load_modules.

## 0.4.5 - 2023-01-23
- Show usage message with any errors in main.

## 0.4.4 - 2023-01-20
- Remove install_modules from ampltools.
- Move add_to_path to ampltools.
- Add PATH and run commands for modules.

## 0.4.3 - 2023-01-19
- Fix bug in tools.modules.uninstall.

## 0.4.2 - 2023-01-19
- Do not specify the version of the dependency 'requests'.
- Reduce number of symbols exported.

## 0.4.1 - 2023-01-19
- Move modules code to its own submodule.

## 0.4.0 - 2023-01-18
- Add command line actions to manage modules.

## 0.3.10 - 2023-01-13
- Only show UUID prompt on Colab if any module is not open-source.

## 0.3.9 - 2022-12-29
- Allow simplified ampl_notebook invocation with modules and license_uuid only.

## 0.3.8 - 2022-12-28
- Handle license_uuid="default".

## 0.3.7 - 2022-12-28
- Fix license activation in ampl_notebook when using license_uuid.

## 0.3.6 - 2022-12-26
- Use x-ampl by default on Google Colab.

## 0.3.5 - 2022-12-23
- Fix line number offset in ampl_eval cells.

## 0.3.4 - 2022-12-22
- Make ampl_notebook output even more compact.

## 0.3.3 - 2022-12-21
- Make ampl_notebook output more compact.

## 0.3.2 - 2022-12-21
- Fixed typo.

## 0.3.1 - 2022-12-21
- Simplify output of ampl_notebook.

## 0.3.0 - 2022-12-20
- Add support for AMPL modules as python packages.

## 0.2.8 - 2022-11-14
- Add default license.

## 0.2.7 - 2022-10-24
- Fix Google Colab detection.

## 0.2.6 - 2022-10-14
- Add simplified option for ampl_notebook cell.

## 0.2.5 - 2022-04-07
- Remove one last f-string present in the code.

## 0.2.4 - 2022-04-07
- Avoid the use of f-strings to increase portability.

## 0.2.3 - 2022-02-28
- Add ampl_notebook to simplify jupyter notebooks.

## 0.2.2 - 2022-02-25
- Add ampl_license_cell and ampl_installer_cell for jupyter notebooks.

## 0.2.1 - 2022-02-21
- Fix SageMaker Studio Lab detection in cloud_platform_name().

## 0.2.0 - 2022-02-10
- Add cloud_platform_name to guess the name of the cloud platform currently running on.

## 0.1.0 - 2022-02-08
- Initial release with module_installer and ampl_installer.
