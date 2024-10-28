import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

# Crear directorio de salida para las gráficas
output_dir = "D:/Taller de investigacion/scraping/CuscoTrends/scraping/Analisis_Data/img/eda"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Función para conectar a la base de datos MySQL usando SQLAlchemy
def conectar_mysql():
    """
    Establece la conexión con la base de datos MySQL utilizando SQLAlchemy sin contraseña.
    """
    try:
        engine = create_engine("mysql+mysqlconnector://root:@localhost/cuscotrends")
        print("Conexión exitosa a la base de datos")
        return engine
    except Exception as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

# Cargar datos desde la base de datos
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

# Limpiar y convertir datos
def change_to_numeric_and_clean(df):
    df['opinion_count'] = pd.to_numeric(df['opinion_count'], errors='coerce')
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    review_columns = ['estrellas_5', 'estrellas_4', 'estrellas_3', 'estrellas_2', 'estrellas_1']
    for col in review_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

# Visualización 1: Gráfica de barra para Opiniones vs Rating
def rating_reviews_plot_bar(df):
    grouped_data = df.groupby('rating')['opinion_count'].mean()
    plt.figure(figsize=(8, 6))
    sns.barplot(x=grouped_data.index, y=grouped_data.values)
    plt.xlabel('Rating')
    plt.ylabel('Opinion Count (Promedio)')
    plt.title('Promedio de Opiniones por Rating')
    output_path = os.path.join(output_dir, "rating_reviews_bar.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Gráfica guardada en {output_path}")

# Visualización 2: Gráfico de dispersión entre Opiniones y Rating
def opinion_vs_rating_scatterplot(df):
    df_filtered = df.dropna(subset=['opinion_count', 'rating'])
    plt.figure(figsize=(8, 6))
    plt.scatter(df_filtered['opinion_count'], df_filtered['rating'], alpha=0.6)
    plt.xscale('log')
    plt.xlabel('Opiniones (log)')
    plt.ylabel('Rating')
    plt.title('Opiniones vs Rating (Escala logarítmica en Opiniones)')
    output_path = os.path.join(output_dir, "opinion_vs_rating_scatter.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Gráfica guardada en {output_path}")

# Visualización 3: Heatmap de correlaciones entre variables
def heatmap(df):
    df_filtered = df[['opinion_count', 'rating', 'estrellas_5', 'estrellas_4', 'estrellas_3', 'estrellas_2', 'estrellas_1']].dropna()
    corr_matrix = df_filtered.corr()
    plt.figure(figsize=(10, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Mapa de calor de correlaciones entre variables')
    output_path = os.path.join(output_dir, "heatmap_correlation.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Gráfica guardada en {output_path}")

# Ejecutar visualizaciones
def main():
    df = cargar_datos_desde_bd()
    if df is not None:
        change_to_numeric_and_clean(df)
        rating_reviews_plot_bar(df)
        opinion_vs_rating_scatterplot(df)
        heatmap(df)
    else:
        print("No se pudieron cargar los datos de la base de datos.")

if __name__ == "__main__":
    main()
