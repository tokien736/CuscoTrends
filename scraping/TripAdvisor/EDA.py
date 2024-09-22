import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

# Cargar el archivo CSV que el usuario ha subido
file_path = 'Dataset_after_all.csv'
df = pd.read_csv(file_path)

def change_to_numeric_and_scale():
    """
    Convierte las columnas relevantes a valores numéricos, incluyendo Opinion Count, Image Count y Rating.
    Reemplaza valores no numéricos por NaN y asegura que la escala de Rating esté entre 1 y 5.
    """
    # Convertir Opinion Count e Image Count a numéricos
    df['Opinion Count'] = pd.to_numeric(df['Opinion Count'].str.replace(',', ''), errors='coerce')
    df['Image Count'] = pd.to_numeric(df['Image Count'].str.replace(',', ''), errors='coerce')

    # Convertir Rating a numérico y asegurar que los valores estén en la escala de 1 a 5
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    df['Rating'] = df['Rating'].apply(lambda x: x if 1 <= x <= 5 else pd.NA)

    # Convertir las columnas de reseñas a numéricos
    review_columns = ['Excelente', 'Muy bueno', 'Promedio', 'Mala', 'Horrible']
    for col in review_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Ejecutar la conversión de datos a numéricos y la escala correcta
change_to_numeric_and_scale()

# --- Visualizaciones ---

# Función para graficar barras para Rating vs Opinion Count
def rating_reviews_PlotBar():
    """
    Grafica una barra que muestra el promedio de 'Opinion Count' por 'Rating' en una escala de 1 a 5.
    """
    x_parameter = 'Rating'
    y_parameter = 'Opinion Count'

    # Agrupar datos por Rating y calcular el promedio de Opinion Count
    grouped_data = df.groupby(x_parameter)[y_parameter].mean()
    
    plt.figure(figsize=(8, 6))
    sns.barplot(x=grouped_data.index, y=grouped_data.values)  # Graficar barras
    plt.xlabel(x_parameter)
    plt.ylabel(y_parameter)
    plt.title(f"Promedio de {y_parameter} por {x_parameter}")
    plt.show()

# Función para graficar barras para Rating vs Image Count
def rating_image_count_PlotBar():
    """
    Grafica una barra que muestra el promedio de 'Image Count' por 'Rating' en una escala de 1 a 5.
    """
    x_parameter = 'Rating'
    y_parameter = 'Image Count'

    # Agrupar datos por Rating y calcular el promedio de Image Count
    grouped_data = df.groupby(x_parameter)[y_parameter].mean()

    plt.figure(figsize=(8, 6))
    sns.barplot(x=grouped_data.index, y=grouped_data.values)  # Graficar barras
    plt.xlabel(x_parameter)
    plt.ylabel(y_parameter)
    plt.title(f"Promedio de {y_parameter} por {x_parameter}")
    plt.show()

# Función para graficar un gráfico de dispersión entre Opiniones y Rating con escala logarítmica
def opinion_vs_rating_ScatterPlot():
    """
    Grafica un gráfico de dispersión entre 'Opinion Count' y 'Rating'.
    Aplica una escala logarítmica en el eje X (Opinion Count) para manejar mejor los datos de gran rango.
    Se eliminan valores NaN para evitar errores en la visualización.
    """
    x_parameter = 'Opinion Count'
    y_parameter = 'Rating'

    # Eliminar filas con NaN en Opinion Count o Rating
    df_filtered = df.dropna(subset=[x_parameter, y_parameter])

    plt.figure(figsize=(8, 6))
    plt.scatter(df_filtered[x_parameter], df_filtered[y_parameter], alpha=0.6)  # Gráfico de dispersión
    plt.xscale('log')  # Aplicar escala logarítmica en el eje X
    plt.xlabel(x_parameter)
    plt.ylabel(y_parameter)
    plt.title(f"Opiniones vs Rating (Escala Logarítmica en Opiniones)")
    plt.show()

# Función para graficar la distribución de los tipos de reseñas
def rating_distribution_PlotBar():
    """
    Grafica una barra apilada que muestra la distribución de tipos de reseñas (Excelente, Muy bueno, etc.)
    por 'Rating' con la escala de 1 a 5.
    """
    # Agrupar por Rating y calcular el promedio de las categorías de reseñas
    grouped_data = df.groupby('Rating')[['Excelente', 'Muy bueno', 'Promedio', 'Mala', 'Horrible']].mean()

    grouped_data.plot(kind='bar', stacked=True, figsize=(10, 7))  # Gráfico de barras apiladas

    plt.xlabel('Rating')
    plt.ylabel('Distribución de comentarios')
    plt.title('Distribución de comentarios por Rating (Escala 1 a 5)')
    plt.show()

# Función para mostrar el heatmap de correlaciones entre variables
def heatmap():
    """
    Genera un mapa de calor que muestra las correlaciones entre las variables numéricas.
    Antes de calcular la correlación, eliminamos las filas que contienen valores NaN.
    """
    # Eliminar filas con valores NaN en las columnas relevantes
    df_filtered = df[['Opinion Count', 'Image Count', 'Rating', 'Excelente', 'Muy bueno', 'Promedio', 'Mala', 'Horrible']].dropna()

    # Calcular la matriz de correlaciones
    corr_matrix = df_filtered.corr()

    # Mostrar la matriz de correlación en un mapa de calor
    plt.figure(figsize=(10, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Mapa de calor de las correlaciones entre variables')
    plt.show()

# Ejecutar las funciones de visualización
rating_reviews_PlotBar()
rating_image_count_PlotBar()
opinion_vs_rating_ScatterPlot()
rating_distribution_PlotBar()
heatmap()
