from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NuevoVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.navegador = webdriver.Firefox()
        self.navegador.implicitly_wait(3)

    def tearDown(self):
        self.navegador.quit()

    def check_fila_tabla(self, fila_text):
        # Agrega un nuevo item.
        inputbox = self.navegador.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Pon un item.'
        )
        inputbox.send_keys(fila_text)
        inputbox.send_keys(Keys.ENTER)

        tabla = self.navegador.find_element_by_id('id_list_table')
        filas = tabla.find_elements_by_tag_name('tr')
        self.assertIn(fila_text, [fila.text for fila in filas])

    def test_can_start_list_retrieve(self):
        # Entrar a la pagina principal.
        self.navegador.get(self.live_server_url)

        # El cliente mira el titulo.
        self.assertIn('Lista', self.navegador.title)

        # Consulta la seccion h1.
        header_text = self.navegador.find_element_by_tag_name('h1').text
        self.assertIn('Hacer', header_text)

        # En este momento la pagina se actualiza.
        # Ahora aparece el nuevo item agregado por el usuario.
        # Comprar una pluma de pajaro.

        self.check_fila_tabla('Comprar una pluma de pajaro.')
        self.check_fila_tabla('Usar la pluma de pajaro.')

        self.fail('Test finalizado.')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
