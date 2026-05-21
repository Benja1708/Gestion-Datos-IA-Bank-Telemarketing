import pandas as pd
import logging
import os
from datetime import datetime

# Mismo log de siempre para la trazabilidad completa
logging.basicConfig(
    filename='pipeline_dataops.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [CARGA] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def ejecutar_carga(ruta_entrada, ruta_sql_salida):
    """
    Toma los datos validados y genera el script de carga con sintaxis de Oracle
    para su inserción final en el Data Warehouse.
    """
    logging.info("Iniciando etapa final: Carga de datos.")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando carga de datos...")
    
    if not os.path.exists(ruta_entrada):
        logging.error(f"No se encontró el archivo validado: {ruta_entrada}")
        return False
        
    try:
        df = pd.read_csv(ruta_entrada)
        
        # Generar script SQL para Oracle
        with open(ruta_sql_salida, 'w', encoding='utf-8') as f:
            f.write("-- ==========================================\n")
            f.write("-- Script de Carga Automática para Oracle SQL\n")
            f.write("-- ==========================================\n\n")
            
            # Prevención de errores si la tabla ya existe
            f.write("BEGIN\n")
            f.write("   EXECUTE IMMEDIATE 'DROP TABLE BANK_MARKETING_GOLD';\n")
            f.write("EXCEPTION\n")
            f.write("   WHEN OTHERS THEN\n")
            f.write("      IF SQLCODE != -942 THEN\n")
            f.write("         RAISE;\n")
            f.write("      END IF;\n")
            f.write("END;\n/\n\n")
            
            # Creación de tabla con tipos de datos Oracle
            f.write("CREATE TABLE BANK_MARKETING_GOLD (\n")
            f.write("    age NUMBER,\n")
            f.write("    job VARCHAR2(50),\n")
            f.write("    marital VARCHAR2(50),\n")
            f.write("    education VARCHAR2(50),\n")
            f.write("    default_credit VARCHAR2(10), -- Renombrado para evitar conflicto con palabra reservada de Oracle\n")
            f.write("    balance NUMBER,\n")
            f.write("    housing VARCHAR2(10),\n")
            f.write("    loan VARCHAR2(10),\n")
            f.write("    contact VARCHAR2(50),\n")
            f.write("    day NUMBER,\n")
            f.write("    month VARCHAR2(20),\n")
            f.write("    duration NUMBER,\n")
            f.write("    campaign NUMBER,\n")
            f.write("    pdays NUMBER,\n")
            f.write("    previous NUMBER,\n")
            f.write("    poutcome VARCHAR2(50),\n")
            f.write("    deposit VARCHAR2(10)\n")
            f.write(");\n/\n\n")
            
            logging.info("Estructura de tabla Oracle generada en el script.")
            
            f.write("-- Inserción de registros validados\n")
            
            registros_procesados = 0
            for index, row in df.iterrows():
                valores = []
                for val in row:
                    if pd.isna(val):
                        valores.append("NULL")
                    elif isinstance(val, (int, float)):
                        valores.append(str(val))
                    else:
                        # Escapar comillas simples de los textos para que Oracle no falle
                        val_str = str(val).replace("'", "''")
                        valores.append(f"'{val_str}'")
                
                linea_insert = f"INSERT INTO BANK_MARKETING_GOLD VALUES ({', '.join(valores)});\n"
                f.write(linea_insert)
                registros_procesados += 1
            
            f.write("COMMIT;\n/\n")
            
        logging.info(f"Script de carga Oracle generado con {registros_procesados} sentencias INSERT.")
        print(f"[+] Etapa de carga lista. Archivo SQL generado: {ruta_sql_salida}")
        return True

    except Exception as e:
        logging.error(f"Fallo en la generación de la carga: {str(e)}")
        print(f"[-] Error inesperado: {str(e)}")
        return False

if __name__ == "__main__":
    RUTA_VALIDADO = "data/banco_validado.csv"
    RUTA_SQL = "data/carga_oracle.sql"
    
    ejecutar_carga(RUTA_VALIDADO, RUTA_SQL)