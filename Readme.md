# Objetivo General #
Generar una imagen Docker con las herramientas necesarias para conexión y pruebas a base de datos Oracle.

# Objetivo Principal #
Verificar tiempo de respuesta de conexion a base de datos Oracle mediante herramienta TNSPING.

## Metodo trabajo ##

### Obtener herramientas necesarias ###
Para conseguir el objetivo principal, se instala el instant client de oracle version 23.7 + SQLPLUS.
Esta versión de SQLPLUS posee comando PING el cual puede ser utilizado para el objetivo principal, pero posee una gran desventaja ya que debemos que conectarnos a la base de datos para ejecutar el comando.

https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html

Por otra parte entre las herramientas de instant client no se encuentra el TSNPING, por lo que se tuvo que extraer de la imagen gratuita de base de datos esta herramienta, mas carpetas necesarias para que funcione.

Docker Image: container-registry.oracle.com/database/free:latest

Ver carpeta "oracle", se pueden incluir mas herramientas pero la imagen llega a pesar alrededor de 1.5GB, evaluar para que se necesita y dejar lo mas liviano posible.

### Automatizar consulta de host ###
Para automatizar comando TNSPING a distintos HOST, se genera una shell que toma la lista de host informadas en variable LISTA_HOST, se espera string con formato HOST:PUERTO/INSTANCIA, para enviar mas de un host separar con espacio la lista. Adicionalmente se incluye atributo TIEMPO_ESPERA para que luego de recorrer la lista de HOST se espere un tiempo X.

Ver carpeta "proceso".

### Opcion uso desde Kubernetes ###
Se genera un script para desplegar en un cluster de kubernetes, con el objetivo de medir el tiempo de respuesta de las conexiones.

Ver carpeta "k8s".

## Imagen Docker ##
Para generar la imagen docker se hizo pruebas con distintas distros linux persiguiendo la imagen mas liviana, se opto por debian-slim-stable, igualmente se dejan las distintas pruebas realizadas y otros enfoques para lograr.

Ver carpeta "bkp".