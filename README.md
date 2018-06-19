# snippet
[![CircleCI](https://circleci.com/gh/ARMmbed/snippet.svg?style=svg&circle-token=f8151197e9160de7877eda3ae049d0925e9b7ff3)](https://circleci.com/gh/ARMmbed/snippet)

A Python3 tool to extract text snippets from files

## features
Primarily snippet extracts marked sections of text from a given
set of input files, and saves them elsewhere. Features include:

- Works on any text file, e.g.
any coding language by reading from source files
- Customisable markup syntax
- Writes to templated output (e.g. `.md` code blocks)
- Hide sections from output
- Validation to help avoid snippets breaking as code changes

## motivation
Investigating approaches for having language-native code
tested and displayed in documentation.
- The docs need a written example demonstrating use of some code
- But documentation can become outdated, or contain its own errors
- Treat documentation examples as you would any other code in your project
- So write some tests for them!
- But it can be hard to instrument examples in a testable way... typically tests need:
  - Setup
  - Assertions
  - Hooks, grey-box tweaking and other checks
  - Teardown

One approach, using `snippet`, is to extract the useful (customer readable!) part of the example from
within the test, ready for rendering in the docs.

# getting started
## prerequisite
`snippet` requires Python 3

## install
Something like:
```
git clone ARMmbed/snippet
pip install -e path/to/snippet
```
or directly (with `pip`>10 environment variables can be unpacked):
```
python -m pip install -U pip>10
pip install git+https://${GH_TOKEN}@github.com/ARMmbed/snippet.git#egg=snippet
```

## configure
Place a config file in the [toml format](https://github.com/toml-lang/toml)
in your project directory (e.g. `snippet.toml`). Any value defined in [the config object](https://github.com/ARMmbed/snippet/blob/master/src/snippet/config.py#L8)
can be overridden.

As an example, basic configuration typically includes input and output directories:

```
[snippet]
input_glob = 'tests/unit/*.py'
output_dir = 'docs/examples'
```

## run
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

# usage
## example
Say you have an API that you would like to document and test:
```
class MyTest():
    def setUp():
        self.load_fixtures()

    def test():
        import my_api
        api = my_api()
        items = api.list_items()
        for item in items:
            print(item)
        assert len(items) > 1
```

`snippet` can be used to extract the useful documentation that's buried in this code:
```python
# listing api items
items = api.list_items()
for item in items:
    print(item)
```

It does this using a customisable markup syntax:
```
class MyTest():
    def setUp():
        self.load_fixtures()

    def test():
        import my_api
        api = my_api()
        # an example: listing api items
        items = api.list_items()
        for item in items:
            print(item)
        # end of example
        assert len(items) > 1
```

## cloaking
Maybe you can't escape a janky test hook in your code, or you don't fancy
 having a separate file for your doc tests:
```
import my_api
api = my_api()
items = api.list_items()
for item in items:
    assert 'id' in item
    assert item.size > 42
    print(item)
assert len(items) > 1
```
`snippet` can exclude lines from the output:
```
import my_api
api = my_api()
# an example: listing api items
items = api.list_items()
for item in items:
    # cloak
    assert 'id' in item
    assert item.size > 42
    # uncloak
    print(item)
# end of example
assert len(items) > 1
```
Once again this gives the thoroughly readable:
```python
# listing api items
items = api.list_items()
for item in items:
    print(item)
```

## validation
Because `snippet` is language-agnostic it is unlikely that an
IDE would detect invalid snippets, or changes to code that may break them.

`snippet` can be configured to validate snippets to avoid the syntax from
introducing bizarre broken documentation to your users. That said, it can't
do everything - and it's still wise to QA your docs from time to time.
Some of the checks include:
- Tag open / close matches (avoiding nested examples or cloaks)
- Examples left unterminated
- Indents reducing beyond the start level for the current example

## notable config options

Any parameter in the default configuration can be overridden.

Some notable entries include:

- `language_name` passed to the output template; can improve markdown rendering
in syntax-aware renderers
- `drop_lines` for removing entire lines containing these exact matches
- `replacements` for globally replacing exact matches

```python
# IO
project_root = '.'  # the project root used for relative IO paths (set by commandline)
input_glob = 'tests/example/*.py'
output_append = True  # if the output file exists, append to it
output_dir = '.'
output_file_name_template = '{{name}}.md'  # a mustache template for the output file name
write_attempts = 3  # number of retries when writing output files

# Language and style
language_name = 'python'
comment_prefix = '# '
comment_suffix = ''
# a mustache template for each file (triple braces important for code literals, no escaping)
output_template = '```{{language_name}}\n{{comment_prefix}}example: {{{name}}}{{comment_suffix}}\n{{{code}}}\n```\n'

# Logger
log_level = logging.INFO

# Code block indicators
start_flag = 'an example'
end_flag = 'end of example'

# Hidden block indicators
cloak_flag = 'cloak'
uncloak_flag = 'uncloak'

# Validation and formatting logic
drop_lines = []  # drop lines containing these phrases
replacements = {'self.': ''}  # straightforward replacements
fail_on_contains = ['assert']  # fail if these strings are found in code blocks
auto_dedent = True  # keep code left-aligned with the start flag
fail_on_dedent = True  # fail if code is dedented before reaching the end flag
stop_on_first_failure = False  # fail early
```
