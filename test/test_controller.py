from __future__ import absolute_import

import json
from unittest.mock import patch, MagicMock

from test.test_client import TestClient


class TestController(TestClient):
    def test_info_endpoint(self):
        self.app.config['METADATA'] = {'test': 123}
        response = self.get_info()
        self.assertIn('name', response)
        self.assertIn('version', response)
        self.assertIn('test', response)

    @patch('ras_backstage.controllers.controller.requests')
    def test_proxy_endpoint_proxies_a_get_request(self, mock):
        mock.request = MagicMock()
        self.app.config.dependency = {
            'mock-service': {
                'scheme': 'httpx',
                'host': '1.2.3.4',
                'port': '4321'
            }
        }
        response = self.client.get('/backstage-api/v1/mock-service/a')
        self.assertEqual(response.status_code, 200)

        mock.request.assert_called_once()
        call_args = mock.request.call_args[1]
        self.assertIn('method', call_args)
        self.assertEqual(call_args['method'], 'GET')
        self.assertIn('url', call_args)
        self.assertEqual(call_args['url'], 'httpx://1.2.3.4:4321/a')

    @patch('ras_backstage.controllers.controller.requests')
    def test_proxy_endpoint_proxies_supplied_path(self, mock):
        mock.request = MagicMock()
        self.app.config.dependency = {
            'mock-service': {
                'scheme': 'httpx',
                'host': '1.2.3.4',
                'port': '4321'
            }
        }
        self.client.get('/backstage-api/v1/mock-service/path/to/endpoint/')

        mock.request.assert_called_once()
        call_args = mock.request.call_args[1]
        self.assertIn('url', call_args)
        self.assertEqual(call_args['url'], 'httpx://1.2.3.4:4321/path/to/endpoint/')

    @patch('ras_backstage.controllers.controller.requests')
    def test_proxy_endpoint_proxies_query_params(self, mock):
        mock.request = MagicMock()
        self.app.config.dependency = {
            'mock-service': {
                'scheme': 'httpx',
                'host': '1.2.3.4',
                'port': '4321'
            }
        }
        self.client.get('/backstage-api/v1/mock-service/path/to/endpoint/?a=1&b=2&a=3')

        mock.request.assert_called_once()
        call_args = mock.request.call_args[1]
        self.assertIn('url', call_args)
        self.assertEqual(call_args['url'], 'httpx://1.2.3.4:4321/path/to/endpoint/')
        self.assertIn('params', call_args)
        self.assertDictEqual(call_args['params'], {'a': ['1', '3'], 'b': '2'})

    @patch('ras_backstage.controllers.controller.requests')
    def test_proxy_endpoint_proxies_post_body(self, mock):
        mock.request = MagicMock()
        self.app.config.dependency = {
            'mock-service': {
                'scheme': 'httpx',
                'host': '1.2.3.4',
                'port': '4321'
            }
        }
        mock_body = dict(foo='bar')
        self.client.post('/backstage-api/v1/mock-service/path/to/endpoint/?a=1&b=2&a=3', data=json.dumps(mock_body))

        mock.request.assert_called_once()
        call_args = mock.request.call_args[1]
        self.assertIn('data', call_args)
        self.assertDictEqual(json.loads(call_args['data']), mock_body)

    def test_proxy_endpoint_proxies_a_post_request(self):
        pass

    def test_proxy_endpoint_proxies_a_put_request(self):
        pass

    def test_proxy_endpoint_proxies_a_delete_request(self):
        pass

    def test_proxy_endpoint_throws_on_unknown_service(self):
        pass

    def test_proxy_endpoint_proxies_headers(self):
        pass

    def test_proxy_endpoint_proxies_downstream_errors(self):
        pass

    def test_proxy_endpoint_raises_for_incorrect_config(self):
        pass


if __name__ == '__main__':
    import unittest

    unittest.main()
