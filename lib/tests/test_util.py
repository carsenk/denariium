import unittest
from lib.util import format_satoshis, parse_URI

class TestUtil(unittest.TestCase):

    def test_format_satoshis(self):
        result = format_satoshis(1234)
        expected = "0.00001234"
        self.assertEqual(expected, result)

    def test_format_satoshis_diff_positive(self):
        result = format_satoshis(1234, is_diff=True)
        expected = "+0.00001234"
        self.assertEqual(expected, result)

    def test_format_satoshis_diff_negative(self):
        result = format_satoshis(-1234, is_diff=True)
        expected = "-0.00001234"
        self.assertEqual(expected, result)

    def _do_test_parse_URI(self, uri, expected):
        result = parse_URI(uri)
        self.assertEqual(expected, result)

    def test_parse_URI_address(self):
        self._do_test_parse_URI('denarius:15mKKb2eos1hWa6tisdPwwDC1a5J1y9nma',
                                {'address': '15mKKb2eos1hWa6tisdPwwDC1a5J1y9nma'})

    def test_parse_URI_only_address(self):
        self._do_test_parse_URI('15mKKb2eos1hWa6tisdPwwDC1a5J1y9nma',
                                {'address': '15mKKb2eos1hWa6tisdPwwDC1a5J1y9nma'})


    def test_parse_URI_address_label(self):
        self._do_test_parse_URI('denarius:15mKKb2eos1hWa6tisdPwwDC1a5J1y9nma?label=denariium%20test',
                                {'address': '15mKKb2eos1hWa6tisdPwwDC1a5J1y9nma', 'label': 'denariium test'})

    def test_parse_URI_address_message(self):
        self._do_test_parse_URI('denarius:15mKKb2eos1hWa6tisdPwwDC1a5J1y9nma?message=denariium%20test',
                                {'address': '15mKKb2eos1hWa6tisdPwwDC1a5J1y9nma', 'message': 'denariium test', 'memo': 'denariium test'})

    def test_parse_URI_address_amount(self):
        self._do_test_parse_URI('denarius:15mKKb2eos1hWa6tisdPwwDC1a5J1y9nma?amount=0.0003',
                                {'address': '15mKKb2eos1hWa6tisdPwwDC1a5J1y9nma', 'amount': 30000})

    def test_parse_URI_address_request_url(self):
        self._do_test_parse_URI('denarius:15mKKb2eos1hWa6tisdPwwDC1a5J1y9nma?r=http://domain.tld/page?h%3D2a8628fc2fbe',
                                {'address': '15mKKb2eos1hWa6tisdPwwDC1a5J1y9nma', 'r': 'http://domain.tld/page?h=2a8628fc2fbe'})

    def test_parse_URI_ignore_args(self):
        self._do_test_parse_URI('denarius:15mKKb2eos1hWa6tisdPwwDC1a5J1y9nma?test=test',
                                {'address': '15mKKb2eos1hWa6tisdPwwDC1a5J1y9nma', 'test': 'test'})

    def test_parse_URI_multiple_args(self):
        self._do_test_parse_URI('denarius:15mKKb2eos1hWa6tisdPwwDC1a5J1y9nma?amount=0.00004&label=denariium-test&message=denariium%20test&test=none&r=http://domain.tld/page',
                                {'address': '15mKKb2eos1hWa6tisdPwwDC1a5J1y9nma', 'amount': 4000, 'label': 'denariium-test', 'message': u'denariium test', 'memo': u'denariium test', 'r': 'http://domain.tld/page', 'test': 'none'})

    def test_parse_URI_no_address_request_url(self):
        self._do_test_parse_URI('denarius:?r=http://domain.tld/page?h%3D2a8628fc2fbe',
                                {'r': 'http://domain.tld/page?h=2a8628fc2fbe'})

    def test_parse_URI_invalid_address(self):
        self.assertRaises(BaseException, parse_URI, 'denarius:invalidaddress')

    def test_parse_URI_invalid(self):
        self.assertRaises(BaseException, parse_URI, 'notdenarius:15mKKb2eos1hWa6tisdPwwDC1a5J1y9nma')

    def test_parse_URI_parameter_polution(self):
        self.assertRaises(Exception, parse_URI, 'denarius:15mKKb2eos1hWa6tisdPwwDC1a5J1y9nma?amount=0.0003&label=test&amount=30.0')

