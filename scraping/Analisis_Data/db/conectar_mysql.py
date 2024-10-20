import pandas as pd
import mysql.connector
import numpy as np

# Conexión a MySQL
conexion = mysql.connector.connect(
    host="localhost",       
    user="root",            
    password="",            # Pon tu contraseña de MySQL si tienes una
    database="cuscotrends"  # Nombre de la base de datos
)

# Confirmar que la conexión fue exitosa
if conexion.is_connected():
    print("Conexión exitosa a la base de datos")

    # Truncar la tabla 'reviews' antes de insertar los nuevos datos
    cursor = conexion.cursor()
    cursor.execute("TRUNCATE TABLE reviews;")
    print("Tabla 'reviews' truncada exitosamente.")

    # Leer dataset de TripAdvisor
    tripadvisor_df = pd.read_csv(r"D:/Taller de investigacion/scraping/CuscoTrends/scraping/TripAdvisor/Dataset_after_all.csv")

    # Limpiar y normalizar TripAdvisor
    tripadvisor_df['Opinion Count'] = tripadvisor_df['Opinion Count'].replace('No', -1)
    tripadvisor_df['Rating'] = tripadvisor_df['Rating'].replace('No', -1)
    tripadvisor_df['Image Count'] = tripadvisor_df['Image Count'].replace('No disponible', -1)

    # Asegurarse que los valores sean numéricos donde corresponde
    tripadvisor_df['Opinion Count'] = pd.to_numeric(tripadvisor_df['Opinion Count'], errors='coerce')
    tripadvisor_df['Image Count'] = pd.to_numeric(tripadvisor_df['Image Count'], errors='coerce')
    tripadvisor_df['Rating'] = pd.to_numeric(tripadvisor_df['Rating'], errors='coerce')

    # Crear las columnas de estrellas en TripAdvisor
    tripadvisor_df['5_estrellas'] = pd.to_numeric(tripadvisor_df['Excelente'], errors='coerce')
    tripadvisor_df['4_estrellas'] = pd.to_numeric(tripadvisor_df['Muy bueno'], errors='coerce')
    tripadvisor_df['3_estrellas'] = pd.to_numeric(tripadvisor_df['Promedio'], errors='coerce')
    tripadvisor_df['2_estrellas'] = pd.to_numeric(tripadvisor_df['Mala'], errors='coerce')
    tripadvisor_df['1_estrella'] = pd.to_numeric(tripadvisor_df['Horrible'], errors='coerce')

    # Calcular los porcentajes de las opiniones en TripAdvisor
    tripadvisor_df['5 Estrellas'] = (tripadvisor_df['5_estrellas'] / tripadvisor_df['Opinion Count']) * 100
    tripadvisor_df['4 Estrellas'] = (tripadvisor_df['4_estrellas'] / tripadvisor_df['Opinion Count']) * 100
    tripadvisor_df['3 Estrellas'] = (tripadvisor_df['3_estrellas'] / tripadvisor_df['Opinion Count']) * 100
    tripadvisor_df['2 Estrellas'] = (tripadvisor_df['2_estrellas'] / tripadvisor_df['Opinion Count']) * 100
    tripadvisor_df['1 Estrella'] = (tripadvisor_df['1_estrella'] / tripadvisor_df['Opinion Count']) * 100

    # Reemplazar valores menores a 0 por None para excluir
    tripadvisor_df = tripadvisor_df.replace([-1], np.nan)

    # Leer dataset de Trustpilot
    trustpilot_df = pd.read_csv(r"D:/Taller de investigacion/scraping/CuscoTrends/scraping/Trustpilot/final_tour_reviews.csv")

    # Limpiar y normalizar Trustpilot
    trustpilot_df['Opinion Count'] = pd.to_numeric(trustpilot_df['Total Opinions'], errors='coerce')
    trustpilot_df['Rating'] = trustpilot_df['Rating'].str.replace(',', '.').astype(float)

    # Calcular los porcentajes de las opiniones en Trustpilot
    trustpilot_df['5 Estrellas'] = (trustpilot_df['5_estrellas'] / trustpilot_df['Opinion Count']) * 100
    trustpilot_df['4 Estrellas'] = (trustpilot_df['4_estrellas'] / trustpilot_df['Opinion Count']) * 100
    trustpilot_df['3 Estrellas'] = (trustpilot_df['3_estrellas'] / trustpilot_df['Opinion Count']) * 100
    trustpilot_df['2 Estrellas'] = (trustpilot_df['2_estrellas'] / trustpilot_df['Opinion Count']) * 100
    trustpilot_df['1 Estrella'] = (trustpilot_df['1_estrella'] / trustpilot_df['Opinion Count']) * 100

    # Reemplazar valores menores a 0 por None para excluir
    trustpilot_df = trustpilot_df.replace([-1], np.nan)

    # Renombrar columnas de Trustpilot para unificar con TripAdvisor
    trustpilot_df = trustpilot_df.rename(columns={
        'Business Title': 'Tour Title'
    })

    # Añadir una columna para indicar la fuente de los datos
    tripadvisor_df['Source'] = 'TripAdvisor'
    trustpilot_df['Source'] = 'Trustpilot'

    # Seleccionar las columnas clave para la tabla normalizada final
    tripadvisor_columns = ['Tour Title', 'Source', 'Opinion Count', 'Rating', '5 Estrellas', '4 Estrellas', '3 Estrellas', '2 Estrellas', '1 Estrella']
    trustpilot_columns = ['Tour Title', 'Source', 'Opinion Count', 'Rating', '5 Estrellas', '4 Estrellas', '3 Estrellas', '2 Estrellas', '1 Estrella']

    tripadvisor_df = tripadvisor_df[tripadvisor_columns]
    trustpilot_df = trustpilot_df[trustpilot_columns]

    # Unir ambos datasets
    combined_df = pd.concat([tripadvisor_df, trustpilot_df], ignore_index=True)

    # Filtrar registros que tengan valores menores a 0 en Opinion Count o Rating
    combined_df_filtered = combined_df.dropna(subset=['Opinion Count', 'Rating'])

    # Inserción en la tabla reviews
    insertar_review = """
    INSERT INTO reviews (tour_title, source, opinion_count, rating, estrellas_5, estrellas_4, estrellas_3, estrellas_2, estrellas_1)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Insertar todas las filas excepto aquellas que tengan valores menores a 0
    for index, row in combined_df_filtered.iterrows():
        cursor.execute(insertar_review, (
            row['Tour Title'], 
            row['Source'], 
            row['Opinion Count'], 
            row['Rating'], 
            row['5 Estrellas'], 
            row['4 Estrellas'], 
            row['3 Estrellas'], 
            row['2 Estrellas'], 
            row['1 Estrella']
        ))

    # Confirmar la inserción
    conexion.commit()

    print("Datos insertados exitosamente en la tabla 'reviews'")

    # Cerrar el cursor y la conexión
    cursor.close()
    conexion.close()
