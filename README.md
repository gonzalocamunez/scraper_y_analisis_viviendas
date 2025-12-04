# Proyecto de datos (Idealista)

## Descripción

Proyecto de análisis de datos de viviendas a partir de un *scraper* de Idealista.

El objetivo es:
- **Explorar** la muestra de viviendas (EDA).
- **Analizar y visualizar** las principales variables del mercado.
- **Generar informes** listos para compartir a partir de los notebooks.

Los datos proceden de un proceso de *scraping* previo (no incluido aquí como código principal) y se almacenan en ficheros como `resultados_scraper.xlsx` y `df_preparado.parquet`.

## Estructura del repositorio

- **`1. EDA/`**  
  Contiene el notebook principal de exploración de datos y los datasets de trabajo:
  - `1. EDA.ipynb`
  - `df_preparado.parquet`
  - `distrib_muestra.xlsx`

- **`2. Visualización y Análisis/`**  
  Notebooks de análisis más detallado y elaboración de informes:
  - `2. viviendas.ipynb`
  - `2. viviendas (informe).ipynb`
  - `3. mercado.ipynb`
  - `3. mercado (informe).ipynb`

- **`img/`**  
  Gráficos exportados desde los notebooks (para informes, presentaciones, etc.).

- **Ficheros de resultados y documentación**
  - `resultados_scraper.xlsx`: resultados tabulares del scraping.
  - `1. EDA/df_preparado.parquet`: dataset preparado para el análisis.
  - `informe_final_proyecto.pdf`: documento principal del proyecto, donde se explica de forma estructurada la metodología, se presentan los análisis y se sintetizan las conclusiones clave.
  - `nuevos_desarrollos.md`: ideas y tareas pendientes/mejoras.

- **Carpeta `0. Knowledge (Cursor context )/`**  
  Documentación auxiliar y scripts relacionados con scraping y configuración (por ejemplo, mitigación de WAF, configuración de navegador camuflado, etc.).

## Requisitos

- Python **3.9+** recomendado.
- Dependencias listadas en `requirements.txt` (Jupyter, ciencia de datos, utilidades de E/S, etc.).

## Preparación del entorno

```bash
# 1) Crear entorno virtual
python3 -m venv .venv

# 2) Activar entorno (macOS / Linux)
source .venv/bin/activate

# 3) Actualizar pip e instalar dependencias
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4) Registrar kernel de Jupyter
python -m ipykernel install --user --name datos-idealista --display-name "Python (.venv) datos-idealista"
```

## Cómo usar los notebooks

1. **Abrir el entorno de trabajo**  
   - Lanzar JupyterLab (`jupyter lab`) o abrir el proyecto en VS Code / otra IDE.

2. **Seleccionar el kernel correcto**  
   - Al abrir cualquier `*.ipynb`, elegir el kernel: `Python (.venv) datos-idealista`.

3. **Orden recomendado de ejecución**  
   - `1. EDA/1. EDA.ipynb` - primera exploración y limpieza.
   - `2. Visualización y Análisis/2. viviendas.ipynb` y `3. mercado.ipynb` - exploraciones y visualizaciones (incluyendo aquellas que no se incorporan al informe final).
   - `2. Visualización y Análisis/2. viviendas (informe).ipynb` y `3. mercado (informe).ipynb` - gráficos y cuadros finales seleccionados que alimentan el `informe_final_proyecto.pdf`.

4. **Datos de entrada**  
   - Asegúrate de que `resultados_scraper.xlsx` y/o `df_preparado.parquet` están disponibles en la raíz del proyecto o en la ruta esperada por los notebooks.

5. **Salida / resultados**  
   - Los gráficos se guardan típicamente en `img/`.
   - Las tablas y estadísticas clave se resumen en los informes `informe_final_proyecto.*`.

## Notas y buenas prácticas

- **Gestión de datos grandes**: guarda datasets muy pesados fuera del repositorio o añade las rutas correspondientes a `.gitignore`.
- **Dependencias**: si añades o eliminas librerías usadas en los notebooks, actualiza `requirements.txt`.
- **Nuevos desarrollos**: anota ideas, experimentos y próximos pasos en `nuevos_desarrollos.md`.
- **Scraping / WAF**: para detalles sobre configuración de scraping, consulta la carpeta `0. Knowledge (Cursor context )/` y su documentación asociada.

