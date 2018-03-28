import unittest
import snippet
import os
import shutil
import filecmp

from tests import tmp_test_dir


class Test(unittest.TestCase):
    sample_input = os.path.join(os.path.dirname(__file__), 'samples')
    sample_output_dir = os.path.join(os.path.dirname(__file__), tmp_test_dir)

    def setUp(self):
        if os.path.exists(self.sample_output_dir):
            shutil.rmtree(self.sample_output_dir)

    def tearDown(self):
        shutil.rmtree(self.sample_output_dir)

    def test_run(self):
        # writing two different languages sequentially to the same file

        config = snippet.Config()
        config.output_dir = self.sample_output_dir
        config.output_append = True

        # only detect the python file
        config.input_glob = 'tests/samples/example.py'
        snippet.main(config=config)

        # only detect the java file
        config.output_template = '```java\n# example: {{{name}}}\n{{{code}}}\n```'
        config.input_glob = 'tests/samples/example.java'
        snippet.main(config=config)

        self.assertTrue(filecmp.cmp(
            os.path.join(self.sample_output_dir, 'number1.md'),
            os.path.join(self.sample_input, 'fixture.md'),
            shallow=False,
        ))
