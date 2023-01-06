import unittest
import requests_mock
from main import Crawler


class TestAPI(unittest.TestCase):
    @requests_mock.mock()
    def test_get_linked_urls_from_entrypoint_url(self, m):
        url = 'https://example.com'
        m.get('https://example.com', text='<html> <a href="https://example.com/exam">example</a> </html>')
        m.get('https://example.com/exam', text='')
        expected_urls = ['https://example.com/exam']
        with self.assertLogs() as captured:
            Crawler(url).run()
        assert captured.records[0].msg == f"Current page: {url}\n     The connected url in page: {expected_urls}"

    @requests_mock.mock()
    def test_get_linked_special_type_urls_from_entrypoint_url(self, m):
        url = 'https://example.com'
        m.get('https://example.com', text='<html> <a href="/exam">example</a> </html>')
        m.get('https://example.com/exam', text='')
        expected_urls = ['https://example.com/exam']
        with self.assertLogs() as captured:
            Crawler(url).run()
        assert captured.records[0].msg == f"Current page: {url}\n     The connected url in page: {expected_urls}"
