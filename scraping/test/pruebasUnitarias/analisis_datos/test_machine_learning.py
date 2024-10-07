import unittest
import pandas as pd
import sys
import os

# Agregar la ruta del directorio que contiene machine_learning.py
sys.path.insert(0, r"D:\Taller de investigacion\scraping\CuscoTrends\scraping\Analisis_Data")

from machine_learning import clean_data, heatmap, rating_ReviewPicture_LinearRegression, rating_LinearRegression, rating_Decision_Tree_Regression, rating_Random_Forest_Regression
from sklearn.metrics import mean_absolute_error

class TestMachineLearning(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Crear un DataFrame de ejemplo similar al dataset proporcionado
        data = {
            'Tour Title': ['No disponible', 'Excursión a la Laguna Humantay Full Day desde Cusco', 'Cusco City Tour Cuatro Ruinas Tour de medio día', 'Excursión a Machu Picchu de Un Día desde Cusco'],
            'Source': ['TripAdvisor', 'TripAdvisor', 'TripAdvisor', 'TripAdvisor'],
            'Opinion Count': [0, 1088, 229, 392],  # Reemplazar valores negativos por 0
            'Rating': [0.0, 5.0, 5.0, 4.5],  # Reemplazar valores negativos por 0.0
            '5 Estrellas': [0.0, None, 95.20, 74.74],
            '4 Estrellas': [0.0, 4.50, 2.62, 12.76],
            '3 Estrellas': [0.0, 0.73, 1.31, 5.87],
            '2 Estrellas': [0.0, 0.28, 0.44, 2.81],
            '1 Estrella': [0.0, 0.37, 0.44, 3.83]
        }
        cls.df = pd.DataFrame(data)
        cls.cleaned_df = clean_data(cls.df)

    def test_clean_data(self):
        # Verificar que los valores no válidos se hayan convertido a NaN y se eliminaron las filas correspondientes
        self.assertFalse(self.cleaned_df.isnull().values.any(), "El DataFrame contiene valores nulos después de la limpieza")
        self.assertTrue((self.cleaned_df[['Opinion Count', 'Rating']] >= 0).all().all(), "El DataFrame contiene valores negativos después de la limpieza")

    def test_heatmap(self):
        # Probar si la función heatmap se ejecuta sin errores
        try:
            heatmap(self.cleaned_df)
        except Exception as e:
            self.fail(f"La función heatmap lanzó una excepción: {e}")

    def test_rating_reviewpicture_linear_regression(self):
        # Probar si la regresión lineal con ReviewPicture se ejecuta sin errores y cumple con MAE < 10%
        try:
            result = rating_ReviewPicture_LinearRegression(self.cleaned_df)
            if result is not None:
                y_true, y_pred = result
                mae = mean_absolute_error(y_true, y_pred)
                self.assertLess(mae, 0.1 * max(y_true), "MAE no cumple con el criterio de ser menor al 10% del valor máximo de las predicciones")
            else:
                self.fail("La función rating_ReviewPicture_LinearRegression no devolvió resultados")
        except Exception as e:
            self.fail(f"La función rating_ReviewPicture_LinearRegression lanzó una excepción: {e}")

    def test_rating_linear_regression(self):
        # Probar si la regresión lineal se ejecuta sin errores y cumple con MAE < 10%
        try:
            result = rating_LinearRegression(self.cleaned_df)
            if result is not None:
                y_true, y_pred = result
                mae = mean_absolute_error(y_true, y_pred)
                self.assertLess(mae, 0.1 * max(y_true), "MAE no cumple con el criterio de ser menor al 10% del valor máximo de las predicciones")
            else:
                self.fail("La función rating_LinearRegression no devolvió resultados")
        except Exception as e:
            self.fail(f"La función rating_LinearRegression lanzó una excepción: {e}")

    def test_rating_decision_tree_regression(self):
        # Probar si la regresión con árbol de decisión se ejecuta sin errores y cumple con MAE < 10%
        try:
            result = rating_Decision_Tree_Regression(self.cleaned_df)
            if result is not None:
                y_true, y_pred = result
                mae = mean_absolute_error(y_true, y_pred)
                self.assertLess(mae, 0.1 * max(y_true), "MAE no cumple con el criterio de ser menor al 10% del valor máximo de las predicciones")
            else:
                self.fail("La función rating_Decision_Tree_Regression no devolvió resultados")
        except ValueError as e:
            if "n_splits=5" in str(e):
                self.fail("Número de divisiones en GridSearchCV mayor que la cantidad de muestras. Reduce 'cv' a un valor menor.")
            else:
                self.fail(f"La función rating_Decision_Tree_Regression lanzó una excepción: {e}")
        except Exception as e:
            self.fail(f"La función rating_Decision_Tree_Regression lanzó una excepción: {e}")

    def test_rating_random_forest_regression(self):
        # Probar si la regresión con Random Forest se ejecuta sin errores y cumple con MAE < 10%
        try:
            result = rating_Random_Forest_Regression(self.cleaned_df)
            if result is not None:
                y_true, y_pred = result
                mae = mean_absolute_error(y_true, y_pred)
                self.assertLess(mae, 0.1 * max(y_true), "MAE no cumple con el criterio de ser menor al 10% del valor máximo de las predicciones")
            else:
                self.fail("La función rating_Random_Forest_Regression no devolvió resultados")
        except ValueError as e:
            if "n_splits=5" in str(e):
                self.fail("Número de divisiones en GridSearchCV mayor que la cantidad de muestras. Reduce 'cv' a un valor menor.")
            else:
                self.fail(f"La función rating_Random_Forest_Regression lanzó una excepción: {e}")
        except Exception as e:
            self.fail(f"La función rating_Random_Forest_Regression lanzó una excepción: {e}")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMachineLearning)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(f"Pruebas ejecutadas: {result.testsRun}, Fallidas: {len(result.failures)}, Saltadas: {len(result.skipped)}")