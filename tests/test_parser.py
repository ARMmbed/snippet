import unittest
from snippet.snippet import extract_snippets
from snippet.config import Config
from snippet import exceptions


start = f'# this is {Config.start_flag}: '
newline = '\n'
A = 'items = my_api().do_something()\n'
B = 'for item in items:\n'
C = '    print(item.name)\n'
stop = f'# {Config.end_flag}\n'
cloak = f'# {Config.cloak_flag}\n'
uncloak = f'# {Config.uncloak_flag}\n'

# however the output is combined, it should match this
sample_output = """items = my_api().do_something()\nfor item in items:\n    print(item.name)"""


class Test(unittest.TestCase):
    maxDiff = None

    def go(self, config, sequence):
        # shorthand to get the code equivalent post-parsing
        text = ''.join(sequence)
        result = extract_snippets(config, text.splitlines(), None)
        return ['\n'.join(block) for k, block in result.items()]

    def go_exact(self, config, sequence):
        # *really* shorthand, assumes the result matches the sample exactly
        self.assertEqual(
            sample_output,
            self.go(
                config,
                sequence
            )[0]
        )
        # print('test sequence:\n', ''.join(sequence))

    def test_empty(self):
        self.assertEqual(self.go(Config(), [start, 'test', newline, stop]), [])

    def test_plain(self):
        self.go_exact(Config(), [start, 'test', newline, A, B, C, stop])

    def test_indent(self):
        # left pad the sequence by two, to check result is dedented to depth of start
        sequence = [f'  {x}' for x in [start + 'test' + newline, A, B, C]]
        sequence.append(stop)
        self.go_exact(
            Config(),
            sequence
        )

    def test_trigger_phrase(self):
        with self.assertRaises(exceptions.ValidationFailure):
            self.go_exact(Config(), [start, 'test', newline, A, B, C, 'assert\n', stop])

    def test_dedent_code(self):
        with self.assertRaises(exceptions.ValidationFailure):
            sequence = [f'  {x}' for x in [start + 'test' + newline, A, B, C, stop]]
            sequence[-2] = sequence[-2].lstrip()
            self.go_exact(
                Config(),
                sequence
            )

    def test_unstarted(self):
        with self.assertRaises(exceptions.StartEndMismatch):
            self.go_exact(
                Config(),
                [A, B, C, stop]
            )

    def test_unfinished(self):
        with self.assertRaises(exceptions.StartEndMismatch):
            self.go_exact(
                Config(),
                [start, 'test', newline, A, B, C]
            )

    def test_double_start(self):
        with self.assertRaises(exceptions.StartEndMismatch):
            self.go_exact(
                Config(),
                [start, 'test', newline, A, start, 'test again', newline, B, C, stop]
            )

    def test_double_stop(self):
        with self.assertRaises(exceptions.StartEndMismatch):
            self.go_exact(
                Config(),
                [start, 'test', newline, A, stop, B, C, stop]
            )

    def test_prefix(self):
        self.go_exact(
            Config(),
            ['some other stuff', start, 'test', newline, A, B, C, stop, 'other stuff']
        )

    def test_cloak(self):
        self.go_exact(
            Config(),
            ['some other stuff\n', start, 'test', newline,
             A,
             cloak,
             'ignore this stuff\n',
             uncloak,
             B, C,
             stop, 'other stuff']
        )

    def test_cloak_unstarted(self):
        with self.assertRaises(exceptions.CloakMismatch):
            self.go_exact(
                Config(),
                ['some other stuff', start, 'test', newline, A, uncloak, B, C, stop, 'other stuff']
            )

    def test_cloak_unfinished(self):
        with self.assertRaises(exceptions.CloakMismatch):
            self.go_exact(
                Config(),
                ['some other stuff', start, 'test', newline, A, cloak, B, C, stop, 'other stuff']
            )

    def test_multiple(self):
        sequence = [
            'some other stuff',
            start, 'test 1 ', newline,
            A,
            cloak,
            'something to hide?',
            uncloak,
            B, C,
            stop,
            'other stuff',
            'more other stuff',
            start, ' test 2  ', newline,
            A,
            B, C,
            stop,
            'more stuff'
        ]
        for i, parsed in enumerate(self.go(Config(), sequence)):
            with self.subTest(attempt=i):
                self.assertEqual(sample_output, parsed)
