from __future__ import absolute_import

import json
from unittest.mock import patch, MagicMock

from jose import JWTError
from ras_common_utils.ras_error.ras_error import RasError

from test.test_client import TestClient


class MockResponse:

    def __init__(self, status_code, body=None):
        self.status_code = status_code
        self._body = body or {'response': "test"}

    def raise_for_status(self):
        status_category = int(self.status_code / 100)
        if status_category != 2:
            raise RasError(["Mock error"], status_code=self.status_code)

    def json(self):
        return self._body


class TestController(TestClient):
    def test_info_endpoint(self):
        self.app.config['METADATA'] = {'test': 123}
        response = self.get_info()
        self.assertIn('name', response)
        self.assertIn('version', response)
        self.assertIn('test', response)

    @patch('ras_backstage.controllers.controller.requests')
    def test_proxy_endpoint_proxies_a_get_request(self, mock):
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
    def test_proxy_endpoint_proxies_a_post_request(self, mock):
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
        self.assertIn('method', call_args)
        self.assertEqual(call_args['method'], 'POST')
        self.assertIn('data', call_args)
        self.assertDictEqual(json.loads(call_args['data']), mock_body)

    @patch('ras_backstage.controllers.controller.requests')
    def test_proxy_endpoint_proxies_a_put_request(self, mock):
        self.app.config.dependency = {
            'mock-service': {
                'scheme': 'httpx',
                'host': '1.2.3.4',
                'port': '4321'
            }
        }
        mock_body = dict(foo='bar')
        self.client.put('/backstage-api/v1/mock-service/path/to/endpoint/?a=1&b=2&a=3', data=json.dumps(mock_body))

        mock.request.assert_called_once()
        call_args = mock.request.call_args[1]
        self.assertIn('method', call_args)
        self.assertEqual(call_args['method'], 'PUT')
        self.assertIn('data', call_args)
        self.assertDictEqual(json.loads(call_args['data']), mock_body)

    @patch('ras_backstage.controllers.controller.requests')
    def test_proxy_endpoint_proxies_a_delete_request(self, mock):
        self.app.config.dependency = {
            'mock-service': {
                'scheme': 'httpx',
                'host': '1.2.3.4',
                'port': '4321'
            }
        }
        self.client.delete('/backstage-api/v1/mock-service/path/to/endpoint/?a=1&b=2&a=3')

        mock.request.assert_called_once()
        call_args = mock.request.call_args[1]
        self.assertIn('method', call_args)
        self.assertEqual(call_args['method'], 'DELETE')

    def test_proxy_endpoint_responds_404_for_unknown_service(self):
        resp = self.client.get('/backstage-api/v1/mock-service/path/to/endpoint/?a=1&b=2&a=3')
        self.assertEqual(resp.status_code, 404)

    @patch('ras_backstage.controllers.controller.requests')
    def test_proxy_endpoint_proxies_headers(self, mock):
        self.app.config.dependency = {
            'mock-service': {
                'scheme': 'httpx',
                'host': '1.2.3.4',
                'port': '4321'
            }
        }
        response = self.client.get('/backstage-api/v1/mock-service/a',
                                   headers={'bar': 'baz',
                                            'Authorization': 'wibble',
                                            'Content-Type': 'application/stuff'})
        self.assertEqual(response.status_code, 200)

        mock.request.assert_called_once()
        call_args = mock.request.call_args[1]
        self.assertIn('method', call_args)
        self.assertEqual(call_args['method'], 'GET')
        self.assertIn('headers', call_args)
        self.assertEqual(call_args['headers'].get('Authorization'), 'wibble')
        self.assertEqual(call_args['headers'].get('Content-Type'), 'application/stuff')
        self.assertEqual(call_args['headers'].get('bar'), None)

    @patch('ras_backstage.controllers.controller.requests')
    def test_proxy_endpoint_proxies_downstream_errors(self, mock):
        mock.request.return_value = MockResponse(status_code=400)
        self.app.config.dependency = {
            'mock-service': {
                'scheme': 'httpx',
                'host': '1.2.3.4',
                'port': '4321'
            }
        }
        response = self.client.get('/backstage-api/v1/mock-service/a')
        self.assertEqual(response.status_code, 400)

    @patch('ras_backstage.controllers.controller.requests')
    def test_proxy_endpoint_raises_for_incorrect_config(self, mock):
        self.app.config.dependency = {
            'mock-service': {
                'host': '1.2.3.4',
                'port': '4321'
            }
        }
        response = self.client.get('/backstage-api/v1/mock-service/a')
        self.assertEqual(response.status_code, 500)

    @patch('ras_backstage.controllers.controller.requests')
    def test_sign_in_calls_the_oauth_endpoint_with_the_correct_parameters(self, mock):
        mock.post.return_value = MockResponse(status_code=201, body={'expires_in': '1'})
        payload = {'username': 'testuser', 'password': 'abcd'}
        response = self.client.post('/backstage-api/v1/sign_in',
                                    data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

        mock.post.assert_called_once()
        call_args = mock.post.call_args[0]
        self.assertEqual(call_args[0], "http://mockhost:4444/api/v1/tokens/")

        call_kws = mock.post.call_args[1]
        self.assertIn('auth', call_kws)
        self.assertEqual(call_kws['auth'], ('ons@ons.gov', 'password'))
        self.assertIn('headers', call_kws)
        self.assertDictEqual(call_kws['headers'], {'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertIn('data', call_kws)
        self.assertEqual(call_kws['data'], 'grant_type=password&username=testuser&password=abcd')

    @patch('ras_backstage.controllers.controller.requests')
    def test_sign_in_generates_a_token(self, mock):
        mock.post.return_value = MockResponse(status_code=201, body={'expires_in': '1'})
        payload = {'username': 'testuser', 'password': 'abcd'}
        response = self.client.post('/backstage-api/v1/sign_in',
                                    data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

        self.assertIn('token', response.json)

    @patch('ras_backstage.controllers.controller.requests')
    def test_sign_in_without_body_returns_a_400(self, mock):
        mock.post.return_value = MockResponse(status_code=201)
        response = self.client.post('/backstage-api/v1/sign_in',
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.json)
        self.assertIn('No JSON supplied in request body.', response.json['errors'])

    @patch('ras_backstage.controllers.controller.requests')
    def test_sign_in_without_username_password_returns_a_400(self, mock):
        mock.post.return_value = MockResponse(status_code=201)
        response = self.client.post('/backstage-api/v1/sign_in',
                                    data=json.dumps({'foo': 'bar'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.json)
        self.assertIn('username is missing from the JSON body.', response.json['errors'])
        self.assertIn('password is missing from the JSON body.', response.json['errors'])

    @patch('ras_backstage.controllers.controller.requests')
    @patch('ras_backstage.controllers.controller.jwt')
    @patch('ras_backstage.controllers.controller.datetime')
    def test_request_with_valid_jwt_is_proxied(self, mock_datetime, mock_jwt, mock_requests):
        self.app.config.feature = {'validate_jwt': True}
        mock_datetime.now.return_value = 100
        mock_datetime.fromtimestamp = lambda x: x
        mock_jwt.decode.return_value = {'expires_at': 123}

        self.app.config.dependency = {
            'mock-service': {
                'scheme': 'httpx',
                'host': '1.2.3.4',
                'port': '4321'
            }
        }
        response = self.client.get('/backstage-api/v1/mock-service/a', headers={'authorization': 'abc'})
        self.assertEqual(response.status_code, 200)

    @patch('ras_backstage.controllers.controller.requests')
    @patch('ras_backstage.controllers.controller.jwt')
    @patch('ras_backstage.controllers.controller.datetime')
    def test_request_with_invalid_jwt_returns_401(self, mock_datetime, mock_jwt, mock_requests):
        self.app.config.feature = {'validate_jwt': True}
        mock_datetime.now.return_value = 100
        mock_datetime.fromtimestamp = lambda x: x
        mock_jwt.decode.side_effect = JWTError('foo')
        mock_requests.request = MagicMock()
        response = self.client.get('/backstage-api/v1/mock-service/a', headers={'authorization': 'abc'})
        self.assertEqual(response.status_code, 401)

    @patch('ras_backstage.controllers.controller.requests')
    @patch('ras_backstage.controllers.controller.jwt')
    @patch('ras_backstage.controllers.controller.datetime')
    def test_request_with_expired_jwt_still_returns_successfully(self, mock_datetime, mock_jwt, mock_requests):
        self.app.config.feature = {'validate_jwt': True}
        mock_datetime.now.return_value = 124
        mock_datetime.fromtimestamp = lambda x: x
        mock_jwt.decode.return_value = {'expires_at': 123}

        self.app.config.dependency = {
            'mock-service': {
                'scheme': 'httpx',
                'host': '1.2.3.4',
                'port': '4321'
            }
        }
        response = self.client.get('/backstage-api/v1/mock-service/a', headers={'authorization': 'abc'})
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    import unittest

    unittest.main()
