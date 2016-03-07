from selenium import webdriver
import unittest

class NuevoVisitorTest(unittest.TestCase):

    def setUp(self):
        self.navegador = webdriver.Firefox()
        self.navegador.implicitly_wait(3)

    def tearDown(self):
        self.navegador.quit()

    def test_can_start_list_retrieve(self):
        self.navegador.get('http://localhost:8000')

        self.assertIn('To-Do', self.navegador.title)
        self.fail('Test finalizado.')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
