# Snippet

![Package](https://img.shields.io/badge/Package-code--snippet-lightgrey)
[![Documentation](https://img.shields.io/badge/Documentation-GitHub_Pages-blue)](https://armmbed.github.io/code-snippet)
[![PyPI](https://img.shields.io/pypi/v/code-snippet)](https://pypi.org/project/code-snippet/)
[![PyPI - Status](https://img.shields.io/pypi/status/code-snippet)](https://pypi.org/project/code-snippet/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/code-snippet)](https://pypi.org/project/code-snippet/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/ARMmbed/code-snippet/blob/master/LICENSE)

[![Build Status](https://dev.azure.com/mbed-tools/code-snippet/_apis/build/status/Build%20and%20Release?branchName=master&stageName=CI%20Checkpoint)](https://dev.azure.com/mbed-tools/code-snippet/_build/latest?definitionId=TODO_AZURE&branchName=master)
[![Test Coverage](https://codecov.io/gh/ARMmbed/code-snippet/branch/master/graph/badge.svg)](https://codecov.io/gh/ARMmbed/code-snippet)
[![Maintainability](https://api.codeclimate.com/v1/badges/2050e74c1c485109d357/maintainability)](https://codeclimate.com/github/ARMmbed/snippet/maintainability)

## Overview

A tool to extract code snippets from source files

Essentially, snippet extracts marked sections of text from a given set of input files and saves them elsewhere.

Features include:
- Works on any text file, e.g.
any coding language by reading from source files
- Uses customisable markup syntax
- Writes to templated output (e.g. `.md` code blocks)
- Hides sections from output
- Performs validation to help avoid snippets breaking as code changes

## Rationale 
Code documentation usually needs a written example demonstrating use of some code. This example code can however become quite easily outdated as a project evolves or even contain its own errors. 
One solution is to write the examples as tests which can be run within the test system of choice. This ensures that the code of the examples is always valid and working. `snippet`  can then be used to extract the relevant and informative part of the test and put it in a form which can then be rendered by the documentation system, providing fully tested code examples. 
 
## Releases

For release notes and a history of changes of all **production** releases, please see the following:

- [Changelog](https://github.com/ARMmbed/snippet/blob/master/CHANGELOG.md)

For a the list of all available versions please, please see the:

- [PyPI Release History](https://pypi.org/project/code-snippet/#history)

## Versioning

The version scheme used follows [PEP440](https://www.python.org/dev/peps/pep-0440/) and 
[Semantic Versioning](https://semver.org/). For production quality releases the version will look as follows:

- `<major>.<minor>.<patch>`

Beta releases are used to give early access to new functionality, for testing and to get feedback on experimental 
features. As such these releases may not be stable and should not be used for production. Additionally any interfaces
introduced in a beta release may be removed or changed without notice. For **beta** releases the version will look as
follows:

- `<major>.<minor>.<patch>-beta.<pre-release-number>`

## Installation

It is recommended that a virtual environment such as [Pipenv](https://github.com/pypa/pipenv/blob/master/README.md) is
used for all installations to avoid Python dependency conflicts.

To install the most recent production quality release use:

```
pip install code-snippet
```

To install a specific release:

```
pip install code-snippet==<version>
```

## Usage
### Configuration 
Place a config file in the [toml format](https://github.com/toml-lang/toml) 
in your project directory (e.g. `snippet.toml`). Any value defined in [the config object](https://github.com/ARMmbed/snippet/blob/master/src/snippet/config.py#L8) 
can be overridden. 
 
As an example, basic configuration typically includes input and output directories: 
 
``` 
[snippet] 
input_glob = 'tests/unit/*.py' 
output_dir = 'docs/examples' 
``` 
### Run 
Run the following command in your project: 
 
``` 
snippet 
``` 
 
Alternatively, run snippet from anywhere and specify a working directory and config file: 
``` 
snippet path/to/root --config=path/to/config.toml 
``` 
Config files can be specified as glob patterns, defaulting to `*.toml`, and can 
be set multiple times. Multiple files will be loaded in the order specified 
and discovered. Settings loaded last will take precedence. 

For more information about how to use the tool, please have a look at the [Usage page](./USAGE.md) 
The full CLI options are: 
``` 
> snippet --help 
usage: __main__.py [-h] [--config CONFIG] [-v] [dir] 
 
positional arguments: 
  dir              path to project root, used by any relative paths in loaded 
                   configs [cwd] 
 
optional arguments: 
  -h, --help       show this help message and exit 
  --config CONFIG  paths (or globs) to config files 
  -v, --verbosity  increase output verbosity 
``` 

Interface definition and usage documentation (for developers of tooling) is available for the most recent
production release here:

- [GitHub Pages](https://armmbed.github.io/snippet)

## Project Structure

The follow described the major aspects of the project structure:

- `azure-pipelines/` - CI configuration files for Azure Pipelines.
- `docs/` - Interface definition and usage documentation.
- `examples/` - Usage examples.
- `snippet/` - Python source files.
- `news/` - Collection of news files for unreleased changes.
- `tests/` - Unit and integration tests.

## Getting Help

- For interface definition and usage documentation, please see [GitHub Pages](https://armmbed.github.io/snippet).
- For a list of known issues and possible work arounds, please see [Known Issues](KNOWN_ISSUES.md).
- To raise a defect or enhancement please use [GitHub Issues](https://github.com/ARMmbed/snippet/issues).
- To ask a question please use the [Mbed Forum](https://forums.mbed.com/).

## Contributing

- Snippet is an open source project and we are committed to fostering a welcoming community, please see our
  [Code of Conduct](https://github.com/ARMmbed/snippet/blob/master/CODE_OF_CONDUCT.md) for more information.
- For ways to contribute to the project, please see the [Contributions Guidelines](https://github.com/ARMmbed/snippet/blob/master/CONTRIBUTING.md)
- For a technical introduction into developing this package, please see the [Development Guide](https://github.com/ARMmbed/snippet/blob/master/DEVELOPMENT.md)
