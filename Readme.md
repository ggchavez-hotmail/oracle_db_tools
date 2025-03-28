# Objetivo General #

Construir una imagen Docker que incluya todas las herramientas necesarias para realizar pruebas de conexión y medir el tiempo de respuesta a una base de datos Oracle.

---

# Objetivo Principal #

Verificar el tiempo de respuesta de la conexión a una base de datos Oracle utilizando la herramienta TNSPING.

---

# Metodología #

### 1. Instalación de Herramientas ##

Para alcanzar el objetivo principal, se instala el **Oracle Instant Client** versión 23.7 junto con **SQL*Plus**. Esta versión de SQL*Plus incluye el comando `PING`, que permite realizar pruebas de conectividad. Sin embargo, presenta la desventaja de requerir conexión a la base de datos para ejecutar el comando.

Más información y descargas en:  
[Oracle Instant Client Downloads](https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html)

Dado que el Instant Client no incluye la herramienta **TNSPING**, se extrajo de la imagen gratuita de base de datos de Oracle, junto con las carpetas necesarias para su funcionamiento.

- **Imagen Docker utilizada:** `container-registry.oracle.com/database/free:latest`

Dentro de la carpeta `oracle` se pueden encontrar el detalla de los archivos utilizados. Tras evaluar distintas opciones y considerando el tamaño final de la imagen (alrededor de 1.5GB), se optó por incluir únicamente el **Instant Client Lite** y **TNSPING**.

---

### 2. Automatización de la Consulta de Hosts ###

Se creó un script shell que automatiza la ejecución del comando **TNSPING** para múltiples hosts.  
- La lista de hosts se define en la variable `LISTA_HOST` con el formato `HOST:PUERTO/INSTANCIA`.
- Para incluir más de un host, se deben separar con espacios.  
- Además, se incluye un parámetro `TIEMPO_ESPERA` que especifica el tiempo de espera una vez que se ha recorrido la lista de hosts.

Consulta el contenido en la carpeta `proceso`.

---

### 3. Uso desde Kubernetes ###

Se ha desarrollado un script para desplegar la solución en un clúster de Kubernetes. Esto permite medir el tiempo de respuesta de las conexiones en un entorno distribuido y escalable.

Consulta la carpeta `k8s` para más detalles.

---

## Imagen Docker ##

Se realizaron pruebas con diversas distribuciones Linux buscando obtener una imagen lo más liviana posible. Se optó por utilizar **debian-slim-stable**.  
En la carpeta `bkp` se encuentran los diferentes enfoques y pruebas realizadas durante el desarrollo.

---

Esta documentación resume el proceso para construir y utilizar la imagen Docker destinada a la conexión y pruebas a base de datos Oracle. Si tienes alguna duda o sugerencia, por favor abre un issue o envía un pull request.

---
