# CuscoTrends

## Introducción

**CuscoTrends** es un proyecto que utiliza técnicas de scraping web para extraer datos de opiniones de TripAdvisor, con el objetivo de analizar y descubrir tendencias relacionadas con el turismo en la ciudad de Cusco. El propósito principal es proporcionar información útil sobre las atracciones turísticas más importantes basadas en las opiniones de los usuarios.

## Tabla de Contenidos
1. [Instalación](#instalación)
2. [Uso](#uso)
3. [Características](#características)
4. [Dependencias](#dependencias)
5. [Configuración](#configuración)
6. [Ejemplos](#ejemplos)
7. [Problemas Comunes](#problemas-comunes)
8. [Contribuidores](#contribuidores)
9. [Licencia](#licencia)

## Instalación

Sigue estos pasos para instalar y configurar el proyecto en tu entorno local:

1. Clona este repositorio:
    ```bash
    git clone https://github.com/tokien736/CuscoTrends.git
    ```
2. Cambia al directorio del proyecto:
    ```bash
    cd CuscoTrends
    ```
3. Instala las dependencias requeridas:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

Para ejecutar el script de scraping y comenzar a recopilar datos de TripAdvisor, sigue los siguientes pasos:

1. Ejecuta el script principal desde el directorio raíz del proyecto:
    ```bash
    python scrape.py
    ```
2. El script descargará las opiniones de las atracciones turísticas de Cusco desde TripAdvisor. Los datos se almacenarán en un archivo CSV en el directorio de salida configurado.

## Características

- **Extracción de Datos:** Recopila automáticamente las opiniones de TripAdvisor sobre diferentes atracciones turísticas en Cusco.
- **Análisis de Tendencias:** Procesa las opiniones y genera estadísticas sobre las calificaciones y comentarios.
- **Exportación:** Los datos se pueden exportar a formatos CSV para un análisis adicional o informes.

## Dependencias

El proyecto requiere las siguientes librerías de Python:

- `requests`: Para realizar las solicitudes HTTP a las páginas web.
- `beautifulsoup4`: Para analizar y extraer los datos de HTML.
- `pandas`: Para el procesamiento y almacenamiento de datos.

Todas las dependencias necesarias están detalladas en el archivo `requirements.txt`.

## Configuración

El proyecto utiliza un archivo de configuración para definir los parámetros de scraping, tales como:

- La URL base de TripAdvisor.
- Opciones para evitar bloqueos por scraping (configuración de user-agent, tiempo de espera, etc.).
- Directorio de salida para los archivos exportados.

Asegúrate de revisar y modificar los parámetros en el archivo de configuración antes de ejecutar el scraping.

## Ejemplos

Un ejemplo básico de cómo ejecutar el script:

```bash
python scrape.py
```

Esto generará un archivo CSV en el directorio `output/` con todas las opiniones de los usuarios.

## Problemas Comunes

- **Bloqueo del sitio web:** Si TripAdvisor detecta el scraping y bloquea las solicitudes, intenta ajustar los tiempos de espera o cambiar el user-agent en la configuración.
- **Errores de conexión:** Asegúrate de tener una conexión a Internet estable. Si el error persiste, verifica la estructura de la URL y las configuraciones de cabecera.

## Contribuidores

- [tokien736](https://github.com/tokien736)

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Para más detalles, consulta el archivo [LICENSE](LICENSE).
