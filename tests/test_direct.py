#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
import unittest
from snippet import config as snippet_config, api
from pathlib import Path
import shutil
import filecmp

from tests import tmp_test_dir
from tests import sample_input_dir


class Test(unittest.TestCase):
    def tearDown(self):
        shutil.rmtree(tmp_test_dir)

    def test_run(self):
        # writing two different languages sequentially to the same file

        config = snippet_config.Config()
        config.output_dir = tmp_test_dir
        config.output_append = True

        # only detect the python file
        config.input_glob = Path(sample_input_dir).joinpath("example.py")
        api.extract_code_snippets(config=config)

        # only detect the java file
        config.input_glob = Path(sample_input_dir).joinpath("example.java")
        config.language_name = "java"
        config.comment_prefix = "// "
        api.extract_code_snippets(config=config)

        self.assertTrue(
            filecmp.cmp(
                Path(tmp_test_dir).joinpath("number_1.md"), Path(sample_input_dir).joinpath("fixture.md"), shallow=False
            )
        )
