import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from db.conectar_mysql import conectar_mysql, cargar_datos_tripadvisor, cargar_datos_trustpilot, insertar_datos_en_bd

# Función para renombrar las columnas del CSV para que coincidan con las de la base de datos
def renombrar_columnas(df, source):
    """
    Renombra las columnas del CSV para que coincidan con los nombres en la base de datos.
    """
    if source == 'TripAdvisor':
        df.rename(columns={
            'Tour Title': 'tour_title',
            'Opinion Count': 'opinion_count',
            'Rating': 'rating',
            'Excelente': 'estrellas_5',
            'Muy bueno': 'estrellas_4',
            'Promedio': 'estrellas_3',
            'Mala': 'estrellas_2',
            'Horrible': 'estrellas_1'
        }, inplace=True)
    elif source == 'Trustpilot':
        df.rename(columns={
            'Business Title': 'tour_title',
            'Opinion Count': 'opinion_count',
            'Rating': 'rating',
            '5_estrellas': 'estrellas_5',
            '4_estrellas': 'estrellas_4',
            '3_estrellas': 'estrellas_3',
            '2_estrellas': 'estrellas_2',
            '1_estrella': 'estrellas_1'
        }, inplace=True)
    return df

# Función para normalizar los datos
def normalizar_datos(df):
    """
    Aplica la normalización Min-Max a las columnas numéricas relevantes.
    """
    columnas_a_normalizar = ['opinion_count', 'rating', 'estrellas_5', 'estrellas_4', 'estrellas_3', 'estrellas_2', 'estrellas_1']
    
    scaler = MinMaxScaler()
    df[columnas_a_normalizar] = scaler.fit_transform(df[columnas_a_normalizar])
    
    return df

# --- Código principal ---
def main():
    try:
        # Conectarse a MySQL
        conexion = conectar_mysql()

        if conexion is not None:
            # Cargar y procesar los datos de TripAdvisor
            tripadvisor_df = cargar_datos_tripadvisor(r"D:/Taller de investigacion/scraping/CuscoTrends/scraping/TripAdvisor/Dataset_after_all.csv")
            tripadvisor_df['source'] = 'TripAdvisor'
            tripadvisor_df = renombrar_columnas(tripadvisor_df, 'TripAdvisor')

            # Cargar y procesar los datos de Trustpilot
            trustpilot_df = cargar_datos_trustpilot(r"D:/Taller de investigacion/scraping/CuscoTrends/scraping/Trustpilot/final_tour_reviews.csv")
            trustpilot_df['source'] = 'Trustpilot'
            trustpilot_df = renombrar_columnas(trustpilot_df, 'Trustpilot')

            # Seleccionar las columnas clave para la tabla normalizada final
            columnas_clave = ['tour_title', 'source', 'opinion_count', 'rating', 'estrellas_5', 'estrellas_4', 'estrellas_3', 'estrellas_2', 'estrellas_1']

            tripadvisor_df = tripadvisor_df[columnas_clave]
            trustpilot_df = trustpilot_df[columnas_clave]

            # Unir ambos datasets
            combined_df = pd.concat([tripadvisor_df, trustpilot_df], ignore_index=True)

            # Normalizar los datos
            combined_df_normalizado = normalizar_datos(combined_df)

            # Insertar los datos normalizados en la base de datos
            insertar_datos_en_bd(combined_df_normalizado, conexion)

            # Cerrar la conexión
            conexion.close()

    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()
