from __future__ import absolute_import

from test.test_client import TestClient


class TestController(TestClient):
    def test_info_endpoint(self):
        self.app.config['METADATA'] = {'test': 123}
        response = self.get_info()
        self.assertIn('name', response)
        self.assertIn('version', response)
        self.assertIn('test', response)


if __name__ == '__main__':
    import unittest

    unittest.main()
