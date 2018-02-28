import tempfile
import os
import unittest

from snippet.workflow import run
from snippet.config import Config

from tests import test_parser as P


class Test(unittest.TestCase):
    example_name = 'this snippet'
    text = ''.join([
        'blah blah\n', P.start, example_name, P.newline, P.A, P.B, P.stop, '# rhubarb\n'
    ])

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.tmp_fp = os.path.join(self.tmpdir.name, 'sample.txt')
        with open(self.tmp_fp, 'w') as fh:
            fh.write('\n')

    def test_read(self):
        with open(self.tmp_fp, 'w') as fh:
            fh.write(self.text)

        print(self.text)

        config = Config()
        config.stop_on_first_failure = True
        config.input_glob = self.tmp_fp
        config.output_dir = self.tmpdir.name

        examples, paths, failures = run(config)

        with self.subTest(part='found the file'):
            self.assertEqual([self.tmp_fp], paths)

        with self.subTest(part='no failures'):
            self.assertEqual([], failures)

        with self.subTest(part='one example extracted'):
            self.assertEqual(len(examples), 1)

        for k, v in examples.items():
            with self.subTest(part='example matches'):
                self.assertEqual('\n'.join(v), P.sample_output)
                self.assertEqual(k[-1], self.example_name)


class TestDuplicateNames(Test):
    text = ''.join([
        'blah blah\n', P.start, Test.example_name, P.newline, P.A, P.B, P.stop, '# rhubarb\n'
    ])
    text = text + '\n' + text

    def test_read(self):
        with self.assertRaises(Exception):
            super().test_read()
