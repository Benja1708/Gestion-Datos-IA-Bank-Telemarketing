# Gestión de Datos para IA - Pipeline DataOps Telemarketing Bancario

## 📋 Resumen Ejecutivo
Este proyecto implementa un ciclo de vida de datos automatizado (DataOps) para procesar información de campañas de telemarketing bancario. El valor para la organización radica en transformar datos crudos y propensos a errores en un conjunto de datos limpio, validado y listo para modelos predictivos (Machine Learning). Esto permite predecir con mayor precisión si un cliente suscribirá un depósito a plazo, optimizando los recursos de la campaña y mejorando el retorno de inversión.

## 🏗️ Justificación de la Metodología (PMBOK Adaptativa)
Se ha seleccionado una **metodología ágil (adaptativa)** del PMBOK. A diferencia de un enfoque predictivo tradicional, el enfoque adaptativo es fundamental en proyectos de DataOps, ya que permite iterar sobre las reglas de limpieza y validación a medida que se descubren nuevas anomalías en los datos. Esto facilita la entrega continua de valor mediante entregables incrementales, asegurando que el pipeline se adapte rápidamente a variaciones en el formato de los datos de origen.

## 📂 Arquitectura y Estructura del Repositorio
El proyecto sigue una arquitectura modular, separando los procesos lógicos para facilitar el mantenimiento y la escalabilidad:
* `data/`: Almacena el dataset original (`02_bank.csv`), los datos intermedios limpios/validados y la salida final (`carga_oracle.sql`).
* `src/ingesta.py`: Módulo encargado de la extracción y lectura inicial de los datos.
* `src/limpieza.py`: Módulo para el tratamiento de valores nulos, estandarización de columnas categóricas (ej. imputación de "unknown") y eliminación de registros duplicados.
* `src/validacion.py`: Módulo central de DataOps que aplica reglas de negocio estrictas (ej. verificación de la mayoría de edad y coherencia de rangos numéricos).
* `src/carga.py`: Módulo final que consolida los datos procesados y genera los archivos de salida para su consumo.

## 🛡️ Plan de Seguridad DataOps
Para garantizar la confidencialidad e integridad de la información bancaria, el diseño del entorno contempla las siguientes políticas:
* **Cumplimiento Legal:** El procesamiento de los datos se diseña en estricto apego a la **Ley N° 19.628 sobre Protección de la Vida Privada (Chile)**, garantizando que la información personal de los clientes bancarios se utilice exclusivamente para los fines analíticos autorizados.
* **Técnicas de Protección:** Se establecen directrices para el enmascaramiento de datos personales en el código y el uso de técnicas de cifrado tanto para los datos en reposo (bases de datos) como en tránsito durante la carga.

## 📈 Estrategia de Monitoreo y KPIs
El seguimiento de la salud del pipeline se realiza mediante los siguientes Indicadores Clave de Rendimiento (KPIs):
* **Latencia:** Tiempo total de ejecución (en segundos o milisegundos) de cada etapa del pipeline, garantizando la eficiencia temporal ante mayores volúmenes de datos.
* **Completitud:** Porcentaje de registros validados y cargados exitosamente en comparación con el volumen total extraído en la ingesta.
* **Tasa de Anomalías:** Detección y conteo de registros que no cumplen con la estructura semántica (ej. campos vacíos críticos o edades ilógicas).

## 🔮 Conclusiones y Próximos Pasos
La solución actual establece un flujo de datos robusto y estructurado. Los próximos pasos para evolucionar este proyecto son:
1. Implementar contenedorización con **Docker** para estandarizar el entorno de ejecución.
2. Configurar Integración y Despliegue Continuo (CI/CD) mediante **GitHub Actions** para automatizar pruebas del código ante cada actualización.
3. Desplegar alertas automáticas que notifiquen a los ingenieros si el KPI de completitud cae por debajo de un umbral aceptable.

---
**Autor:** Bastián Ignacio Frey Pérez & Benjamin Bastias
Estudiante de Ingeniería en Informática, DuocUC.
*Evaluación Parcial N°2 - Asignatura Gestión de Datos para IA (ITY1101).*
