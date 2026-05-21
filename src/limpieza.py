import pandas as pd
import logging
import os
from datetime import datetime

# Configuración del log para que siga escribiendo en el mismo archivo de evidencia
logging.basicConfig(
    filename='pipeline_dataops.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [LIMPIEZA] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def ejecutar_limpieza(ruta_entrada, ruta_salida):
    """
    Toma los datos crudos, aplica reglas de limpieza y estandarización,
    y guarda el resultado en la zona limpia.
    """
    logging.info("Iniciando etapa automatizada de limpieza y transformación.")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando limpieza de datos...")
    
    if not os.path.exists(ruta_entrada):
        logging.error(f"No se encontró el archivo de entrada: {ruta_entrada}")
        return False

    try:
        df = pd.read_csv(ruta_entrada)
        filas_iniciales = len(df)
        
        # 1. Eliminación de duplicados exactos
        df = df.drop_duplicates()
        duplicados_eliminados = filas_iniciales - len(df)
        logging.info(f"Transformación: Se eliminaron {duplicados_eliminados} registros duplicados.")
        
        # 2. Estandarización de texto (transformar a minúsculas para evitar errores futuros)
        cols_texto = ['job', 'marital', 'education', 'contact', 'month', 'poutcome']
        for col in cols_texto:
            if col in df.columns:
                df[col] = df[col].astype(str).str.lower()
                
        # 3. Monitoreo de anomalías: Conteo de valores 'unknown' 
        # (Esto te sirve para justificar el manejo de anomalías en la presentación)
        unknowns = (df == 'unknown').sum().sum()
        logging.info(f"Monitoreo: Se detectaron {unknowns} valores 'unknown' en variables categóricas. Se mantienen para no perder volumen analítico.")
        
        # 4. Guardar los datos limpios
        df.to_csv(ruta_salida, index=False)
        logging.info(f"Limpieza exitosa. Archivo guardado en: {ruta_salida}. Filas finales listas para validación: {len(df)}")
        print(f"[+] Etapa de limpieza finalizada. Filas resultantes: {len(df)}")
        
        return True
        
    except Exception as e:
        logging.error(f"Fallo durante la limpieza de datos: {str(e)}")
        print(f"[-] Error inesperado: {str(e)}")
        return False

if __name__ == "__main__":
    # Rutas de entrada (el crudo que creamos) y salida (el limpio)
    RUTA_RAW = "data/raw_ingested.csv"
    RUTA_CLEAN = "data/banco_limpio.csv"
    
    ejecutar_limpieza(RUTA_RAW, RUTA_CLEAN)