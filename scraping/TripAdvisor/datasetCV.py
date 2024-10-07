import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import json
import os  # Para verificar si el archivo existe y eliminarlo
import concurrent.futures
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Lista de User-Agents para rotación
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
]

# Establecer tiempo de espera y backoff para los reintentos
REQUEST_TIMEOUT = 10  # 10 segundos de timeout
MAX_RETRIES = 5  # Número máximo de reintentos

# Crear una sesión para las solicitudes con reintentos automáticos
def create_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=MAX_RETRIES,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504, 403],  # Incluir 403 en la lista de reintentos
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# Función para obtener un header aleatorio
def get_random_headers():
    return {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': 'en-US, en;q=0.9,es;q=0.8'
    }

# Función para realizar una solicitud con reintentos automáticos y rotación de User-Agent
def make_request_with_retries(url, session, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            headers = get_random_headers()  # Rotar User-Agent
            response = session.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()  # Verificar si hubo errores HTTP
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error al hacer la solicitud a {url}: {e}")
            retries += 1
            print(f"Reintentando... ({retries}/{max_retries})")
            time.sleep(10)  # Pausa antes de reintentar
    print(f"Fallo tras {max_retries} reintentos en {url}")
    return None  # Devolver None si se agotan los reintentos

# Función para extraer datos de reseñas de un tour específico
def extract_tour_data(tour_url, session):
    print(f"Accediendo a la URL: {tour_url}")
    response = make_request_with_retries(tour_url, session)
    if not response:
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        tour_title = soup.find('h1', class_='biGQs _P fiohW ncFvv EVnyE').text.strip()
    except AttributeError:
        tour_title = 'No disponible'
    
    # Extraer solo los números del campo de opiniones
    try:
        opinion_count = soup.find('span', class_='biGQs _P pZUbB KxBGd').find('span').text.strip()
        opinion_count = ''.join(filter(str.isdigit, opinion_count))  # Solo dejar los dígitos
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
def extract_tour_reviews_parallel(tour_urls, max_workers=5):
    reviews_data = []
    session = create_session()

    # Contadores para estadísticas
    total_links = len(tour_urls)
    successful_links = 0
    failed_links = 0

    # Función interna para procesar cada URL
    def process_url(url):
        nonlocal successful_links, failed_links
        data = extract_tour_data(url, session)
        if data:
            successful_links += 1
            return data
        else:
            failed_links += 1
            return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(process_url, url): url for url in tour_urls}
        for future in concurrent.futures.as_completed(future_to_url):
            result = future.result()
            if result:
                reviews_data.append(result)

    session.close()

    # Mostrar estadísticas al final
    print(f"\nEstadísticas de procesamiento:")
    print(f"Total de enlaces: {total_links}")
    print(f"Enlaces procesados exitosamente: {successful_links}")
    print(f"Enlaces fallidos: {failed_links}")

    return reviews_data

# Función para guardar los datos incrementalmente en un archivo CSV (sin sobrescribir)
def save_to_csv_incremental(reviews_data, first_chunk=False, filename='tour_reviews_partial.csv'):
    # Solo eliminar el archivo si es el primer chunk y el archivo ya existe
    if first_chunk and os.path.exists(filename):
        os.remove(filename)  # Eliminar archivo si ya existe antes de empezar

    # Guardar los datos en el archivo (escribir o agregar)
    if not os.path.exists(filename) or first_chunk:
        pd.DataFrame(reviews_data).to_csv(filename, index=False, mode='w', header=True)
    else:
        pd.DataFrame(reviews_data).to_csv(filename, index=False, mode='a', header=False)

# Función para eliminar datos faltantes
def remove_missing_data(file_name='tour_reviews_partial.csv'):
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
    df['Rating'] = df['Rating'].apply(lambda x: x.split()[0] if isinstance(x, str) else x)
    df.to_csv("Dataset_after_all.csv", index=False)
    print("Columna 'Rating' normalizada y guardada como 'Dataset_after_all.csv'.")

# Función para normalizar la columna 'Opinion Count'
def normalize_review_count_column(file_name='Dataset_after_all.csv'):
    df = pd.read_csv(file_name)
    df['Opinion Count'] = df['Opinion Count'].apply(lambda x: str(x).split()[0] if pd.notna(x) else x)
    df.to_csv(file_name, index=False)
    print("Columna 'Opinion Count' normalizada.")

# Función para dividir la lista en lotes de tamaño especificado
def chunk_list(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

# Función principal
def main():
    start_time = time.time()

    # Cargar los enlaces desde el archivo JSON
    with open('tour_links.json', 'r') as json_file:
        tour_urls = json.load(json_file)

    total_urls = len(tour_urls)
    print(f"Total de enlaces cargados desde JSON: {total_urls}")

    # Dividir los enlaces en lotes de 50
    batch_size = 50
    batches = list(chunk_list(tour_urls, batch_size))
    num_batches = len(batches)

    for i, batch in enumerate(batches):
        print(f"Procesando lote {i + 1} de {num_batches}...")

        # El parámetro first_chunk será True solo para el primer lote
        first_chunk = (i == 0)

        # Extraer las reseñas del lote actual usando paralelismo
        reviews_data = extract_tour_reviews_parallel(batch, max_workers=10)

        # Guardar datos, pasando el indicador si es el primer chunk o no
        save_to_csv_incremental(reviews_data, first_chunk)

        # Pausar solo si no es el último lote
        if i < num_batches - 1:
            wait_time = 120  # Pausa de 2 minutos (120 segundos)
            print(f"Esperando {wait_time // 60} minutos antes de procesar el siguiente lote...")
            time.sleep(wait_time)

    # Eliminar datos faltantes
    remove_missing_data()

    # Eliminar duplicados
    remove_duplicates()

    # Normalizar las columnas 'Rating' y 'Opinion Count'
    normalize_rating_column()
    normalize_review_count_column()

    # Medir y mostrar el tiempo de ejecución total
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Tiempo total de ejecución: {execution_time:.2f} segundos")

if __name__ == "__main__":
    main()
