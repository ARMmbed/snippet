import os
import shutil
import filecmp
import subprocess
import sys
import textwrap
import unittest

import snippet

from tests import tmp_test_dir
from tests import sample_input_dir


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # use a plain directory not-really-in-tmp to avoid cross-process perms issues in windows
        os.makedirs(tmp_test_dir)
        cls.tmp_fp = os.path.join(tmp_test_dir, 'config.toml')
        with open(cls.tmp_fp, 'w') as fh:
            fh.write(textwrap.dedent("""
            [snippet]
            # an example: this config is itself an example
            input_glob = '*'
            
            stop_on_first_failure = true
            end_flag = 'custom value'
            
            foo = 'bar'
            """).lstrip())

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(tmp_test_dir)

    def test_config_from_file(self):
        # explicitly load config from a file
        config = snippet.config.get_config(config_path=self.tmp_fp)
        self.assertEqual(config.end_flag, 'custom value')
        self.assertEqual(config.foo, 'bar')

    def test_config_from_cli(self):
        # load config when run as a module
        subprocess.check_call(
            [sys.executable, '-m', 'snippet', tmp_test_dir, '--config', self.tmp_fp],
            stderr=subprocess.STDOUT
        )

        self.assertTrue(filecmp.cmp(
            os.path.join(tmp_test_dir, 'thisconfigisitselfanexample.md'),
            os.path.join(sample_input_dir, 'config_fixture.md'),
            shallow=False,
        ))

    def test_auto_config(self):
        # load config, without explicitly setting the config path
        config = snippet.config.get_config()
        self.assertEqual(config.end_flag, 'custom value')
        self.assertEqual(config.foo, 'bar')
