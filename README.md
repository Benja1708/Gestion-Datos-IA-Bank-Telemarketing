# Gestión de Datos para IA - Pipeline DataOps y Modelo Predictivo (Telemarketing Bancario)

## 📋 Resumen Ejecutivo
Este proyecto implementa un ciclo de vida de datos automatizado (DataOps) que culmina en el entrenamiento de un modelo de Inteligencia Artificial para procesar información de campañas de telemarketing bancario. El valor para la organización radica en transformar datos crudos en un conjunto de datos validado, el cual alimenta un modelo predictivo capaz de determinar con alta precisión si un cliente suscribirá un depósito a plazo. Esto permite optimizar los recursos de la campaña, mejorar el retorno de inversión y monitorear los resultados mediante un dashboard interactivo de Business Intelligence.

## 🏗️ Justificación de la Metodología (PMBOK Adaptativa)
Se ha seleccionado una **metodología ágil (adaptativa)** del PMBOK. A diferencia de un enfoque predictivo tradicional, el enfoque adaptativo es fundamental en proyectos de DataOps e IA, ya que permite iterar sobre las reglas de limpieza a medida que se descubren anomalías, y ajustar los hiperparámetros del modelo predictivo de forma incremental para asegurar la entrega continua de valor.

## 📂 Arquitectura y Estructura del Repositorio
El proyecto sigue una arquitectura modular, separando los procesos lógicos para facilitar el mantenimiento y la escalabilidad:
* `data/`: Almacena el dataset original, los datos limpios (`banco_validado.csv`), scripts SQL de salida y visualizaciones analíticas (matriz de correlación).
* `src/ingesta.py`: Módulo de extracción y lectura inicial de los datos.
* `src/limpieza.py`: Tratamiento de nulos y estandarización de columnas categóricas.
* `src/validacion.py`: Aplicación de reglas de negocio estrictas (ej. verificación de mayoría de edad).
* `src/carga.py`: Consolidación y persistencia de los datos procesados.
* **[NUEVO] `src/entrenamiento.py`:** Módulo de Inteligencia Artificial para el análisis bivariado, codificación de variables y entrenamiento del modelo predictivo.
* **`requirements.txt`:** Define las dependencias del entorno, incluyendo `pandas`, `scikit-learn`, `matplotlib` y `seaborn`.

## 🧠 Entrenamiento de Modelo IA y Resultados
A partir de los datos limpios, se implementó un modelo de clasificación binaria utilizando el algoritmo **Random Forest**. Tras el entrenamiento, el modelo demostró un rendimiento altamente efectivo para los objetivos comerciales del banco:
* **Accuracy (Exactitud): 84.10%** (Clasificación correcta general de los clientes).
* **Recall (Sensibilidad): 86.41%** (Métrica clave de negocio: capacidad de identificar correctamente a la gran mayoría de los clientes realmente dispuestos a invertir).
* **Indicador Gini: 82.56%** (Alta capacidad de discriminación del algoritmo).

## 📊 Integración BI (Business Intelligence)
Los resultados del pipeline y el archivo `banco_validado.csv` se integraron directamente con **Looker Studio**. Se diseñó un dashboard interactivo que permite a la gerencia monitorear visualmente la proporción de aceptación de la campaña, analizar la matriz de correlación del modelo y revisar los KPIs de éxito en tiempo real.

## 🛡️ Plan de Seguridad DataOps y Cumplimiento Legal
Para garantizar la confidencialidad de la información bancaria:
* **Cumplimiento Legal:** El procesamiento se rige estrictamente por la **Ley N° 19.628 sobre Protección de la Vida Privada (Chile)**.
* **Separación de Roles y Anonimización:** Se aplica el principio de mínimo privilegio. Los Data Engineers realizan el enmascaramiento de PII (Información de Identificación Personal) en la ingesta, garantizando que los Data Scientists entrenen el modelo utilizando exclusivamente datos anonimizados, sin posibilidad de identificar a los clientes.

## 📈 Estrategia de Monitoreo y KPIs
El seguimiento de la salud del pipeline se realiza mediante:
* **Latencia:** Tiempo total de ejecución de cada etapa del pipeline.
* **Completitud:** Porcentaje de registros validados frente a los extraídos.
* **Tasa de Anomalías:** Detección de registros que no cumplen la semántica esperada.

## 🔮 Conclusiones y Próximos Pasos (Arquitectura Cloud)
La evolución de este proyecto valida que la ingeniería de datos y la IA transforman un flujo operativo en una herramienta estratégica. Para escalar esta solución a un nivel empresarial, proponemos:
1. **Migración a la Nube:** Trasladar la ejecución y entrenamiento a servicios cloud (AWS/Oracle Cloud) para asegurar escalabilidad horizontal.
2. **Implementación de MLOps:** Integrar herramientas como MLflow para el versionado automático de modelos y monitoreo de *Data Drift*.
3. **Orquestación Avanzada:** Migrar la ejecución a Apache Airflow para automatizar el re-entrenamiento en horarios nocturnos.

---
**Autores:** Bastián Ignacio Frey Pérez & Benjamin Bastias
Estudiantes de Ingeniería en Informática, DuocUC.
*Evaluación Parcial N°3 - Asignatura Gestión de Datos para IA (ITY1101).*
