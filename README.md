# snippet
[![CircleCI](https://circleci.com/gh/ARMmbed/snippet.svg?style=svg&circle-token=f8151197e9160de7877eda3ae049d0925e9b7ff3)](https://circleci.com/gh/ARMmbed/snippet)

A Python3 tool to extract code snippets from source files

Essentially, `snippet` extracts marked sections of text from a given
set of input files and saves them elsewhere.

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

## Getting started
### Prerequisites
- `snippet` requires Python 3

### Installation
```
pip install code-snippet
```
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
Run the following command in your project, using the Python interpreter you installed `snippet` to:

```
python -m snippet
```

Alternatively, run snippet from anywhere and specify a working directory and config file:
```
python -m snippet path/to/root --config=path/to/config.toml
```
Config files can be specified as glob patterns, defaulting to `*.toml`, and can
be set multiple times. Multiple files will be loaded in the order specified
and discovered. Settings loaded last will take precedence.

### Usage
For more information about how to use the tool, please have a look at the [Usage page](./USAGE.md)
The full CLI options are:
```
> python -m snippet --help
usage: __main__.py [-h] [--config CONFIG] [-v] [dir]

positional arguments:
  dir              path to project root, used by any relative paths in loaded
                   configs [cwd]

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  paths (or globs) to config files
  -v, --verbosity  increase output verbosity
```
