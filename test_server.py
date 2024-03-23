
# COMPLETED BY 
# /////////////////////////////////////////////
# ANURAG DAS
# STUDENT ID 126031228
# EMAIL- adas35@myseneca.ca
# /////////////////////////////////////////////


import http
import unittest
from http.server import HTTPServer
from server import SimpleHTTPRequestHandler
import http.client
import json
import threading




class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_address = ('localhost', 8080)
        cls.server = HTTPServer(cls.server_address, SimpleHTTPRequestHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

    def test_get_method(self):
        # CONNECT SERVER AND SEND GET REQ
        connection = http.client.HTTPConnection(*self.server_address)
        connection.request('GET', '/')
        response = connection.getresponse()

        # READ AND DECODE
        data = response.read().decode()
        connection.close()

        # CHECK IF RESPONS EXPECTED
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'application/json')

        # PARSE JSON DATA AND VERIFY 
        response_data = json.loads(data)
        self.assertEqual(response_data, {'message': 'This is a GET request response'})

    def test_post_method(self):
        # CONNECT SERVER AND SEND POST REQUEST
        connection = http.client.HTTPConnection(*self.server_address)
        headers = {'Content-type': 'application/json'}
        test_data = {'key': 'value'}
        connection.request('POST', '/', body=json.dumps(test_data), headers=headers)
        response = connection.getresponse()

        # READ AND DECODE RESPONSE
        data = response.read().decode()
        connection.close()

        # CHECK RSPONS 
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'application/json')

        # VERIFY CONTENT
        response_data = json.loads(data)
        self.assertEqual(response_data, {'received': test_data})

if __name__ == '__main__':
    unittest.main()