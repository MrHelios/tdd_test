from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from .views import home_page
from .models import Item

class HomePageTest(TestCase):

    def test_url_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_html(self):
        request = HttpRequest()
        response = home_page(request)
        html_esperado = render_to_string('home.html', request=request)
        self.assertEqual(response.content.decode(), html_esperado)

    def test_home_page_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'Un nuevo item'

        response = home_page(request)

        self.assertIn('Un nuevo item', response.content.decode())
        html_esperado = render_to_string(
                'home.html',
                {'new_item_text': 'Un nuevo item'}, request=request)
        self.assertEqual(response.content.decode(), html_esperado)

class ItemModelTest(TestCase):

    def test_guardar_retornar_items(self):
        primer_item = Item()
        primer_item.text = 'El primer Item.'
        primer_item.save()

        segundo_item = Item()
        segundo_item.text = 'El segundo Item.'
        segundo_item.save()

        items_guardados = Item.objects.all()
        self.assertEqual(items_guardados.count(), 2)

        primer_item_guardado = items_guardados[0]
        segundo_item_guardado = items_guardados[1]
        self.assertEqual(primer_item_guardado.text, 'El primer Item.')
        self.assertEqual(segundo_item_guardado.text, 'El segundo Item.')
