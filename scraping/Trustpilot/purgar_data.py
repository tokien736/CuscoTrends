import pandas as pd
import ast

# Cargar el archivo CSV
df = pd.read_csv('Dataset_after_all.csv')

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

# Aplicar la función para dividir la columna "Review Distribution" y obtener los porcentajes
df[['5_estrellas', '4_estrellas', '3_estrellas', '2_estrellas', '1_estrella']] = df['Review Distribution'].apply(purgar_review_distribution)

# Convertir los porcentajes en números absolutos en función de 'Total Opinions'
df['Total Opinions'] = df['Total Opinions'].astype(int)  # Asegurarnos que 'Total Opinions' es entero

# Multiplicar cada porcentaje por el total de opiniones
df['5_estrellas'] = (df['5_estrellas'] * df['Total Opinions']).round().astype(int)
df['4_estrellas'] = (df['4_estrellas'] * df['Total Opinions']).round().astype(int)
df['3_estrellas'] = (df['3_estrellas'] * df['Total Opinions']).round().astype(int)
df['2_estrellas'] = (df['2_estrellas'] * df['Total Opinions']).round().astype(int)
df['1_estrella'] = (df['1_estrella'] * df['Total Opinions']).round().astype(int)

# Eliminar la columna "Review Distribution" si ya no es necesaria
df.drop(columns=['Review Distribution'], inplace=True)

# Guardar el nuevo CSV purgado con los números absolutos
df.to_csv('Dataset_after_all_purged.csv', index=False)

print("El dataset ha sido purgado, los porcentajes convertidos a números absolutos, y guardado como 'Dataset_after_all_purged.csv'.")
