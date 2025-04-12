#!/bin/bash

#calcular el maximo para generar
MAX_SIZE=$((MAX_SIZE_MB * 1024 * 1024))

# Bucle infinito
while true; do
    echo "---------------------------------------------------------------"
    #revisa lista de HOST
    for ORACLE_SERVICE in ${LISTA_HOST}
    do
        # Ejecutar tnsping y transformar la salida en una sola línea
        RESULT=$(tnsping "$ORACLE_SERVICE" | tr '\n' ' ')
        # Imprimir el número de ejecución y la salida del comando en una misma línea
        FECHA=$(date +"%Y-%m-%d %H:%M:%S")
        echo "{ \"timestamp\" : \"${FECHA}\", \"host\" : \"${ORACLE_SERVICE}\" , \"resultado\" : \"${RESULT}\" }" #spool
        echo "{ \"timestamp\" : \"${FECHA}\", \"host\" : \"${ORACLE_SERVICE}\" , \"resultado\" : \"${RESULT}\" }" >> ${LOG_FILE} #archivo
    done
    echo "----- Fin del ciclo. Esperando ${TIEMPO_PAUSA} segundo antes de repetir -----"
    RESULT=$(sleep ${TIEMPO_PAUSA}) # Pausa entre cada ejecución individual
    
    # Obtener el tamano actual del archivo
    FILE_SIZE=$(stat -c %s "${LOG_FILE}")

    # Si el tamano supera el limite, se trunca el archivo
    if [ "${FILE_SIZE}" -gt "${MAX_SIZE}" ]; then
        echo "El archivo ${LOG_FILE} ha superado los ${MAX_SIZE_MB}MB. Redimensionando..."

        # Calcular cuantas lineas deben conservarse
        ACTUAL_LINE_SIZE=$(wc -l < "${LOG_FILE}")
        LINES_TO_KEEP=$(((ACTUAL_LINE_SIZE * PORCENT_KEEP_LINE_SIZE) / 100))

        # Crear un archivo temporal con las ultimas líneas
        tail -n "${LINES_TO_KEEP}" "${LOG_FILE}" > "${LOG_FILE}.bkp"

        # Reemplazar el archivo original con la versión reducida
        mv "${LOG_FILE}.bkp" "${LOG_FILE}"

        echo "Archivo reducido a las ultimas ${LINES_TO_KEEP} lineas."
    fi
done