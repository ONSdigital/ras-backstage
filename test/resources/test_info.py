import json
import os
import unittest
from pathlib import Path

from ras_backstage import app


class TestInfo(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_info_no_git_info(self):
        if Path('git_info').exists():
            os.remove('git_info')

        response = self.app.get("/info")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['name'], "ras-backstage")
        self.assertIsNone(response_data.get('test'))

    def test_info_with_git_info(self):
        with open('git_info', 'w') as outfile:
            json.dump({"test": "test"}, outfile)

        response = self.app.get("/info")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['name'], "ras-backstage")
        self.assertEqual(response_data['test'], "test")
