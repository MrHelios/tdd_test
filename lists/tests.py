from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from .views import home_page

class HomePageTest(TestCase):

    def test_url_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_html(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>Lista</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))
