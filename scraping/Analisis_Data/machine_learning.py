import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
import seaborn as sns

# Cargar el archivo CSV
df = pd.read_csv("combined_dataset_normalized.csv", sep=";", encoding='utf-8')

# --- LIMPIEZA DE DATOS ---
def clean_data():
    """
    Reemplaza valores "No" por NaN y asegura que las columnas relevantes sean numéricas.
    Además, elimina caracteres especiales en las columnas numéricas y convierte el formato a float.
    """
    columns_to_replace = ['Opinion Count', 'Image Count', 'Rating', 'Excelente', 'Muy bueno', 'Promedio', 'Mala', 'Horrible',
                          '1_estrella', '2_estrellas', '3_estrellas', '4_estrellas', '5_estrellas']

    # Reemplazar "No" por NaN y convertir las columnas a numérico
    for col in columns_to_replace:
        df[col] = df[col].replace('No', np.nan)  # Reemplazar "No" por NaN
        df[col] = df[col].replace(',', '', regex=True)  # Eliminar comas en los valores numéricos
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Convertir a numérico

    # Eliminar filas con NaN en las columnas numéricas
    df.dropna(subset=columns_to_replace, inplace=True)

# Ejecutar la limpieza de datos
clean_data()

# --- Visualización: Heatmap de correlaciones ---
def heatmap():
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
heatmap()

# --- Funciones de Machine Learning ---

# 1. Linear Regression para Rating vs. Opinion Count y Image Count
def rating_ReviewPicture_LinearRegression():
    """
    Aplica regresión lineal a 'Rating' usando 'Opinion Count' e 'Image Count' como predictores.
    """
    X = df[['Opinion Count', 'Image Count']]
    y = df['Rating']
    
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
    
    print("Linear Regression (Opinion Count & Image Count):")
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")
    print(f"Adjusted R-squared: {adjusted_r2}")
    
    # Visualizar resultados
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_pred, alpha=0.7)
    plt.xlabel("Actual Ratings")
    plt.ylabel("Predicted Ratings")
    plt.title("Linear Regression - Actual vs. Predicted Ratings")
    plt.show()

# 2. Linear Regression para todos los parámetros
def rating_LinearRegression():
    """
    Aplica regresión lineal usando todas las columnas numéricas para predecir el 'Rating'.
    """
    # Eliminar columnas no numéricas
    X = df.drop(['Rating', 'Tour Title', 'Tour URL', 'Source'], axis=1)  # 'Source' añadido
    y = df['Rating']
    
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
    
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_pred, alpha=0.7)
    plt.xlabel("Actual Ratings")
    plt.ylabel("Predicted Ratings")
    plt.title("Linear Regression - Actual vs. Predicted Ratings")
    plt.show()

# 3. Decision Tree Regression con búsqueda de hiperparámetros
def rating_Decision_Tree_Regression():
    """
    Aplica un modelo de árbol de decisión para predecir 'Rating'.
    Incluye búsqueda de hiperparámetros con GridSearchCV.
    """
    # Eliminar columnas no numéricas
    X = df.drop(['Rating', 'Tour Title', 'Tour URL', 'Source'], axis=1)  # 'Source' añadido
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
    
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_pred, alpha=0.7)
    plt.xlabel("Actual Ratings")
    plt.ylabel("Predicted Ratings")
    plt.title("Decision Tree Regression - Actual vs. Predicted Ratings")
    plt.show()

# 4. Random Forest Regression con GridSearchCV
def rating_Random_Forest_Regression():
    """
    Aplica un modelo de bosque aleatorio para predecir 'Rating'.
    Incluye búsqueda de hiperparámetros con GridSearchCV.
    """
    # Eliminar columnas no numéricas
    X = df.drop(['Rating', 'Tour Title', 'Tour URL', 'Source'], axis=1)  # 'Source' añadido
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
    
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_pred, alpha=0.7)
    plt.xlabel("Actual Ratings")
    plt.ylabel("Predicted Ratings")
    plt.title("Random Forest Regression - Actual vs. Predicted Ratings")
    plt.show()

# --- Ejecutar Modelos ---
rating_ReviewPicture_LinearRegression()
rating_LinearRegression()
rating_Decision_Tree_Regression()
rating_Random_Forest_Regression()
