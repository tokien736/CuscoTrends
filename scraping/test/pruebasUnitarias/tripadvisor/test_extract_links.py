import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Ajustar sys.path para apuntar al directorio principal
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../..'))
sys.path.insert(0, project_root)

from TripAdvisor.tour_scraper import extract_tour_urls

class TestExtractLinks(unittest.TestCase):
    """
    CP01: Verificar extracción de datos de TripAdvisor
    Descripción: Verificar que el módulo de scraping pueda extraer correctamente los enlaces de tours de la página de TripAdvisor.
    URL de prueba: URL de TripAdvisor
    Resultado esperado: Extraiga los enlaces de las páginas.
    Criterio de éxito: 100% de los datos esperados extraídos sin errores.
    """

    @patch('TripAdvisor.tour_scraper.make_request_with_retries')
    def test_extract_tour_urls(self, mock_request):
        # Simulación de la respuesta de la página de un listado de tours de TripAdvisor
        mock_response = MagicMock()
        mock_response.content = '''
        <html>
        <body>
            <a class="BUupS _R w _Z y M0 B0 Gm wSSLS" href="/Attraction_Review-t1.html">Tour 1</a>
            <a class="BUupS _R w _Z y M0 B0 Gm wSSLS" href="/Attraction_Review-t2.html">Tour 2</a>
        </body>
        </html>
        '''
        mock_request.return_value = mock_response

        expected_urls = [
            'https://www.tripadvisor.com.pe/Attraction_Review-t1.html',
            'https://www.tripadvisor.com.pe/Attraction_Review-t2.html'
        ]

        result = extract_tour_urls("https://www.tripadvisor.com.pe/Attractions-g294314-Activities-Cusco.html")
        self.assertEqual(result, expected_urls)

if __name__ == '__main__':
    unittest.main()