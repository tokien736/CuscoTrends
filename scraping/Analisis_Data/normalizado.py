import pandas as pd

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

# Guardar el dataset combinado y normalizado en un archivo CSV
output_path = r"D:/Taller de investigacion/scraping/CuscoTrends/scraping/Analisis_Data/combined_dataset_normalized.csv"
combined_df.to_csv(output_path, index=False, sep=';')

print(f"Datos combinados y normalizados guardados en: {output_path}")

# Imprimir algunas filas para verificar
print(combined_df.head())
