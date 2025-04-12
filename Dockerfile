FROM python:3.11-slim

#Instalar herramientas necesarias
RUN apt update -y && \
    apt install -y \
    unzip \
    libaio1 \
    curl

#Descargar version reducida cliente oracle
WORKDIR /opt/oracle

RUN curl -o oracleclientlite.zip https://download.oracle.com/otn_software/linux/instantclient/2370000/instantclient-basiclite-linux.x64-23.7.0.25.01.zip && \
    unzip oracleclientlite.zip && \
    sh -c "echo /opt/oracle/instantclient_23_7 > \
    /etc/ld.so.conf.d/oracle-instantclient.conf" && \
    ldconfig && \
    rm oracleclientlite.zip

#Eliminar herramientas que no se utilizan
RUN apt remove --purge -y \
    unzip \
    curl && \
    apt autoremove -y

#Copiar carpetas necesarias para que funcione TNSPING
WORKDIR /opt/oracle/instantclient_23_7

COPY oracle/instantclient_23_7/network ./network
COPY oracle/instantclient_23_7/tnsping ./tnsping

ENV ORACLE_BASE=/opt/oracle
ENV ORACLE_HOME=${ORACLE_BASE}/instantclient_23_7
ENV PATH=$ORACLE_HOME:$PATH
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME 
ENV TNS_ADMIN=${ORACLE_HOME}/network/admin

WORKDIR /home/proceso

COPY proceso .

RUN pip install --no-cache-dir -r app/requirements.txt 

# Exponer el puerto usado por Streamlit
ENV APP_PORT=8501
EXPOSE $APP_PORT

ENV LOG_FILE=/var/log/proceso.log
ENV BASEURLPATH=informetnsping

ENV MAX_SIZE_MB=100
ENV PORCENT_KEEP_LINE_SIZE=10

# Definir el nombre del servicio Oracle a testear
ENV LISTA_HOST=HOST:PUERTO/INSTANCIA
ENV TIEMPO_PAUSA="3"

CMD [ "sh", "test-host.sh"]