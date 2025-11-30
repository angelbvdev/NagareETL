import os
import json
import random
import uuid
from datetime import datetime
import pandas as pd
from flask import Blueprint, render_template, jsonify

main = Blueprint('main', __name__)

# Rutas absolutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BRONZE_DIR = os.path.join(BASE_DIR, 'data_lake', 'bronze')
SILVER_DIR = os.path.join(BASE_DIR, 'data_lake', 'silver')
GOLD_DIR = os.path.join(BASE_DIR, 'data_lake', 'gold') # Aunque no guardemos ficheros aquí, es bueno tener la ref

# Crear directorios
for d in [BRONZE_DIR, SILVER_DIR, GOLD_DIR]:
    os.makedirs(d, exist_ok=True)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/generate', methods=['POST'])
def generate_data():
    """Genera datos en Bronze"""
    try:
        venta = {
            "transaction_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "store": random.choice(["Tokyo-Shibuya", "Osaka-Namba", "Kyoto-Station"]),
            "product": random.choice(["Katana Decorativa", "Manga Set", "Ramen Bowl", "Pocky Pack"]),
            "amount": round(random.uniform(10.0, 200.0), 2),
            "status": random.choice(["COMPLETED", "COMPLETED", "COMPLETED", "ERROR", None]) 
        }
        
        filename = f"sales_{datetime.now().strftime('%H%M%S_%f')}.json"
        filepath = os.path.join(BRONZE_DIR, filename)
        
        with open(filepath, 'w') as f:
            json.dump(venta, f, indent=4)
            
        count = len([n for n in os.listdir(BRONZE_DIR) if n.endswith('.json')])
        
        return jsonify({
            "success": True, 
            "filename": filename, 
            "data": venta,
            "total_files": count
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/run-etl', methods=['POST'])
def run_etl():
    """Motor ETL con Auto-Limpieza (Garbage Collection)"""
    logs = []
    processed_count = 0
    total_sales_batch = 0
    
    files = [f for f in os.listdir(BRONZE_DIR) if f.endswith('.json')]
    
    if not files:
        return jsonify({"logs": ["WARN: No hay archivos en Bronze para procesar."], "stats": None})

    data_batch = []
    
    # 1. EXTRACT & TRANSFORM (Bronze -> Memory)
    logs.append(f"INFO: Procesando {len(files)} archivos de Bronze...")
    
    for file in files:
        file_path = os.path.join(BRONZE_DIR, file)
        try:
            with open(file_path, 'r') as f:
                record = json.load(f)
            
            # Regla de Calidad
            if record.get('status') != 'COMPLETED':
                logs.append(f"WARN: ID {record['transaction_id'][:8]}... DESCARTADO (Data Quality).")
            else:
                record['processed_at'] = datetime.now().isoformat()
                data_batch.append(record)
                processed_count += 1
            
            # Borrar de Bronze (Ingesta completada)
            os.remove(file_path)
            
        except Exception as e:
            logs.append(f"ERROR: Fallo al leer {file}: {str(e)}")

    # 2. LOAD & AGGREGATE (Memory -> Silver -> Gold Metrics)
    if data_batch:
        # Guardar temporalmente en Silver (para simular escritura en disco)
        df = pd.DataFrame(data_batch)
        silver_filename = f"batch_{datetime.now().strftime('%H%M%S')}.json"
        silver_path = os.path.join(SILVER_DIR, silver_filename)
        
        df.to_json(silver_path, orient='records')
        logs.append(f"SUCCESS: Lote guardado en Silver ({processed_count} registros).")
        
        # Calcular métricas para Gold
        total_sales_batch = df['amount'].sum()
        logs.append(f"INFO: Métricas calculadas. Ventas del lote: ${total_sales_batch}")

        # --- FASE 3: GARBAGE COLLECTION (LIMPIEZA) ---
        # Aquí borramos los archivos de Silver para no llenar el disco
        try:
            os.remove(silver_path)
            logs.append(f"INFO: [Garbage Collector] Archivo temporal {silver_filename} eliminado.")
        except Exception as e:
            logs.append(f"ERROR: No se pudo limpiar archivo temporal: {str(e)}")
            
    else:
        logs.append("INFO: Ningún archivo pasó los filtros de calidad.")

    return jsonify({
        "logs": logs,
        "metrics": {
            "processed": processed_count,
            "sales_added": total_sales_batch
        }
    })