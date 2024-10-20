import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import json
import concurrent.futures
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import ast

# Función para obtener un header aleatorio
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/91.0.4472.114 Safari/537.36'
]

# Crear una sesión para las solicitudes con reintentos automáticos
def create_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504, 403],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# Función para realizar una solicitud con reintentos automáticos y rotación de User-Agent
def make_request_with_retries(url, session):
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': 'en-US, en;q=0.9,es;q=0.8'
    }
    try:
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud a {url}: {e}")
        return None

# Función para extraer datos de reseñas de un tour específico
def extract_tour_data(tour_url, session):
    response = make_request_with_retries(tour_url, session)
    if not response:
        return None
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        business_title = soup.find('span', class_='typography_display-s__qOjh6').text.strip()
    except AttributeError:
        business_title = 'No disponible'

    try:
        opinion_count = soup.find('span', class_='typography_body-l__KUYFJ').text.strip().split('•')[0].strip()
    except AttributeError:
        opinion_count = 'No disponible'

    try:
        total_opinions = int(soup.find('p', {'data-reviews-count-typography': 'true'}).text.strip().split(' ')[0])
    except (AttributeError, ValueError):
        total_opinions = 0

    try:
        rating = soup.find('span', class_='typography_heading-m__T_L_X').text.strip()
    except AttributeError:
        rating = 'No disponible'

    review_distribution = {'5 estrellas': '0%', '4 estrellas': '0%', '3 estrellas': '0%', '2 estrellas': '0%', '1 estrella': '0%'}
    star_ratings = soup.find_all('label', class_='styles_row__wvn4i')

    for rating_row in star_ratings:
        try:
            star_type = rating_row.find('p', class_='typography_body-m__xgxZ_').text.strip()
            percentage = rating_row.find('p', class_='styles_percentageCell__cHAnb').text.strip()
            if star_type in review_distribution:
                review_distribution[star_type] = percentage
        except AttributeError:
            continue

    # Filtrar si algún campo clave contiene "No disponible"
    if business_title == 'No disponible' or total_opinions == 0 or rating == 'No disponible':
        print(f"Datos incompletos para {tour_url}, omitiendo este registro.")
        return None

    return {
        'Business Title': business_title,
        'Tour URL': tour_url,
        'Opinion Count': opinion_count,
        'Total Opinions': total_opinions,
        'Rating': rating,
        'Review Distribution': review_distribution
    }

# Función para guardar los datos en un archivo CSV (acumulando los datos)
def save_to_csv(reviews_data, filename='final_tour_reviewcsvs.'):
    df = pd.DataFrame(reviews_data)
    if not df.empty:
        if os.path.exists(filename):
            df.to_csv(filename, mode='a', header=False, index=False)  # Si ya existe, agregar los nuevos datos
        else:
            df.to_csv(filename, mode='w', header=True, index=False)  # Si no existe, crear el archivo
        print(f"Datos extraídos y guardados en '{filename}'.")
    else:
        print("No se extrajeron datos.")

# Proceso de limpieza y normalización en un solo paso
def clean_and_normalize(file_name='final_tour_reviews.csv'):
    # Cargar el archivo
    df = pd.read_csv(file_name)

    # Eliminar filas con datos faltantes
    df = df.dropna()

    # Eliminar duplicados
    df = df.drop_duplicates()

    # Normalizar la columna 'Rating'
    df['Rating'] = df['Rating'].apply(lambda x: x.split()[0] if isinstance(x, str) else x)

    # Normalizar la columna 'Opinion Count'
    df['Opinion Count'] = df['Opinion Count'].apply(lambda x: x.split()[0] if pd.notna(x) else x)

    # Aplicar la purga a la columna 'Review Distribution'
    df[['5_estrellas', '4_estrellas', '3_estrellas', '2_estrellas', '1_estrella']] = df['Review Distribution'].apply(purgar_review_distribution)

    # Convertir los porcentajes en números absolutos en función de 'Total Opinions'
    df['Total Opinions'] = df['Total Opinions'].astype(int)  # Asegurarnos de que 'Total Opinions' es entero
    df['5_estrellas'] = (df['5_estrellas'] * df['Total Opinions']).round().astype(int)
    df['4_estrellas'] = (df['4_estrellas'] * df['Total Opinions']).round().astype(int)
    df['3_estrellas'] = (df['3_estrellas'] * df['Total Opinions']).round().astype(int)
    df['2_estrellas'] = (df['2_estrellas'] * df['Total Opinions']).round().astype(int)
    df['1_estrella'] = (df['1_estrella'] * df['Total Opinions']).round().astype(int)

    # Eliminar la columna "Review Distribution"
    df.drop(columns=['Review Distribution'], inplace=True)

    # Guardar el dataset final en el mismo archivo
    df.to_csv(file_name, index=False)
    print(f"El dataset ha sido limpiado, normalizado, y guardado como '{file_name}'.")

# Función para purgar el campo "Review Distribution" y convertirlo en variables separadas
def purgar_review_distribution(review_dist):
    # Quitar caracteres no deseados como '\xa0' y cualquier espacio extra
    review_dist = review_dist.replace('\xa0', '').replace('"', '').strip()

    # Convertir el string a un diccionario
    review_dict = ast.literal_eval(review_dist)

    # Función para convertir porcentajes a valores decimales
    def convertir_a_float(porcentaje):
        # Si el valor es '<1%' lo convertimos a 0.01
        if '<' in porcentaje:
            return 0.01
        # De lo contrario, eliminamos el símbolo '%' y convertimos a float
        return float(porcentaje.replace('%', '')) / 100

    # Crear nuevas columnas basadas en el diccionario
    estrellas_5 = convertir_a_float(review_dict['5 estrellas'])
    estrellas_4 = convertir_a_float(review_dict['4 estrellas'])
    estrellas_3 = convertir_a_float(review_dict['3 estrellas'])
    estrellas_2 = convertir_a_float(review_dict['2 estrellas'])
    estrellas_1 = convertir_a_float(review_dict['1 estrella'])

    return pd.Series([estrellas_5, estrellas_4, estrellas_3, estrellas_2, estrellas_1])

# Función para dividir la lista en lotes de tamaño especificado
def chunk_list(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

# Función para extraer los datos de las reseñas en paralelo
def extract_tour_reviews(tour_urls):
    reviews_data = []
    session = create_session()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(extract_tour_data, url, session) for url in tour_urls]
        for future in concurrent.futures.as_completed(futures):
            data = future.result()
            if data:
                reviews_data.append(data)

    session.close()
    return reviews_data

# Función principal
def main():
    # Cargar los enlaces desde el archivo JSON
    with open('trustpilot_review_links.json', 'r') as json_file:
        tour_urls = json.load(json_file)

    # Dividir los enlaces en lotes de 50
    batch_size = 50
    batches = list(chunk_list(tour_urls, batch_size))

    # Procesar los lotes
    for i, batch in enumerate(batches):
        print(f"Procesando lote {i + 1} de {len(batches)}...")
        reviews_data = extract_tour_reviews(batch)

        # Guardar los datos en un solo archivo CSV
        save_to_csv(reviews_data, 'final_tour_reviews.csv')

        # Esperar antes del siguiente lote
        if i < len(batches) - 1:
            print("Esperando 4 minutos antes de procesar el siguiente lote...")
            time.sleep(240)

    # Proceso de limpieza y normalización final
    clean_and_normalize('final_tour_reviews.csv')

if __name__ == "__main__":
    main()
