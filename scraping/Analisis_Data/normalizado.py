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
tripadvisor_df['5_estrellas'] = tripadvisor_df['Excelente']
tripadvisor_df['4_estrellas'] = tripadvisor_df['Muy bueno']
tripadvisor_df['3_estrellas'] = tripadvisor_df['Promedio']
tripadvisor_df['2_estrellas'] = tripadvisor_df['Mala']
tripadvisor_df['1_estrella'] = tripadvisor_df['Horrible']

# Leer dataset de Trustpilot
trustpilot_df = pd.read_csv(r"D:/Taller de investigacion/scraping/CuscoTrends/scraping/Trustpilot/Dataset_after_all_purged.csv")

# Limpiar y normalizar Trustpilot
trustpilot_df['Opinion Count'] = trustpilot_df.apply(lambda x: x['Total Opinions'] if x['Opinion Count'] == 'Opiniones' else x['Opinion Count'], axis=1)
trustpilot_df['Rating'] = trustpilot_df['Rating'].str.replace(',', '.').astype(float)

# Renombrar columnas de Trustpilot para unificar con TripAdvisor
trustpilot_df = trustpilot_df.rename(columns={
    'Business Title': 'Tour Title',
    'Total Opinions': 'Opinion Count'
})

# Añadir una columna para indicar la fuente de los datos
tripadvisor_df['Source'] = 'TripAdvisor'
trustpilot_df['Source'] = 'Trustpilot'

# Unir los nombres de las columnas, eliminando duplicados
common_columns = list(set(tripadvisor_df.columns).union(set(trustpilot_df.columns)))

# Asegurarse de que ambos DataFrames tengan las mismas columnas (rellenar con NaN si faltan columnas en cualquiera de los dos)
tripadvisor_df = tripadvisor_df.loc[:, ~tripadvisor_df.columns.duplicated()]
trustpilot_df = trustpilot_df.loc[:, ~trustpilot_df.columns.duplicated()]

tripadvisor_df = tripadvisor_df.reindex(columns=common_columns)
trustpilot_df = trustpilot_df.reindex(columns=common_columns)

# Unir ambos datasets basados en la columna 'Tour URL'
combined_df = pd.concat([tripadvisor_df, trustpilot_df], ignore_index=True)

# Guardar el dataset combinado en un único archivo CSV utilizando punto y coma como delimitador
output_path = r"D:/Taller de investigacion/scraping/CuscoTrends/scraping/Analisis_Data/combined_dataset_normalized.csv"
combined_df.to_csv(output_path, index=False, sep=';')

print(f"Datos combinados y normalizados guardados en: {output_path}")

# Imprimir algunas filas para verificar
print(combined_df.head())
