import pandas as pd
import logging
import os
from datetime import datetime

# Seguimos apuntando al mismo log para tener toda la historia junta
logging.basicConfig(
    filename='pipeline_dataops.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [VALIDACION] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def ejecutar_validacion(ruta_entrada, ruta_salida):
    """
    Aplica reglas de negocio (semánticas) y de formato (estructurales)
    para asegurar la calidad del dato antes de la carga final.
    """
    logging.info("Iniciando etapa de validación estructural y semántica.")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando validación de datos...")
    
    if not os.path.exists(ruta_entrada):
        logging.error(f"Archivo no encontrado en la zona de limpieza: {ruta_entrada}")
        return False
        
    try:
        df = pd.read_csv(ruta_entrada)
        
        # 1. Validación Estructural: Comprobar columnas críticas
        columnas_requeridas = ['age', 'job', 'marital', 'balance', 'deposit']
        faltantes = [col for col in columnas_requeridas if col not in df.columns]
        
        if faltantes:
            logging.error(f"Fallo estructural: Faltan las columnas {faltantes}")
            return False
        else:
            logging.info("Validación estructural aprobada: Todas las columnas críticas están presentes.")
            
        # 2. Validación Semántica: Reglas de negocio del banco
        # Regla A: Clientes deben ser mayores de edad (18+)
        filas_invalidas_edad = df[df['age'] < 18].index
        if len(filas_invalidas_edad) > 0:
            logging.warning(f"Anomalía semántica detectada: {len(filas_invalidas_edad)} registros con edad < 18. Excluyendo del dataset final.")
            df = df.drop(filas_invalidas_edad)
            
        # Regla B: El saldo (balance) debe ser un valor numérico válido (rellenamos vacíos con 0)
        nulos_balance = df['balance'].isnull().sum()
        if nulos_balance > 0:
            logging.warning(f"Anomalía semántica: {nulos_balance} registros sin saldo definido. Imputando valor 0.")
            df['balance'] = df['balance'].fillna(0)
            
        logging.info("Validación semántica completada exitosamente.")
        
        # 3. Guardar datos validados (Gold zone)
        df.to_csv(ruta_salida, index=False)
        
        print(f"[+] Etapa de validación finalizada. Filas aprobadas para carga: {len(df)}")
        logging.info(f"Validación exitosa. Archivo final guardado en: {ruta_salida}")
        return True
        
    except Exception as e:
        logging.error(f"Fallo crítico durante la validación: {str(e)}")
        print(f"[-] Error inesperado: {str(e)}")
        return False

if __name__ == "__main__":
    # Tomamos el limpio y generamos el validado final
    RUTA_CLEAN = "data/banco_limpio.csv"
    RUTA_VALIDADO = "data/banco_validado.csv"
    
    ejecutar_validacion(RUTA_CLEAN, RUTA_VALIDADO)