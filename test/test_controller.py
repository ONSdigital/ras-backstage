from __future__ import absolute_import

from test.test_client import TestClient


class TestController(TestClient):
    def test_info_endpoint(self):
        response = self.get_info()
        self.assertIn('name', response)
        self.assertIn('version', response)
        self.assertIn('origin', response)


if __name__ == '__main__':
    import unittest

    unittest.main()
