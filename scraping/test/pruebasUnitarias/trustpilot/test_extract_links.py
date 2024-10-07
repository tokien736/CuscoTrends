import unittest
import sys
import os

# Agregar la ruta exacta del archivo extract_links.py
sys.path.insert(0, r"D:\Taller de investigacion\scraping\CuscoTrends\scraping\Trustpilot")
from extract_links import extract_pages, base_url  # Importar funciones desde el archivo correspondiente

class TestExtractLinks(unittest.TestCase):
    def test_extract_pages(self):
        # Probamos la extracción de una sola página para verificar si se obtienen enlaces
        resultado = extract_pages(base_url, 1)
        self.assertGreater(len(resultado), 0, "No se extrajeron enlaces de la primera página")

    def test_cp02_verificar_extraccion_datos(self):
        # Probamos la extracción de múltiples páginas para verificar la cobertura completa
        num_paginas = 5  # Número de páginas a extraer
        resultado = extract_pages(base_url, num_paginas)
        self.assertGreater(len(resultado), 0, "No se extrajeron datos de Trustpilot")
        # Verificar si el número de datos extraídos corresponde al número de páginas esperadas
        self.assertTrue(len(resultado) >= num_paginas * 10, "No se extrajeron todos los datos esperados de Trustpilot")

if __name__ == '__main__':
    unittest.main()