import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
import seaborn as sns
from sqlalchemy import create_engine
import os

# Crear directorio de salida para las gráficas
output_dir = "D:/Taller de investigacion/scraping/CuscoTrends/scraping/Analisis_Data/img/machine_learning"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Función para conectar a la base de datos MySQL usando SQLAlchemy
def conectar_mysql():
    try:
        engine = create_engine("mysql+mysqlconnector://root:@localhost/cuscotrends")
        print("Conexión exitosa a la base de datos")
        return engine
    except Exception as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

# Cargar los datos desde la base de datos
def cargar_datos_desde_bd():
    engine = conectar_mysql()
    if engine is None:
        return None
    
    query = """
    SELECT tour_title, source, opinion_count, rating, estrellas_5, estrellas_4, 
           estrellas_3, estrellas_2, estrellas_1 
    FROM reviews
    """
    df = pd.read_sql(query, engine)
    print(df.columns)  # Imprimir las columnas para verificar los nombres
    return df

# Limpieza de datos
def clean_data(df):
    columns_to_replace = ['opinion_count', 'rating', 'estrellas_5', 'estrellas_4', 
                          'estrellas_3', 'estrellas_2', 'estrellas_1']
    for col in columns_to_replace:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(subset=columns_to_replace, inplace=True)

# Visualización: Heatmap de correlaciones
def heatmap(df):
    plt.figure(figsize=(10, 6))
    numeric_columns = df.select_dtypes(include=['float64', 'int64'])
    corr_matrix = numeric_columns.corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Mapa de calor de las correlaciones entre variables')
    output_path = os.path.join(output_dir, "heatmap_correlation.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Gráfica guardada en {output_path}")

# Modelos de Machine Learning

# 1. Linear Regression para Rating vs. Opinion Count
def rating_ReviewPicture_LinearRegression(df):
    X = df[['opinion_count']]
    y = df['rating']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    adjusted_r2 = 1 - (1 - r2) * (len(y_test) - 1) / (len(y_test) - X_test.shape[1] - 1)
    print("Linear Regression (Opinion Count):")
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")
    print(f"Adjusted R-squared: {adjusted_r2}")
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_pred, alpha=0.7)
    plt.xlabel("Actual Ratings")
    plt.ylabel("Predicted Ratings")
    plt.title("Linear Regression - Actual vs. Predicted Ratings")
    output_path = os.path.join(output_dir, "linear_regression_opinion_count.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Gráfica guardada en {output_path}")

# 2. Linear Regression para todos los parámetros
def rating_LinearRegression(df):
    X = df.drop(['rating', 'tour_title', 'source'], axis=1)
    y = df['rating']
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
    output_path = os.path.join(output_dir, "linear_regression_all_params.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Gráfica guardada en {output_path}")

# 3. Decision Tree Regression
def rating_Decision_Tree_Regression(df):
    X = df.drop(['rating', 'tour_title', 'source'], axis=1)
    y = df['rating']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
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
    output_path = os.path.join(output_dir, "decision_tree_regression.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Gráfica guardada en {output_path}")

# 4. Random Forest Regression
def rating_Random_Forest_Regression(df):
    X = df.drop(['rating', 'tour_title', 'source'], axis=1)
    y = df['rating']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
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
    output_path = os.path.join(output_dir, "random_forest_regression.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Gráfica guardada en {output_path}")

# Ejecutar Modelos
def main():
    df = cargar_datos_desde_bd()
    if df is not None:
        clean_data(df)
        heatmap(df)
        rating_ReviewPicture_LinearRegression(df)
        rating_LinearRegression(df)
        rating_Decision_Tree_Regression(df)
        rating_Random_Forest_Regression(df)
    else:
        print("No se pudieron cargar los datos desde la base de datos.")

if __name__ == "__main__":
    main()
