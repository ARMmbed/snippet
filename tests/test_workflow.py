#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import tempfile
import unittest
from pathlib import Path

from snippet import exceptions
from snippet import workflow
from snippet.config import Config
from tests import test_parser as P


class Test(unittest.TestCase):
    example_name = "this snippet"
    expect_examples = 1
    text = "".join(["blah blah\n", P.start, example_name, P.newline, P.A, P.B, P.C, P.stop, "# rhubarb\n"])

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.tmp_fp = str(Path(self.tmpdir.name).joinpath("sample.txt"))
        with open(self.tmp_fp, "w", encoding="utf8") as fh:
            fh.write("\n")

    def test_read(self):
        with open(self.tmp_fp, "w", encoding="utf8") as fh:
            fh.write(self.text)

        config = Config()
        config.stop_on_first_failure = True
        config.input_glob = self.tmp_fp
        config.output_dir = self.tmpdir.name

        examples, paths, failures = workflow.run(config)

        with self.subTest(part="found the file"):
            self.assertEqual([self.tmp_fp], paths)

        with self.subTest(part="no failures"):
            self.assertEqual([], failures)

        with self.subTest(part="one example extracted"):
            self.assertEqual(len(examples), self.expect_examples)

        for k, v in examples.items():
            with self.subTest(part="example matches"):
                self.assertEqual("\n".join(v), P.sample_output)
                self.assertIn(self.example_name, k[-1])

    def tearDown(self):
        if self.tmpdir:
            self.tmpdir.cleanup()
            self.tmpdir = None


class TestMultipleExtract(Test):
    # two examples in one file
    expect_examples = 2
    text = "".join(["blah blah\n", P.start, Test.example_name, P.newline, P.A, P.B, P.C, P.stop, "# rhubarb\n"])
    text = text + "\n" + text.replace(Test.example_name, "this snippet 2")


class TestDuplicateNames(Test):
    text = "".join(["blah blah\n", P.start, Test.example_name, P.newline, P.A, P.B, P.C, P.stop, "# rhubarb\n"])
    text = text + "\n" + text

    def test_read(self):
        with self.assertRaises(exceptions.DuplicateName):
            super().test_read()


class TestNoExamplesInFile(Test):
    expect_examples = 0
    text = "".join(["blah blah\n", Test.example_name, P.newline, P.A, P.B, P.C, "# rhubarb\n"])
    text = text + "\n" + text
