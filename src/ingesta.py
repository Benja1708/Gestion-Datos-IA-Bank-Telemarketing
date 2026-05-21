import os
import logging
import pandas as pd
from datetime import datetime

# Configuración del sistema de Logs (Evidencia obligatoria para la rúbrica)
# Guardará los registros en la carpeta raíz del proyecto
logging.basicConfig(
    filename='pipeline_dataops.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [INGESTA] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def ejecutar_ingesta(ruta_origen, ruta_destino_raw):
    """
    Lee el archivo CSV crudo de telemarketing bancario, valida su existencia
    y lo almacena en la zona de datos crudos (Raw), registrando cada paso en los logs.
    """
    logging.info("Iniciando proceso automatizado de ingesta de datos.")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando etapa de ingesta...")

    # 1. Validación de la existencia del archivo de origen
    if not os.path.exists(ruta_origen):
        mensaje_error = f"Error crítico: No se encontró el archivo origen en '{ruta_origen}'."
        logging.error(mensaje_error)
        print(f"[-] {mensaje_error}")
        return False

    try:
        # 2. Lectura de los datos crudos (Ingesta)
        logging.info(f"Leyendo archivo origen desde: {ruta_origen}")
        df_raw = pd.read_csv(ruta_origen)
        
        filas, columnas = df_raw.shape
        logging.info(f"Lectura exitosa. Dimensiones del dataset cargado: {filas} filas y {columnas} columnas.")

        # 3. Validación rápida de estructura básica (Columnas principales según Metadata)
        columnas_esperadas = ['age', 'job', 'marital', 'balance', 'housing', 'loan', 'deposit']
        columnas_faltantes = [col for col in columnas_esperadas if col not in df_raw.columns]
        
        if columnas_faltantes:
            logging.warning(f"Alerta de estructura: Faltan las siguientes columnas esperadas: {columnas_faltantes}")
        else:
            logging.info("Validación estructural de ingesta completada con éxito. Columnas clave presentes.")

        # 4. Almacenamiento en zona de staging/raw interna del pipeline
        os.makedirs(os.path.dirname(ruta_destino_raw), exist_ok=True)
        df_raw.to_csv(ruta_destino_raw, index=False)
        logging.info(f"Datos crudos respaldados exitosamente en: {ruta_destino_raw}")
        
        print(f"[+] Etapa de ingesta finalizada correctamente. Registros procesados: {filas}")
        logging.info("Finalizando etapa de ingesta sin anomalías técnicas.")
        return True

    except pd.errors.EmptyDataError:
        logging.error("Error en la ingesta: El archivo CSV está vacío.")
        print("[-] Error: El archivo CSV está vacío.")
        return False
    except Exception as e:
        logging.error(f"Error inesperado durante la fase de ingesta: {str(e)}")
        print(f"[-] Error inesperado: {str(e)}")
        return False

if __name__ == "__main__":
    # Definición de rutas relativas compatibles con el entorno local y Docker
    RUTA_ORIGEN = "data/02_bank.csv"
    RUTA_DESTINO = "data/raw_ingested.csv"
    
    ejecutar_ingesta(RUTA_ORIGEN, RUTA_DESTINO)