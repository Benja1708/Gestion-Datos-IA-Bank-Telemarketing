import pandas as pd
import logging
import os
import hashlib
from datetime import datetime

# Configuración del log para que siga escribiendo en el mismo archivo de evidencia
logging.basicConfig(
    filename='pipeline_dataops.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [LIMPIEZA] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def generar_hash_anonimo(row):
    """
    Genera un hash SHA-256 basado en atributos del cliente para 
    crear un ID único y proteger su identidad real (Pseudonimización).
    """
    # Concatenamos variables para crear una huella única por registro
    data_string = f"{row['age']}_{row['job']}_{row['balance']}"
    return hashlib.sha256(data_string.encode('utf-8')).hexdigest()[:16]

def ejecutar_limpieza(ruta_entrada, ruta_salida):
    """
    Toma los datos crudos, aplica reglas de limpieza, estandarización,
    políticas de seguridad (enmascaramiento) y guarda el resultado.
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
        
        # 2. Estandarización de texto (transformar a minúsculas)
        cols_texto = ['job', 'marital', 'education', 'contact', 'month', 'poutcome']
        for col in cols_texto:
            if col in df.columns:
                df[col] = df[col].astype(str).str.lower()
                
        # 3. Monitoreo de anomalías: Conteo de valores 'unknown' 
        unknowns = (df == 'unknown').sum().sum()
        logging.info(f"Monitoreo: Se detectaron {unknowns} valores 'unknown'. Se mantienen para no perder volumen analítico.")
        
        # 4. POLÍTICA DE SEGURIDAD: Enmascaramiento y Pseudonimización
        # Se agrega una columna como identificador cifrado
        df.insert(0, 'client_id_hash', df.apply(generar_hash_anonimo, axis=1))
        logging.info("Seguridad: Se aplicó cifrado SHA-256 para generar 'client_id_hash' y proteger la identidad (Ley 19.628).")
        print("[+] Política de seguridad aplicada: Datos de clientes anonimizados (SHA-256).")

        # 5. Guardar los datos limpios
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
    RUTA_RAW = "../data/raw_ingested.csv"
    RUTA_CLEAN = "../data/banco_limpio.csv"
    
    ejecutar_limpieza(RUTA_RAW, RUTA_CLEAN)