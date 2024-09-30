import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

# Cargar el archivo CSV en un DataFrame (usando separador ';' ya que tus datos lo usan)
file_path = 'combined_dataset_normalized.csv'
df = pd.read_csv(file_path, sep=';')

# --- LIMPIEZA DE DATOS ---
def change_to_numeric_and_clean():
    """
    Convierte las columnas relevantes a valores numéricos, incluyendo Opinion Count, Image Count, Rating y las categorías de estrellas.
    Reemplaza valores no numéricos por NaN y corrige los valores.
    """
    # Convertir Opinion Count, Image Count y Rating a numéricos
    df['Opinion Count'] = pd.to_numeric(df['Opinion Count'], errors='coerce')
    df['Image Count'] = pd.to_numeric(df['Image Count'], errors='coerce')
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

    # Convertir las columnas de estrellas y reseñas a numéricos
    review_columns = ['Excelente', 'Muy bueno', 'Promedio', 'Mala', 'Horrible', 
                      '1_estrella', '2_estrellas', '3_estrellas', '4_estrellas', '5_estrellas']
    for col in review_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

# Ejecutar la limpieza y conversión de datos
change_to_numeric_and_clean()

# --- ANÁLISIS Y VISUALIZACIONES ---

# 1. Grafica de barra para Opiniones vs Rating
def rating_reviews_plot_bar():
    """
    Grafica una barra que muestra el promedio de 'Opinion Count' por 'Rating'.
    """
    grouped_data = df.groupby('Rating')['Opinion Count'].mean()
    plt.figure(figsize=(8, 6))
    sns.barplot(x=grouped_data.index, y=grouped_data.values)
    plt.xlabel('Rating')
    plt.ylabel('Opinion Count (Promedio)')
    plt.title('Promedio de Opiniones por Rating')
    plt.show()

# 2. Gráfico de dispersión entre Opiniones y Rating
def opinion_vs_rating_scatterplot():
    """
    Gráfico de dispersión entre 'Opinion Count' y 'Rating', aplicando escala logarítmica en el eje X.
    """
    df_filtered = df.dropna(subset=['Opinion Count', 'Rating'])
    plt.figure(figsize=(8, 6))
    plt.scatter(df_filtered['Opinion Count'], df_filtered['Rating'], alpha=0.6)
    plt.xscale('log')
    plt.xlabel('Opiniones (log)')
    plt.ylabel('Rating')
    plt.title('Opiniones vs Rating (Escala logarítmica en Opiniones)')
    plt.show()

# 3. Heatmap de correlaciones entre variables
def heatmap():
    """
    Mapa de calor para mostrar las correlaciones entre las variables numéricas.
    """
    df_filtered = df[['Opinion Count', 'Image Count', 'Rating', 'Excelente', 'Muy bueno', 'Promedio', 'Mala', 'Horrible']].dropna()
    corr_matrix = df_filtered.corr()
    plt.figure(figsize=(10, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Mapa de calor de correlaciones entre variables')
    plt.show()

# --- EJECUTAR VISUALIZACIONES ---
rating_reviews_plot_bar()
opinion_vs_rating_scatterplot()
heatmap()
