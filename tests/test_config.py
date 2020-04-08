#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import os
import shutil
import filecmp
import subprocess
import sys
import textwrap
import unittest

from snippet import config as snippet_config

from tests import tmp_test_dir
from tests import sample_input_dir


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # use a plain directory not-really-in-tmp to avoid cross-process perms issues in windows
        os.makedirs(tmp_test_dir)
        cls.tmp_fp = os.path.join(tmp_test_dir, "config.toml")
        with open(cls.tmp_fp, "w", encoding="utf8") as fh:
            fh.write(
                textwrap.dedent(
                    """
            [snippet]
            # an example: this config is itself an example
            input_glob = "does not match anything"

            stop_on_first_failure = true
            end_flag = "custom value"

            foo = "bar"
            fizz = "buzz"
            """
                ).lstrip()
            )

        cls.tmp_fp_2 = os.path.join(tmp_test_dir, "config2.toml")
        with open(cls.tmp_fp_2, "w", encoding="utf8") as fh:
            fh.write(
                textwrap.dedent(
                    """
            [snippet]
            input_glob = 'config.toml'

            foo = 'baz'
            """
                ).lstrip()
            )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(tmp_test_dir)

    def test_config_from_file(self):
        # explicitly load config from a file
        config = snippet_config.get_config(config_paths=[self.tmp_fp])
        self.assertEqual(config.end_flag, "custom value")
        self.assertEqual(config.foo, "bar")
        self.assertEqual(config.fizz, "buzz")

    def test_config_from_multi_globs(self):
        # explicitly load from two files
        config = snippet_config.get_config(config_paths=[self.tmp_fp, self.tmp_fp_2])
        self.assertEqual(config.foo, "baz")
        self.assertEqual(config.fizz, "buzz")

    def test_config_from_cli(self):
        # load config when run as a module
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "snippet",
                str(tmp_test_dir),
                "--config",
                str(self.tmp_fp),
                "--config",
                str(self.tmp_fp_2),
            ],
            stderr=subprocess.STDOUT,
        )

        self.assertTrue(
            filecmp.cmp(
                os.path.join(tmp_test_dir, "this_config_is_itself_an_example.md"),
                os.path.join(sample_input_dir, "config_fixture.md"),
                shallow=False,
            )
        )

    def test_auto_config(self):
        # load config, without explicitly setting the config path
        config = snippet_config.get_config()
        self.assertEqual(config.end_flag, "custom value")
        self.assertEqual(config.fizz, "buzz")
