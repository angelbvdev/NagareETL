<img width="1847" height="955" alt="image" src="https://github.com/user-attachments/assets/21767947-fa1c-4526-9993-88567247d871" /># 🌊 NagareETL (流れ) - Data Pipeline Simulator

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-red?style=for-the-badge&logo=flask&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-UI-38bdf8?style=for-the-badge&logo=tailwindcss&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data_Processing-150458?style=for-the-badge&logo=pandas&logoColor=white)

> **Nagare (流れ)**: Palabra japonesa para "Flujo" o "Corriente".

## 📋 Sobre el Proyecto

**NagareETL** es una herramienta educativa interactiva diseñada para visualizar, simular y explicar el ciclo de vida de un **Data Pipeline** moderno bajo la **Arquitectura Medallion** (Bronze, Silver, Gold).

A diferencia de los scripts de ETL tradicionales que corren en silencio en el backend, este proyecto ofrece una interfaz gráfica en tiempo real que permite ver cómo los datos "sucios" son ingeridos, limpiados, transformados y agregados para la toma de decisiones.

Este proyecto fue creado para demostrar conceptos clave de **Ingeniería de Datos** como Data Quality, Orquestación y Procesamiento Distribuido (simulado) en un entorno controlado.

---

## 🏗️ Arquitectura Simulada

Este simulador mapea conceptos locales a servicios reales de una arquitectura Enterprise en Azure:

| Capa (NagareETL) | Concepto Técnico | Equivalente en Azure | Función |
| :--- | :--- | :--- | :--- |
| **Landing (Bronze)** | Ingesta de Datos Crudos | **Azure Data Lake Gen2** | Recepción de archivos JSON sin procesar (Raw). |
| **Processing (Silver)** | Limpieza y Validación | **Azure Databricks / Spark** | Eliminación de nulos, corrección de tipos de datos y descarte de registros corruptos. |
| **Analytics (Gold)** | Agregación de Valor | **Synapse Analytics / SQL** | Cálculo de KPIs (Ventas Totales) listos para consumo. |
| **Dashboard** | Capa de Servicio | **Power BI** | Visualización final para el usuario de negocio. |

---

## ✨ Características Clave

* **Ingesta de Caos (Chaos Engineering):** El sistema genera aleatoriamente "Dirty Data" (archivos corruptos, nulos, errores de formato) para probar la resiliencia del pipeline.
* **Data Quality Gates:** Validación automática que descarta archivos defectuosos (visualizados con bordes rojos) y procesa solo los datos íntegros (bordes verdes).
* **Modo Tutorial Interactivo:** Un sistema de tour guiado paso a paso que enseña al usuario cómo funciona el flujo de datos, bloqueando la interfaz hasta que se completan las tareas de ingeniería.
* **Garbage Collection:** Implementación de almacenamiento efímero; los archivos temporales de procesamiento se limpian automáticamente para optimizar el almacenamiento.
* **Interfaz Reactiva:** UI moderna construida con Tailwind CSS que actualiza el estado del Data Lake sin recargar la página (AJAX).

---

## 🚀 Instalación y Uso

Sigue estos pasos para correr el simulador en tu máquina local:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/angelbvdev/NagareETL.git](https://github.com/angelbvdev/NagareETL.git)
cd NagareETL
2. Crear entorno virtual
Bash

python -m venv venv
# En Windows:
venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate
3. Instalar dependencias
Bash

pip install flask pandas
4. Ejecutar la aplicación
Bash

python run.py
Visita http://127.0.0.1:5000 en tu navegador.

🧠 Lógica Técnica (Deep Dive)
Manejo de Errores y Calidad de Datos
El pipeline no se detiene ante un error. Utiliza un patrón de "Dead Letter Queue" simplificado:

El sistema lee el lote de archivos en Bronze.

Si un registro tiene status: ERROR o campos nulos clave, se marca y se descarta (simulando movimiento a una carpeta de cuarentena).

Solo los registros COMPLETED pasan a la capa Silver.

Eficiencia de Almacenamiento
Para evitar la saturación del disco local durante las pruebas, el sistema implementa una rutina de limpieza post-procesamiento:

Python

# Snippet de routes.py
if data_batch:
    # ... procesamiento ...
    logs.append(f"INFO: Métricas calculadas...")
    # Garbage Collection
    os.remove(silver_path)
```

👨‍💻 Autor
Angel Aldair Burgos Valenzuela Ingeniero en Sistemas Computacionales | Data Engineer 

Apasionado por la nube, la automatización y la cultura japonesa. Este proyecto es parte de mi portafolio para demostrar habilidades Full Stack aplicadas a la Ingeniería de Datos.
