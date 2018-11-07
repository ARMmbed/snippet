# Usage

## Extracting code snippet for documentation purposes

Say you have an API that you would like to document and test using the same code:
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

`snippet` can be used to extract the useful documentation that is buried in this test code:
i.e.
```python
# listing api items
items = api.list_items()
for item in items:
    print(item)
```

It does this using a customisable markup syntax:

_see section delimiters `# an example` and `# end of example`  in the code below_
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

## Cloaking
Due to the test system in use, there may be some test related hooks in the code which should not be present in the documentation:

_e.g. `assert ...`_
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
`snippet` can exclude lines from the output using specific keywords:
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
This ensures that documentation only contains relevant code, without compromising on test quality:
```python
# listing api items
items = api.list_items()
for item in items:
    print(item)
```

## Validation
Because `snippet` is language-agnostic it is unlikely that an
IDE would detect invalid snippets, or changes to code that may break them.

`snippet` can be configured to validate snippets to avoid the syntax from
introducing bizarre broken documentation to your users. That said, it can't
do everything - and it's still wise to QA your docs from time to time.
Some of the checks include:
- Tag open / close matches (avoiding nested examples or cloaks)
- Examples left unterminated
- Indents reducing beyond the start level for the current example

## Notable configuration options

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
