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

# URL inicial de la primera página de Trustpilot para la categoría de viajes y vacaciones en Perú
base_url = "https://es.trustpilot.com/categories/travel_vacation?country=PE"

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

# Función para extraer enlaces de reseñas de una página específica
def extract_review_urls(page_url):
    response = make_request_with_retries(page_url)
    if not response:
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    review_urls = []
    review_links = soup.find_all('a', class_='link_internal__7XN06')

    for link in review_links:
        href = link.get('href')  # Verificamos si 'href' existe
        if href and "/review/" in href:  # Asegurarse de que es un enlace a una reseña
            review_url = 'https://es.trustpilot.com' + href
            review_urls.append(review_url)

    return review_urls

# Función para recorrer un número dado de páginas y extraer todos los enlaces de reseñas
def extract_pages(start_url, num_pages):
    all_review_urls = []
    current_url = start_url
    page_counter = 0

    while current_url and page_counter < num_pages:
        print(f"Extrayendo enlaces de la página {page_counter + 1}: {current_url}")
        response = make_request_with_retries(current_url)
        if not response:
            break
        
        soup = BeautifulSoup(response.content, 'html.parser')
        review_urls = extract_review_urls(current_url)
        all_review_urls.extend(review_urls)
        
        current_url = get_next_page_url(soup)
        page_counter += 1

    return all_review_urls

# Función para encontrar el enlace a la página siguiente
def get_next_page_url(soup):
    next_page = soup.find('a', class_='pagination-link_next__SDNU4')
    if next_page:
        return 'https://es.trustpilot.com' + next_page['href']
    return None

# Función principal para extraer enlaces y guardarlos en un archivo JSON
def main():
    # Vaciar el contenido previo del archivo JSON antes de agregar nuevos datos
    with open('trustpilot_review_links.json', 'w') as json_file:
        json.dump([], json_file)  # Sobrescribir con una lista vacía
    
    all_review_urls = []

    # Extraer enlaces de las primeras 12 páginas
    all_review_urls.extend(extract_pages(base_url, 11))

    # Guardar los enlaces en un archivo JSON
    with open('trustpilot_review_links.json', 'w') as json_file:
        json.dump(all_review_urls, json_file, indent=4)
        print(f"Datos extraídos y guardados en 'trustpilot_review_links.json'.")

if __name__ == "__main__":
    main()
