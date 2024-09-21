import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

# Leer el archivo CSV usando 'utf-8' con manejo de errores en el modo de archivo
with open("Dataset_after_all.csv", encoding='utf-8', errors='replace') as file:
    df = pd.read_csv(file)

def change_to_numeric():
    """
    Convierte las columnas relevantes a valores numéricos.
    """
    params = ['Rating', 'Opinion Count', 'Image Count', 'Excelente', 'Muy bueno', 'Promedio', 'Mala', 'Horrible']
    try:
        for p in params:
            df[p] = pd.to_numeric(df[p].replace('No', '0').str.replace(',', ''), errors='coerce')
    except Exception as e:
        print(f"Error converting to numeric: {e}")

# Función para graficar barras para Rating vs Opinion Count
def rating_reviews_PlotBar():
    x_parameter = 'Rating'
    y_parameter = 'Opinion Count'

    grouped_data = df.groupby(x_parameter)[y_parameter].mean()
    
    plt.bar(grouped_data.index, grouped_data.values)
    plt.xlabel(x_parameter)
    plt.ylabel(y_parameter)
    plt.title(f"Promedio de {y_parameter} por {x_parameter}")
    plt.show()

# Función para graficar barras para Rating vs Image Count
def rating_image_count_PlotBar():
    x_parameter = 'Rating'
    y_parameter = 'Image Count'

    grouped_data = df.groupby(x_parameter)[y_parameter].mean()

    plt.bar(grouped_data.index, grouped_data.values)
    plt.xlabel(x_parameter)
    plt.ylabel(y_parameter)
    plt.title(f"Promedio de {y_parameter} por {x_parameter}")
    plt.show()

# Función para graficar un gráfico de dispersión entre Opiniones y Rating
def opinion_vs_rating_ScatterPlot():
    x_parameter = 'Opinion Count'
    y_parameter = 'Rating'

    plt.scatter(df[x_parameter], df[y_parameter])
    plt.xlabel(x_parameter)
    plt.ylabel(y_parameter)
    plt.title(f"Opiniones vs Rating")
    plt.show()

# Función para graficar la distribución de los tipos de reseñas
def rating_distribution_PlotBar():
    grouped_data = df.groupby('Rating')[['Excelente', 'Muy bueno', 'Promedio', 'Mala', 'Horrible']].mean()

    grouped_data.plot(kind='bar', stacked=True)

    plt.xlabel('Rating')
    plt.ylabel('Distribución de comentarios')
    plt.title('Distribución de comentarios por Rating')
    plt.show()

# Función para mostrar el heatmap de correlaciones
def heatmap():
    plt.figure(figsize=(10, 6))
    corr_matrix = df[['Opinion Count', 'Image Count', 'Rating', 'Excelente', 'Muy bueno', 'Promedio', 'Mala', 'Horrible']].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.title('Mapa de calor de las correlaciones entre variables')
    plt.show()

# Ejecutar las funciones
change_to_numeric()

# Gráficos de barra y dispersión
rating_reviews_PlotBar()
rating_image_count_PlotBar()
opinion_vs_rating_ScatterPlot()
rating_distribution_PlotBar()

# Heatmap de correlaciones
heatmap()
