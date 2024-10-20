import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# Función para conectar a la base de datos MySQL usando SQLAlchemy
def conectar_mysql():
    """
    Establece la conexión con la base de datos MySQL utilizando SQLAlchemy sin contraseña.
    """
    try:
        # Conexión sin contraseña
        engine = create_engine("mysql+mysqlconnector://root:@localhost/cuscotrends")
        print("Conexión exitosa a la base de datos")
        return engine
    except Exception as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

# --- Cargar los datos desde la base de datos ---
def cargar_datos_desde_bd():
    """
    Carga los datos de la tabla 'reviews' desde la base de datos y los devuelve en un DataFrame.
    """
    engine = conectar_mysql()
    if engine is None:
        return None
    
    query = "SELECT * FROM reviews"
    df = pd.read_sql(query, engine)
    return df

# --- LIMPIEZA DE DATOS ---
def change_to_numeric_and_clean(df):
    """
    Convierte las columnas relevantes a valores numéricos, incluyendo Opinion Count, Image Count, Rating y las categorías de estrellas.
    Reemplaza valores no numéricos por NaN y corrige los valores.
    """
    # Convertir Opinion Count, Image Count y Rating a numéricos
    df['opinion_count'] = pd.to_numeric(df['opinion_count'], errors='coerce')
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

    # Convertir las columnas de estrellas a numéricos
    review_columns = ['estrellas_5', 'estrellas_4', 'estrellas_3', 'estrellas_2', 'estrellas_1']
    for col in review_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

# --- ANÁLISIS Y VISUALIZACIONES ---

# 1. Grafica de barra para Opiniones vs Rating
def rating_reviews_plot_bar(df):
    """
    Grafica una barra que muestra el promedio de 'opinion_count' por 'rating'.
    """
    grouped_data = df.groupby('rating')['opinion_count'].mean()
    plt.figure(figsize=(8, 6))
    sns.barplot(x=grouped_data.index, y=grouped_data.values)
    plt.xlabel('Rating')
    plt.ylabel('Opinion Count (Promedio)')
    plt.title('Promedio de Opiniones por Rating')
    plt.show()

# 2. Gráfico de dispersión entre Opiniones y Rating
def opinion_vs_rating_scatterplot(df):
    """
    Gráfico de dispersión entre 'opinion_count' y 'rating', aplicando escala logarítmica en el eje X.
    """
    df_filtered = df.dropna(subset=['opinion_count', 'rating'])
    plt.figure(figsize=(8, 6))
    plt.scatter(df_filtered['opinion_count'], df_filtered['rating'], alpha=0.6)
    plt.xscale('log')
    plt.xlabel('Opiniones (log)')
    plt.ylabel('Rating')
    plt.title('Opiniones vs Rating (Escala logarítmica en Opiniones)')
    plt.show()

# 3. Heatmap de correlaciones entre variables
def heatmap(df):
    """
    Mapa de calor para mostrar las correlaciones entre las variables numéricas.
    """
    df_filtered = df[['opinion_count', 'rating', 'estrellas_5', 'estrellas_4', 'estrellas_3', 'estrellas_2', 'estrellas_1']].dropna()
    corr_matrix = df_filtered.corr()
    plt.figure(figsize=(10, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Mapa de calor de correlaciones entre variables')
    plt.show()

# --- EJECUTAR VISUALIZACIONES ---
def main():
    # Cargar los datos desde la base de datos
    df = cargar_datos_desde_bd()

    if df is not None:
        # Limpiar y convertir los datos
        change_to_numeric_and_clean(df)

        # Ejecutar las visualizaciones
        rating_reviews_plot_bar(df)
        opinion_vs_rating_scatterplot(df)
        heatmap(df)
    else:
        print("No se pudieron cargar los datos de la base de datos.")

if __name__ == "__main__":
    main()
