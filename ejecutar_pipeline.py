import subprocess
import time
import pandas as pd
import os

def ejecutar_modulo(nombre_modulo, ruta_script):
    print(f"\n[{nombre_modulo}] Iniciando...")
    # Ejecuta el script de Python y espera a que termine
    resultado = subprocess.run(["python", ruta_script])
    if resultado.returncode != 0:
        print(f"❌ Error al ejecutar {nombre_modulo}.")
        exit(1)

if __name__ == "__main__":
    print("=== INICIANDO PIPELINE DATAOPS BANK TELEMARKETING ===")
    
    # 1. Inicio del cronómetro para el KPI de Latencia
    start_time = time.time()

    # 2. Ejecución secuencial de los scripts
    ejecutar_modulo("FASE 1: INGESTA", "src/ingesta.py")
    ejecutar_modulo("FASE 2: LIMPIEZA Y SEGURIDAD", "src/limpieza.py")
    ejecutar_modulo("FASE 3: VALIDACIÓN", "src/validacion.py")
    ejecutar_modulo("FASE 4: CARGA", "src/carga.py")

    # 3. Fin del cronómetro
    end_time = time.time()
    latencia = end_time - start_time

    # 4. Cálculo del KPI de Completitud
    try:
        # Leemos el archivo original y el archivo validado final
        df_original = pd.read_csv("data/02_bank.csv")
        df_final = pd.read_csv("data/banco_validado.csv") 
        
        completitud = (len(df_final) / len(df_original)) * 100
        
        print("\n==================================================")
        print("📊 REPORTE DE KPIs DE MONITOREO (DATAOPS)")
        print("==================================================")
        print(f"⏱️ KPI Latencia    : {latencia:.2f} segundos en procesar el pipeline.")
        print(f"📈 KPI Completitud : {completitud:.2f}% de los datos sobrevivieron.")
        print(f"   -> Registros iniciales : {len(df_original)}")
        print(f"   -> Registros finales   : {len(df_final)}")
        print("==================================================\n")
        
    except Exception as e:
        print(f"\n⚠️ Pipeline ejecutado, pero hubo un error al calcular KPIs: {e}")
