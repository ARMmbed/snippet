import tempfile
import os
import unittest

from snippet import exceptions
from snippet import workflow
from snippet.config import Config

from tests import test_parser as P


class Test(unittest.TestCase):
    example_name = 'this snippet'
    text = ''.join([
        'blah blah\n', P.start, example_name, P.newline, P.A, P.B, P.C, P.stop, '# rhubarb\n'
    ])

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.tmp_fp = os.path.join(self.tmpdir.name, 'sample.txt')
        with open(self.tmp_fp, 'w') as fh:
            fh.write('\n')

    def test_read(self):
        with open(self.tmp_fp, 'w') as fh:
            fh.write(self.text)

        config = Config()
        config.stop_on_first_failure = True
        config.input_glob = self.tmp_fp
        config.output_dir = self.tmpdir.name

        examples, paths, failures = workflow.run(config)

        with self.subTest(part='found the file'):
            self.assertEqual([self.tmp_fp], paths)

        with self.subTest(part='no failures'):
            self.assertEqual([], failures)

        with self.subTest(part='one example extracted'):
            self.assertGreaterEqual(len(examples), 1)

        for k, v in examples.items():
            with self.subTest(part='example matches'):
                self.assertEqual('\n'.join(v), P.sample_output)
                self.assertIn(self.example_name, k[-1])


class TestMultipleExtract(Test):
    text = ''.join([
        'blah blah\n', P.start, Test.example_name, P.newline, P.A, P.B, P.C, P.stop, '# rhubarb\n'
    ])
    text = text + '\n' + text.replace(Test.example_name, 'this snippet 2')

    def test_read(self):
        super().test_read()


class TestDuplicateNames(Test):
    text = ''.join([
        'blah blah\n', P.start, Test.example_name, P.newline, P.A, P.B, P.C, P.stop, '# rhubarb\n'
    ])
    text = text + '\n' + text

    def test_read(self):
        with self.assertRaises(exceptions.DuplicateName):
            super().test_read()
