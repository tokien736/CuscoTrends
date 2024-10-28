import requests
from bs4 import BeautifulSoup
import json
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Lista de User-Agents para rotación
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
]

# URL inicial de la primera página de TripAdvisor para tours
base_url = "https://www.tripadvisor.com.pe/Attractions-g294314-Activities-c42-Cusco_Cusco_Region.html"

# Establecer tiempo de espera y backoff para los reintentos
REQUEST_TIMEOUT = 10  # 10 segundos de timeout
MAX_RETRIES = 5  # Número máximo de reintentos

# Crear una sesión para las solicitudes con reintentos automáticos
session = requests.Session()
retry_strategy = Retry(
    total=MAX_RETRIES,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504, 403],
    allowed_methods=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

# Función para realizar una solicitud con reintentos automáticos y rotación de User-Agent
def make_request_with_retries(url):
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': 'en-US, en;q=0.9,es;q=0.8'
    }
    try:
        response = session.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()  # Verificar si hubo errores HTTP
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud a {url}: {e}")
        return None

# Función para extraer enlaces de tours de una página específica
def extract_tour_urls(page_url):
    response = make_request_with_retries(page_url)
    if not response:
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    tour_urls = []
    tour_links = soup.find_all('a', class_='BUupS _R w _Z y M0 B0 Gm wSSLS')

    for tour in tour_links:
        tour_url = 'https://www.tripadvisor.com.pe' + tour['href']
        tour_urls.append(tour_url)

    return tour_urls

# Función para recorrer un número dado de páginas y extraer todos los enlaces de tours
def extract_pages(start_url, num_pages):
    all_tour_urls = []
    current_url = start_url
    page_counter = 0

    while current_url and page_counter < num_pages:
        print(f"Extrayendo enlaces de la página {page_counter + 1}: {current_url}")
        response = make_request_with_retries(current_url)
        if not response:
            break
        
        soup = BeautifulSoup(response.content, 'html.parser')
        tour_urls = extract_tour_urls(current_url)
        all_tour_urls.extend(tour_urls)
        
        current_url = get_next_page_url(soup)
        page_counter += 1

    return all_tour_urls

# Función para encontrar el enlace a la página siguiente
def get_next_page_url(soup):
    next_page = soup.find('a', {'data-smoke-attr': 'pagination-next-arrow'})
    if next_page:
        return 'https://www.tripadvisor.com.pe' + next_page['href']
    return None

# Función principal para extraer enlaces y guardarlos en un archivo JSON
def main():
    # Vaciar el contenido del archivo JSON antes de empezar
    with open('tour_links.json', 'w') as json_file:
        json.dump([], json_file)
        print("Archivo 'tour_links.json' vaciado.")

    all_tour_urls = []

    # Extraer enlaces de las primeras 6 páginas
    all_tour_urls.extend(extract_pages(base_url, 6))

    # Pausa antes de extraer enlaces de la página 14 a la 21
    print("Esperando 1.30 minutos antes de extraer enlaces de la página 14 a la 21...")
    time.sleep(90)

    # Extraer enlaces de la página 14 a la 21
    page_14_url = "https://www.tripadvisor.com.pe/Attractions-g294314-Activities-oa120-c42-Cusco_Cusco_Region.html"
    all_tour_urls.extend(extract_pages(page_14_url, 8))

    # Pausa antes de extraer enlaces de la página 50 a la 56
    print("Esperando 1.30 minutos antes de extraer enlaces de la página 50 a la 56...")
    time.sleep(90)

    # Extraer enlaces de la página 50 a la 56
    page_50_url = "https://www.tripadvisor.com.pe/Attractions-g294314-Activities-oa480-c42-Cusco_Cusco_Region.html"
    all_tour_urls.extend(extract_pages(page_50_url, 7))

    # Guardar los enlaces en un archivo JSON
    with open('tour_links.json', 'w') as json_file:
        json.dump(all_tour_urls, json_file, indent=4)
        print(f"Datos extraídos y guardados en 'tour_links.json'.")

if __name__ == "__main__":
    main()