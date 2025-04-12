import json
import re
import pandas as pd
from datetime import datetime


def parse_log_line_especial(line):
    """
    Procesa una línea del archivo JSON y extrae:
      - timestamp: Formato 'YYYY-MM-DD HH:MM:SS'
      - host: La dirección y puerto del servicio
      - exec_time: Tiempo de respuesta en milisegundos (NN msec) o -1 si no está presente
    """
    try:
        
        # Regex para capturar campos
        pattern = r"host=(.*?);resultado=(.*?);timestamp=(.*)"

        match = re.match(pattern, line)
        if match:
            host = match.group(1).strip()
            resultado = match.group(2).strip()
            timestamp = match.group(3).strip()
            
            timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

            # Extraer el tiempo de ejecución desde 'resultado'
            time_match = re.search(r"OK\s*\((\d+)\s*msec\)", resultado)
            exec_time = int(time_match.group(1)) if time_match else -10
            status =  extract_result(resultado)
            
            return {"timestamp": timestamp, "host_inst": host, "exec_time": exec_time, "status" : status}
        else:
            return None
    
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"Error procesando línea: {line}\n{e}")
        return None
    
def parse_log_line(line):
    """
    Procesa una línea del archivo JSON y extrae:
      - timestamp: Formato 'YYYY-MM-DD HH:MM:SS'
      - host: La dirección y puerto del servicio
      - exec_time: Tiempo de respuesta en milisegundos (NN msec) o -1 si no está presente
    """
    try:
        log_entry = json.loads(line.strip())  # Convertir la línea en un diccionario
        timestamp = datetime.strptime(log_entry["timestamp"], "%Y-%m-%d %H:%M:%S")
        host = log_entry["host"]
        
        # Extraer el tiempo de ejecución desde 'resultado'
        time_match = re.search(r"OK\s*\((\d+)\s*msec\)", log_entry["resultado"])
        exec_time = int(time_match.group(1)) if time_match else -10
        status =  extract_result(log_entry["resultado"])
        
        return {"timestamp": timestamp, "host_inst": host, "exec_time": exec_time, "status" : status}
    
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"Error procesando línea: {line}\n{e}")
        return None
    
# Función para extraer resultado de cada registro
def extract_result(text):
    if "OK" in text:
        return "OK"
    elif "TNS-" in text:
        return text[text.find("TNS-"):]  # Extrae todo el mensaje desde "TNS-"
    return "Desconocido"

def read_log_file(file_path):
    """
    Lee el archivo de log JSON y devuelve un DataFrame con los registros procesados.
    """
    data = []
    try:
        with open(file_path, "r") as f:
            for line in f:
                #entry = parse_log_line(line)
                entry = parse_log_line_especial(line)
                if entry:
                    data.append(entry)
    except Exception as e:
        print(f"Error al leer el archivo de log: {e}")

    return pd.DataFrame(data)
