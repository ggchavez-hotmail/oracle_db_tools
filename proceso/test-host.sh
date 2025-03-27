#!/bin/bash

# Bucle infinito
while true; do
    echo "---------------------------------------------------------------"
    #revisa lista de HOST
    for ORACLE_SERVICE in ${LISTA_HOST}
    do
        # Ejecutar tnsping y transformar la salida en una sola línea
        RESULT=$(tnsping "$ORACLE_SERVICE" | tr '\n' ' ')
        # Imprimir el número de ejecución y la salida del comando en una misma línea
        echo "Ejecucion ${ORACLE_SERVICE}: ${RESULT}"
    done
    echo "----- Fin del ciclo. Esperando ${TIEMPO_PAUSA} segundo antes de repetir -----"
    RESULT=$(sleep ${TIEMPO_PAUSA}) # Pausa entre cada ejecución individual
done