import os
import shutil
import subprocess
import sys
import textwrap
import unittest

import snippet


class Test(unittest.TestCase):
    tmpdir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tmp_test_dir')

    @classmethod
    def setUpClass(cls):
        # use a plain directory not-really-in-tmp to avoid cross-process perms issues in windows
        os.makedirs(cls.tmpdir)
        cls.tmp_fp = os.path.join(cls.tmpdir, 'config.toml')
        with open(cls.tmp_fp, 'w') as fh:
            fh.write(textwrap.dedent("""
            [snippet]
            input_glob = '*'
            end_flag = 'custom value'
            stop_on_first_failure = true
            foo = 'bar'            
            """).lstrip())

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmpdir)

    def test_config_from_file(self):
        config = snippet.config.get_config(config_path=self.tmp_fp)
        self.assertEqual(config.end_flag, 'custom value')
        self.assertEqual(config.foo, 'bar')

    def test_config_from_cli(self):
        with self.assertRaises(subprocess.CalledProcessError) as ctx:
            subprocess.check_output(
                [sys.executable, '-m', 'snippet', '--config', self.tmp_fp],
                cwd=self.tmpdir,
                stderr=subprocess.STDOUT
            )
        self.assertIn('snippet.exceptions', str(ctx.exception.output))
