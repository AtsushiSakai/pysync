import unittest
import pysync


class PySyncTestCase(unittest.TestCase):

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            pysync.sync("../", "../", [])

        with self.assertRaises(TypeError):
            pysync.sync(["../"], [], [])

        with self.assertRaises(TypeError):
            pysync.sync(["../"], "../", ".git")

        with self.assertRaises(ValueError):
            pysync.sync(["/hoge"], "../", [".git"])


if __name__ == '__main__':
    unittest.main()
