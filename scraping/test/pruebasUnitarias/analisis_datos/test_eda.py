import unittest
import sys
import os
import pandas as pd

# Agregar la ruta del directorio que contiene EDA.py
sys.path.append(r"D:/Taller de investigacion/scraping/CuscoTrends/scraping/Analisis_Data")

from EDA import rating_reviews_plot_bar, opinion_vs_rating_scatterplot, change_to_numeric_and_clean

class TestEDA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Este método se ejecuta una vez al inicio para configurar el dataset"""
        # Cargar el dataset en el DataFrame
        file_path = r"D:/Taller de investigacion/scraping/CuscoTrends/scraping/Analisis_Data/combined_dataset_normalized.csv"
        cls.df = pd.read_csv(file_path, sep=';')
        
        # Ejecutar la limpieza y conversión de datos
        change_to_numeric_and_clean()

    def test_analisis_numerico_completo(self):
        """CP1: Verificar que los datos numéricos se convierten correctamente"""
        star_columns = ['5 Estrellas', '4 Estrellas', '3 Estrellas', '2 Estrellas', '1 Estrella']
        
        for col in star_columns:
            self.assertTrue(pd.api.types.is_numeric_dtype(self.df[col]), f"{col} no es numérico")
        
        self.assertTrue(pd.api.types.is_numeric_dtype(self.df['Opinion Count']), "'Opinion Count' no es numérico")
        self.assertTrue(pd.api.types.is_numeric_dtype(self.df['Rating']), "'Rating' no es numérico")
    
    def test_manejo_nulos(self):
        """CP2: Verificar que los valores nulos son manejados correctamente"""
        df_with_nans = self.df[self.df.isnull().any(axis=1)]
        self.assertGreater(len(df_with_nans), 0, "El dataset no contiene valores nulos.")

    def test_datos_categoricos(self):
        """CP3: Verificar que se manejan correctamente datos categóricos"""
        if 'Categoria' in self.df.columns:
            self.assertTrue(self.df['Categoria'].dtype == 'object', "'Categoria' no es una columna categórica")
        else:
            self.fail("No se encontró una columna categórica en el dataset")

    def test_rating_reviews_plot_bar(self):
        """CP4: Verificar que la función de gráfico de barras se ejecuta sin errores"""
        try:
            rating_reviews_plot_bar()
        except Exception as e:
            self.fail(f"rating_reviews_plot_bar() lanzó un error: {e}")
    
    def test_opinion_vs_rating_scatterplot(self):
        """CP5: Verificar que la función de gráfico de dispersión se ejecuta sin errores"""
        try:
            opinion_vs_rating_scatterplot()
        except Exception as e:
            self.fail(f"opinion_vs_rating_scatterplot() lanzó un error: {e}")

if __name__ == '__main__':
    unittest.main()
