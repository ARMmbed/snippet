import unittest
import snippet
import os
import shutil
import filecmp

from tests import tmp_test_dir
from tests import sample_input_dir


class Test(unittest.TestCase):

    def tearDown(self):
        shutil.rmtree(tmp_test_dir)

    def test_run(self):
        # writing two different languages sequentially to the same file

        config = snippet.Config()
        config.output_dir = tmp_test_dir
        config.output_append = True

        # only detect the python file
        config.input_glob = 'tests/samples/example.py'
        snippet.main(config=config)

        # only detect the java file
        config.output_template = '```java\n# example: {{{name}}}\n{{{code}}}\n```'
        config.input_glob = 'tests/samples/example.java'
        snippet.main(config=config)

        self.assertTrue(filecmp.cmp(
            os.path.join(tmp_test_dir, 'number1.md'),
            os.path.join(sample_input_dir, 'fixture.md'),
            shallow=False,
        ))
