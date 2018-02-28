import unittest

from snippet.wrapper import wrap
from snippet.config import Config


class Test(unittest.TestCase):
    def test_wrap_passthrough(self):
        counter = {'a': 0}

        def x():
            counter['a'] += 1
            return counter

        f = []
        result = wrap(Config(), f, None, x)

        self.assertEqual(result, counter)
        self.assertEqual(counter['a'], 1)
        self.assertEqual(f, [])

    def test_wrap_raises(self):
        def x():
            raise NotImplementedError()
        config = Config()
        config.stop_on_first_failure = True
        f = []
        with self.assertRaises(NotImplementedError):
            wrap(config, f, None, x)

    def test_wrap_wraps(self):
        def x():
            raise NotImplementedError()
        config = Config()
        config.stop_on_first_failure = False
        f = []
        result = wrap(config, f, None, x)

        self.assertIsNone(result)
        self.assertEqual(len(f), 1)
        self.assertIsNone(f[0][0])
        self.assertIn('Traceback', f[0][1])
