# snippet

## purpose
Extract text snippets from files.

This works on plain old text files of any kind.
- Works on any language, reading from source
- Customisable syntax
- Write to templated output (e.g. `.md` triple quotes)
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
Because `snippet` is language-agnostic it is also unlikely that an
IDE would detect invalid snippets, or changes to code that may break them.

`snippet` can be configured to validate snippets to avoid the syntax from
introducing bizarre broken documentation to your users. That said, it can't
do everything - and it's still wise to QA your docs from time to time.
Some of the checks include:
- Tag open / close matches (can't nest examples or cloaks)
- Examples left unterminated
- Indents reducing beyond the start level for the current example

# future work
This is best tracked with proper issues, but areas to work on may include:

- [x] Pep8 compliance
- [x] Test coverage
- [x] Refactor
- [x] Cloaking (disabling capture, without making a new snippet)
- [ ] Test config load
- [ ] Template workflow
- [ ] Parsing with regex
- [ ] Parsing performance
