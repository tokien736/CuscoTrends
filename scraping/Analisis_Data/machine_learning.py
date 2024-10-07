import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
import seaborn as sns

# Cargar el archivo CSV
df = pd.read_csv("combined_dataset_normalized.csv", sep=";", encoding='utf-8')

# --- LIMPIEZA DE DATOS ---
def clean_data(df):
    """
    Reemplaza valores no disponibles por NaN y asegura que las columnas relevantes sean numéricas.
    """
    columns_to_replace = ['Opinion Count', 'Rating', '5 Estrellas', '4 Estrellas', '3 Estrellas', '2 Estrellas', '1 Estrella']

    # Reemplazar "No" y otros valores inválidos por NaN y convertir las columnas a numérico
    for col in columns_to_replace:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Eliminar filas con NaN en las columnas numéricas
    df.dropna(subset=columns_to_replace, inplace=True)
    return df

# Ejecutar la limpieza de datos
df = clean_data(df)

# --- Verificar la variabilidad de la columna "Rating" ---
print("Resumen de la columna 'Rating':")
print(df['Rating'].describe())

# --- Visualización: Heatmap de correlaciones ---
def heatmap(df):
    """
    Genera un heatmap de las correlaciones entre variables numéricas en el dataframe.
    """
    plt.figure(figsize=(10, 6))
    numeric_columns = df.select_dtypes(include=['float64', 'int64'])  # Solo columnas numéricas
    corr_matrix = numeric_columns.corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Mapa de calor de las correlaciones entre variables')
    plt.show()

# Mostrar el heatmap
heatmap(df)

# --- Función para graficar Actual vs Predicted ---
def plot_actual_vs_predicted(y_test, y_pred, title):
    """
    Genera un gráfico de dispersión con los valores reales vs. los valores predichos.
    Incluye una línea de identidad para facilitar la comparación.
    """
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_pred, alpha=0.7, label='Predicted vs Actual', color='blue')
    
    # Dibujar la línea de identidad (predicción perfecta)
    max_val = max(max(y_test), max(y_pred))
    min_val = min(min(y_test), min(y_pred))
    plt.plot([min_val, max_val], [min_val, max_val], color='red', linestyle='--', label='Perfect Prediction')

    plt.xlabel("Actual Ratings")
    plt.ylabel("Predicted Ratings")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

# --- Funciones de Machine Learning ---

# 1. Linear Regression para Rating vs. Opinion Count y Image Count
def rating_ReviewPicture_LinearRegression(df):
    """
    Aplica regresión lineal a 'Rating' usando 'Opinion Count' e 'Image Count' como predictores.
    """
    X = df[['Opinion Count']]
    y = df['Rating']
    
    # Normalizar los datos si es necesario
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    # Separar en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Entrenar el modelo
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Hacer predicciones
    y_pred = model.predict(X_test)
    
    # Evaluar el modelo
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    adjusted_r2 = 1 - (1 - r2) * (len(y_test) - 1) / (len(y_test) - X_test.shape[1] - 1)
    
    print("Linear Regression (Opinion Count):")
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")
    print(f"Adjusted R-squared: {adjusted_r2}")
    
    # Visualizar resultados usando la función mejorada
    plot_actual_vs_predicted(y_test, y_pred, "Linear Regression - Actual vs. Predicted Ratings (Opinion Count)")

# 2. Linear Regression para todos los parámetros
def rating_LinearRegression(df):
    """
    Aplica regresión lineal usando todas las columnas numéricas para predecir el 'Rating'.
    """
    # Eliminar columnas no numéricas
    X = df.drop(['Rating', 'Tour Title', 'Source'], axis=1)
    y = df['Rating']
    
    # Normalizar los datos si es necesario
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    adjusted_r2 = 1 - (1 - r2) * (len(y_test) - 1) / (len(y_test) - X_test.shape[1] - 1)
    
    print("Linear Regression (Todos los parámetros):")
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")
    print(f"Adjusted R-squared: {adjusted_r2}")
    
    # Visualizar resultados
    plot_actual_vs_predicted(y_test, y_pred, "Linear Regression - Actual vs. Predicted Ratings (Todos los parámetros)")

# 3. Decision Tree Regression con búsqueda de hiperparámetros
def rating_Decision_Tree_Regression(df):
    """
    Aplica un modelo de árbol de decisión para predecir 'Rating'.
    Incluye búsqueda de hiperparámetros con GridSearchCV.
    """
    # Eliminar columnas no numéricas
    X = df.drop(['Rating', 'Tour Title', 'Source'], axis=1)
    y = df['Rating']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Configuración de búsqueda de hiperparámetros
    param_grid = {'max_depth': [3, 5, 10], 'min_samples_split': [2, 5, 10]}
    grid_search = GridSearchCV(DecisionTreeRegressor(random_state=42), param_grid, cv=5, scoring='r2')
    grid_search.fit(X_train, y_train)
    
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print("Decision Tree Regression (Optimized):")
    print(f"Best Params: {grid_search.best_params_}")
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")
    
    # Visualizar resultados
    plot_actual_vs_predicted(y_test, y_pred, "Decision Tree Regression - Actual vs. Predicted Ratings")

# 4. Random Forest Regression con GridSearchCV
def rating_Random_Forest_Regression(df):
    """
    Aplica un modelo de bosque aleatorio para predecir 'Rating'.
    Incluye búsqueda de hiperparámetros con GridSearchCV.
    """
    # Eliminar columnas no numéricas
    X = df.drop(['Rating', 'Tour Title', 'Source'], axis=1)
    y = df['Rating']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Configuración de búsqueda de hiperparámetros
    param_grid = {'n_estimators': [50, 100, 200], 'max_depth': [3, 5, 10]}
    grid_search = GridSearchCV(RandomForestRegressor(random_state=42), param_grid, cv=5, scoring='r2')
    grid_search.fit(X_train, y_train)
    
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print("Random Forest Regression (Optimized):")
    print(f"Best Params: {grid_search.best_params_}")
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")
    
    # Visualizar resultados
    plot_actual_vs_predicted(y_test, y_pred, "Random Forest Regression - Actual vs. Predicted Ratings")

# --- Ejecutar Modelos ---
rating_ReviewPicture_LinearRegression(df)
rating_LinearRegression(df)
rating_Decision_Tree_Regression(df)
rating_Random_Forest_Regression(df)
