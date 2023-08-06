from datetime import datetime, timedelta
from fnmatch import fnmatch
import glob
import gzip
from http.client import HTTPMessage
from io import BytesIO
import os
import pickle
import shutil
from unittest import TestCase
from unittest.mock import Mock

from seleniumwire.proxy.storage import RequestStorage


class RequestStorageTest(TestCase):

    def test_initialise(self):
        RequestStorage(base_dir=self.base_dir)
        storage_dir = glob.glob(os.path.join(self.base_dir, '.seleniumwire', 'storage-*'))

        self.assertEqual(len(storage_dir), 1)

    def test_cleanup_removes_storage(self):
        storage = RequestStorage(base_dir=self.base_dir)
        storage.cleanup()

        # The 'seleniumwire' parent folder should have been cleaned up
        # when there is nothing left inside of it.
        self.assertFalse(os.listdir(self.base_dir))

    def test_cleanup_does_not_remove_parent_folder(self):
        # There is an existing storage folder
        os.makedirs(os.path.join(self.base_dir, '.seleniumwire', 'teststorage'))
        storage = RequestStorage(base_dir=self.base_dir)
        storage.cleanup()

        # The existing storage folder is not cleaned up
        self.assertEqual(len(os.listdir(self.base_dir)), 1)
        self.assertTrue(os.path.exists(os.path.join(self.base_dir, '.seleniumwire', 'teststorage')))

    def test_initialise_clears_old_folders(self):
        old_dir = os.path.join(self.base_dir, '.seleniumwire', 'storage-test1')
        new_dir = os.path.join(self.base_dir, '.seleniumwire', 'storage-test2')
        os.makedirs(old_dir)
        os.makedirs(new_dir)
        two_days_ago = (datetime.now() - timedelta(days=2)).timestamp()
        os.utime(old_dir, times=(two_days_ago, two_days_ago))

        RequestStorage(base_dir=self.base_dir)

        self.assertFalse(os.path.exists(old_dir))
        self.assertTrue(os.path.exists(new_dir))

    def test_save_request(self):
        mock_request = self._create_mock_request()

        storage = RequestStorage(base_dir=self.base_dir)
        request_id = storage.save_request(mock_request)

        request_file_path = self._get_stored_path(request_id, 'request')

        with open(request_file_path[0], 'rb') as loaded:
            loaded_request = pickle.load(loaded)

        self.assertEqual(loaded_request['id'], request_id)
        self.assertEqual(loaded_request['path'], 'http://www.example.com/test/path/')
        self.assertEqual(loaded_request['method'], 'GET')
        self.assertEqual(loaded_request['headers'], {
            'Host': 'www.example.com',
            'Accept': '*/*'
        })
        self.assertIsNone(loaded_request['response'])

    def test_save_request_with_body(self):
        mock_request = self._create_mock_request()
        request_body = b'test request body'

        storage = RequestStorage(base_dir=self.base_dir)
        request_id = storage.save_request(mock_request, request_body=request_body)

        request_body_path = self._get_stored_path(request_id, 'requestbody')

        with open(request_body_path[0], 'rb') as loaded:
            loaded_body = pickle.load(loaded)

        self.assertEqual(loaded_body, b'test request body')

    def test_save_response(self):
        mock_request = self._create_mock_request()
        storage = RequestStorage(base_dir=self.base_dir)
        request_id = storage.save_request(mock_request)
        mock_response = self._create_mock_resonse()

        storage.save_response(request_id, mock_response)

        response_file_path = self._get_stored_path(request_id, 'response')

        with open(response_file_path[0], 'rb') as loaded:
            loaded_response = pickle.load(loaded)

        self.assertEqual(loaded_response['status_code'], 200)
        self.assertEqual(loaded_response['reason'], 'OK')
        self.assertEqual(loaded_response['headers'], {
            'Content-Type': 'application/json',
            'Content-Length': '500'
        })

    def test_save_response_with_body(self):
        mock_request = self._create_mock_request()
        storage = RequestStorage(base_dir=self.base_dir)
        request_id = storage.save_request(mock_request)
        mock_response = self._create_mock_resonse()
        response_body = b'some response body'

        storage.save_response(request_id, mock_response, response_body=response_body)

        response_body_path = self._get_stored_path(request_id, 'responsebody')

        with open(response_body_path[0], 'rb') as loaded:
            loaded_body = pickle.load(loaded)

        self.assertEqual(loaded_body, b'some response body')

    def test_save_response_no_request(self):
        mock_request = self._create_mock_request()
        storage = RequestStorage(base_dir=self.base_dir)
        request_id = storage.save_request(mock_request)
        mock_response = self._create_mock_resonse()
        storage.clear_requests()

        storage.save_response(request_id, mock_response)

        response_file_path = self._get_stored_path(request_id, 'response')

        self.assertFalse(response_file_path)

    def test_load_requests(self):
        mock_request_1 = self._create_mock_request()
        mock_request_2 = self._create_mock_request()
        storage = RequestStorage(base_dir=self.base_dir)
        request_id1 = storage.save_request(mock_request_1)
        request_id2 = storage.save_request(mock_request_2)

        requests = storage.load_requests()

        self.assertEqual(len(requests), 2)
        self.assertEqual(requests[0]['id'], request_id1)
        self.assertEqual(requests[1]['id'], request_id2)
        self.assertIsNone(requests[0]['response'])
        self.assertIsNone(requests[1]['response'])

    def test_load_response(self):
        mock_request = self._create_mock_request()
        storage = RequestStorage(base_dir=self.base_dir)
        request_id = storage.save_request(mock_request)
        mock_response = self._create_mock_resonse()
        storage.save_response(request_id, mock_response)

        requests = storage.load_requests()

        self.assertIsNotNone(requests[0]['response'])

    def test_load_request_body(self):
        mock_request = self._create_mock_request()
        storage = RequestStorage(base_dir=self.base_dir)
        request_id = storage.save_request(mock_request, request_body=b'test request body')

        request_body = storage.load_request_body(request_id)

        self.assertEqual(request_body, b'test request body')

    def test_load_response_body(self):
        mock_request = self._create_mock_request()
        storage = RequestStorage(base_dir=self.base_dir)
        request_id = storage.save_request(mock_request, request_body=b'test request body')
        mock_response = self._create_mock_resonse()
        storage.save_response(request_id, mock_response, response_body=b'test response body')

        response_body = storage.load_response_body(request_id)

        self.assertEqual(response_body, b'test response body')

    def test_load_response_body_encoded(self):
        io = BytesIO()
        with gzip.GzipFile(fileobj=io, mode='wb') as f:
            f.write(b'test response body')
        mock_request = self._create_mock_request()
        storage = RequestStorage(base_dir=self.base_dir)
        request_id = storage.save_request(mock_request, request_body=b'test request body')
        mock_response = self._create_mock_resonse()
        mock_response.headers['Content-Encoding'] = 'gzip'
        storage.save_response(request_id, mock_response, response_body=io.getvalue())

        response_body = storage.load_response_body(request_id)

        self.assertEqual(response_body, b'test response body')

    def test_load_last_request(self):
        mock_request_1 = self._create_mock_request()
        mock_request_2 = self._create_mock_request()
        storage = RequestStorage(base_dir=self.base_dir)
        storage.save_request(mock_request_1)
        request_id2 = storage.save_request(mock_request_2)

        last_request = storage.load_last_request()

        self.assertEqual(last_request['id'], request_id2)

    def test_load_last_request_none(self):
        storage = RequestStorage(base_dir=self.base_dir)

        last_request = storage.load_last_request()

        self.assertIsNone(last_request)

    def test_clear_requests(self):
        mock_request_1 = self._create_mock_request()
        mock_request_2 = self._create_mock_request()
        storage = RequestStorage(base_dir=self.base_dir)
        storage.save_request(mock_request_1)
        storage.save_request(mock_request_2)

        storage.clear_requests()
        requests = storage.load_requests()

        self.assertFalse(requests)
        self.assertFalse(glob.glob(os.path.join(self.base_dir, '.seleniumwire', 'storage-*', '*')))

    def test_get_cert_dir(self):
        storage = RequestStorage(base_dir=self.base_dir)

        self.assertTrue(fnmatch(storage.get_cert_dir(),
                                os.path.join(self.base_dir, '.seleniumwire', 'storage-*', 'certs')))

    def test_find(self):
        mock_request_1 = self._create_mock_request('http://www.example.com/test/path/?foo=bar')
        mock_request_2 = self._create_mock_request('http://www.stackoverflow.com/other/path/?x=y')
        mock_response = self._create_mock_resonse()
        storage = RequestStorage(base_dir=self.base_dir)
        request_id = storage.save_request(mock_request_1)
        storage.save_response(request_id, mock_response)
        storage.save_request(mock_request_2)

        self.assertEqual(storage.find('/test/path/')['id'], request_id)
        self.assertEqual(storage.find('/test/path/?foo=bar')['id'], request_id)
        self.assertEqual(storage.find('http://www.example.com/test/path/?foo=bar')['id'], request_id)
        self.assertEqual(storage.find('http://www.example.com/test/path/')['id'], request_id)

        self.assertIsNone(storage.find('/different/path'))
        self.assertIsNone(storage.find('/test/path/?x=y'))
        self.assertIsNone(storage.find('http://www.example.com/different/path/?foo=bar'))
        self.assertIsNone(storage.find('http://www.different.com/test/path/?foo=bar'))
        self.assertIsNone(storage.find('http://www.example.com/test/path/?x=y'))

    def _get_stored_path(self, request_id, filename):
        return glob.glob(os.path.join(self.base_dir, '.seleniumwire', 'storage-*',
                                      'request-{}'.format(request_id), filename))

    def _create_mock_request(self, path='http://www.example.com/test/path/'):
        mock_request = Mock()
        mock_request.path = path
        mock_request.command = 'GET'
        headers = HTTPMessage()
        headers.add_header('Host', 'www.example.com')
        headers.add_header('Accept', '*/*')
        mock_request.headers = headers
        return mock_request

    def _create_mock_resonse(self):
        mock_response = Mock()
        mock_response.status = 200
        mock_response.reason = 'OK'
        headers = HTTPMessage()
        headers.add_header('Content-Type', 'application/json')
        headers.add_header('Content-Length', '500')
        mock_response.headers = headers
        return mock_response

    def setUp(self):
        self.base_dir = os.path.join(os.path.dirname(__file__), 'data')

    def tearDown(self):
        shutil.rmtree(os.path.join(self.base_dir), ignore_errors=True)
