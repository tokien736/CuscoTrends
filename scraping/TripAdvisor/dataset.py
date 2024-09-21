import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import concurrent.futures
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Encabezados para evitar ser bloqueados por el sitio
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.9,es;q=0.8'
}

# URL inicial de la primera página de TripAdvisor para tours
base_url = "https://www.tripadvisor.com.pe/Attractions-g294314-Activities-c42-Cusco_Cusco_Region.html"

# Establecer tiempo de espera y backoff para los reintentos
REQUEST_TIMEOUT = 10  # 10 segundos de timeout
MAX_RETRIES = 5  # Número máximo de reintentos

# Crear una sesión para las solicitudes con reintentos automáticos
session = requests.Session()
retry_strategy = Retry(
    total=MAX_RETRIES,
    backoff_factor=1,  # Incrementar el tiempo de espera después de cada fallo
    status_forcelist=[429, 500, 502, 503, 504],  # Códigos de error que deben gatillar un reintento
    allowed_methods=["HEAD", "GET", "OPTIONS"]  # Cambiado de method_whitelist a allowed_methods
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

# Función para realizar una solicitud con reintentos automáticos
def make_request_with_retries(url):
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

# Función para encontrar el enlace a la página siguiente
def get_next_page_url(soup):
    next_page = soup.find('a', {'data-smoke-attr': 'pagination-next-arrow'})
    if next_page:
        return 'https://www.tripadvisor.com.pe' + next_page['href']
    return None

# Función para recorrer hasta 6 páginas y extraer todos los enlaces de tours
def extract_six_pages(start_url):
    all_tour_urls = []
    current_url = start_url
    page_counter = 0

    while current_url and page_counter < 6:
        print(f"Extrayendo enlaces de la página {page_counter + 1}: {current_url}")
        response = make_request_with_retries(current_url)
        if not response:
            break  # Detenemos el proceso si no obtenemos respuesta
        
        soup = BeautifulSoup(response.content, 'html.parser')
        tour_urls = extract_tour_urls(current_url)
        all_tour_urls.extend(tour_urls)
        
        current_url = get_next_page_url(soup)
        page_counter += 1

    return all_tour_urls

# Función para extraer datos de reseñas de un tour específico
def extract_tour_data(tour_url):
    print(f"Accediendo a la URL: {tour_url}")
    response = make_request_with_retries(tour_url)

    if not response:
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        tour_title = soup.find('h1', class_='biGQs _P fiohW ncFvv EVnyE').text.strip()
    except AttributeError:
        tour_title = 'No disponible'

    try:
        opinion_count = soup.find('span', class_='biGQs _P pZUbB KxBGd').find('span').text.strip().replace("\xa0opiniones", "")
    except AttributeError:
        opinion_count = 'No disponible'

    try:
        image_count = soup.find('button', class_='rmyCe _G B- z _S c Wc wSSLS jWkoZ sOtnj').text.strip()
    except AttributeError:
        image_count = 'No disponible'

    try:
        rating = soup.find('div', class_='biGQs _P fiohW hzzSG uuBRH').text.strip()
    except AttributeError:
        rating = 'No disponible'

    review_distribution = {'Excelente': '0', 'Muy bueno': '0', 'Promedio': '0', 'Mala': '0', 'Horrible': '0'}
    review_types = soup.find_all('div', class_='RZjkd')

    for review_type in review_types:
        try:
            comment_type = review_type.find('div', class_='yFXuQ o W q').text.strip()
            comment_count = review_type.find('div', class_='biGQs _P fiohW biKBZ osNWb').text.strip()
            if comment_type in review_distribution:
                review_distribution[comment_type] = comment_count
        except AttributeError:
            continue

    return {
        'Tour Title': tour_title,
        'Tour URL': tour_url,
        'Opinion Count': opinion_count,
        'Image Count': image_count,
        'Rating': rating,
        'Excelente': review_distribution['Excelente'],
        'Muy bueno': review_distribution['Muy bueno'],
        'Promedio': review_distribution['Promedio'],
        'Mala': review_distribution['Mala'],
        'Horrible': review_distribution['Horrible']
    }

# Función para extraer datos de reseñas de los enlaces de tours en paralelo
def extract_tour_reviews(tour_urls):
    reviews_data = []
    
    # Usamos el módulo concurrent.futures para paralelizar las solicitudes
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(extract_tour_data, url) for url in tour_urls]
        for future in concurrent.futures.as_completed(futures):
            data = future.result()
            if data:
                reviews_data.append(data)
    
    return reviews_data

# Función para guardar los datos en un archivo CSV
def save_to_csv(reviews_data, filename='tour_reviews.csv'):
    df = pd.DataFrame(reviews_data)
    if not df.empty:
        df.to_csv(filename, index=False)
        print(f"Datos extraídos y guardados en '{filename}'.")
    else:
        print("No se extrajeron datos.")

# Función para eliminar datos faltantes
def remove_missing_data(file_name='tour_reviews.csv'):
    df = pd.read_csv(file_name)
    without_missing_dataset = df.dropna()
    without_missing_dataset.to_csv("Without_Missing_Dataset.csv", index=False)
    print("Dataset sin datos faltantes guardado como 'Without_Missing_Dataset.csv'.")
    return without_missing_dataset

# Función para eliminar duplicados
def remove_duplicates(file_name='Without_Missing_Dataset.csv'):
    df = pd.read_csv(file_name)
    without_duplicates_dataset = df.drop_duplicates()
    without_duplicates_dataset.to_csv("Without_Duplicates_Dataset.csv", index=False)
    print("Dataset sin duplicados guardado como 'Without_Duplicates_Dataset.csv'.")
    return without_duplicates_dataset

# Función para normalizar la columna 'Rating'
def normalize_rating_column(file_name='Without_Duplicates_Dataset.csv'):
    df = pd.read_csv(file_name)
    df['Rating'] = df['Rating'].apply(lambda x: x.split()[0] if pd.notna(x) else x)
    df.to_csv("Dataset_after_all.csv", index=False)
    print("Columna 'Rating' normalizada y guardada como 'Dataset_after_all.csv'.")

# Función para normalizar la columna 'Review Count'
def normalize_review_count_column(file_name='Dataset_after_all.csv'):
    df = pd.read_csv(file_name)
    df['Opinion Count'] = df['Opinion Count'].apply(lambda x: x.split()[0] if pd.notna(x) else x)
    df.to_csv(file_name, index=False)
    print("Columna 'Opinion Count' normalizada.")

# Función principal
def main():
    start_time = time.time()
    
    # Extraer enlaces de las primeras 6 páginas
    all_tour_urls = extract_six_pages(base_url)
    print(f"Total de enlaces extraídos: {len(all_tour_urls)}")

    # Extraer las reseñas de los tours extraídos
    reviews_data = extract_tour_reviews(all_tour_urls)

    # Guardar las reseñas en un archivo CSV
    save_to_csv(reviews_data)

    # Eliminar datos faltantes
    remove_missing_data()

    # Eliminar duplicados
    remove_duplicates()

    # Normalizar las columnas
    normalize_rating_column()
    normalize_review_count_column()

    # Medir y mostrar el tiempo de ejecución
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Tiempo total de ejecución: {execution_time:.2f} segundos")

if __name__ == "__main__":
    main()
