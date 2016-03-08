from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from .views import home_page
from .models import Item, List

class HomePageTest(TestCase):

    def test_url_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_html(self):
        request = HttpRequest()
        response = home_page(request)
        html_esperado = render_to_string('home.html', request=request)
        self.assertEqual(response.content.decode(), html_esperado)

class ListAndItemModelTest(TestCase):

    def test_guardar_retornar_items(self):
        list_ = List()
        list_.save()

        primer_item = Item()
        primer_item.text = 'El primer Item.'
        primer_item.list = list_
        primer_item.save()

        segundo_item = Item()
        segundo_item.text = 'El segundo Item.'
        segundo_item.list = list_
        segundo_item.save()

        items_guardados = Item.objects.all()
        self.assertEqual(items_guardados.count(), 2)

        primer_item_guardado = items_guardados[0]
        segundo_item_guardado = items_guardados[1]
        self.assertEqual(primer_item_guardado.text, 'El primer Item.')
        self.assertEqual(primer_item_guardado.list, list_)
        self.assertEqual(segundo_item_guardado.text, 'El segundo Item.')
        self.assertEqual(segundo_item_guardado.list, list_)

class ListViewTest(TestCase):

    def test_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')

    def test_display_solo_items_segun_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='item 1', list=correct_list)
        Item.objects.create(text='item 2', list=correct_list)

        otra_list = List.objects.create()
        Item.objects.create(text='otro item 1', list=otra_list)
        Item.objects.create(text='otro item 2', list=otra_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'otro item 1')
        self.assertNotContains(response, 'otro item 2')

class NewLiveTest(TestCase):

    def test_guardar_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': 'Un nuevo item'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Un nuevo item')

    def test_redirect_desp_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'Un nuevo item'}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id))
