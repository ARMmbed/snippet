import unittest
from snippet.snippet import extract_examples
from snippet.config import Config


newline = '\n'
start = f'# this is {Config.start_flag}: '
A = """items = my_api().do_something()\n"""
B = """for item in items:\n    print(item.name)\n"""
stop = f'# {Config.end_flag}\n'
cloak = f'# {Config.start_cloak_flag}\n'
uncloak = f'# {Config.start_uncloak_flag}\n'

# however the output is combined, it should match this
sample_output = """items = my_api().do_something()\nfor item in items:\n    print(item.name)"""


class Test(unittest.TestCase):
    maxDiff = None

    def go(self, config, sequence):
        # shorthand to get the code equivalent post-parsing
        text = ''.join(sequence)
        result = extract_examples(config, text.splitlines(), None)
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

    def test_empty(self):
        self.assertEqual(self.go(Config(), [start, 'test', newline, stop]), [])

    def test_plain(self):
        self.go_exact(Config(), [start, 'test', newline, A, B, stop])

    def test_indent(self):
        # left pad the sequence by two
        sequence = [f'  {x}' for x in [start + 'test' + newline, A, B]]
        sequence.append(stop)
        self.go_exact(
            Config(),
            sequence
        )

    @unittest.expectedFailure
    def test_dedent_code(self):
        sequence = [f'  {x}' for x in [start + 'test' + newline, A, B, stop]]
        sequence[-2] = sequence[-2].lstrip()
        self.go_exact(
            Config(),
            sequence
        )

    @unittest.expectedFailure
    def test_unstarted(self):
        self.go_exact(
            Config(),
            [A, B, stop]
        )

    @unittest.expectedFailure
    def test_unfinished(self):
        self.go_exact(
            Config(),
            [start, 'test', newline, A, B]
        )

    @unittest.expectedFailure
    def test_double_start(self):
        self.go_exact(
            Config(),
            [start, 'test', newline, A, start, 'test again', newline, B, stop]
        )

    @unittest.expectedFailure
    def test_double_stop(self):
        self.go_exact(
            Config(),
            [start, 'test', newline, A, stop, B, stop]
        )

    def test_prefix(self):
        self.go_exact(
            Config(),
            ['some other stuff', start, 'test', newline, A, B, stop, 'other stuff']
        )

    def test_cloak(self):
        self.go_exact(
            Config(),
            ['some other stuff', start, 'test', newline,
             A,
             cloak,
             'ignore this stuff\n',
             uncloak,
             B,
             stop, 'other stuff']
        )

    @unittest.expectedFailure
    def test_cloak_unstarted(self):
        self.go_exact(
            Config(),
            ['some other stuff', start, 'test', newline, A, uncloak, B, stop, 'other stuff']
        )

    @unittest.expectedFailure
    def test_cloak_unfinished(self):
        self.go_exact(
            Config(),
            ['some other stuff', start, 'test', newline, A, cloak, B, stop, 'other stuff']
        )

    def test_multiple(self):
        sequence = [
            'some other stuff',
            start, 'test 1 ', newline,
            A,
            cloak,
            'something to hide?',
            uncloak,
            B,
            stop,
            'other stuff',
            'more other stuff',
            start, ' test 2  ', newline,
            A,
            B,
            stop,
            'more stuff'
        ]
        for i, parsed in enumerate(self.go(Config(), sequence)):
            with self.subTest(attempt=i):
                self.assertEqual(sample_output, parsed)
