import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import os

from data_processor import read_log_file

# Ruta del archivo de log (asegúrate de que 'logfile.log' esté en el directorio)
LOG_FILE = os.getenv("LOG_FILE", default="/var/log/proceso.log")

# Función con caché (expira en 5 minutos o al presionar el botón)
@st.cache_data(ttl=300)
def get_cached_data():
    return read_log_file(LOG_FILE)


# Cargar datos (desde caché o archivo si expiró)
df = get_cached_data()
              

# Si el DataFrame está vacío, mostrar mensaje y salir
if df.empty:
    st.error("No se encontraron datos en el archivo de log.")
    st.stop()
    

# Asegurar que 'timestamp' es de tipo datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Obtener valores mínimo y máximo del timestamp
min_timestamp = df["timestamp"].min()
max_timestamp = df["timestamp"].max()

# Selección de rango de fecha y hora (en 10 grupos)
num_partitions = 10
partition_labels = np.linspace(min_timestamp.value, max_timestamp.value, num_partitions, dtype=np.int64)
partition_timestamps = [pd.Timestamp(ts) for ts in partition_labels]

# Botón para forzar la actualización
st.sidebar.header("Opciones de Datos")

st.sidebar.header("Filtrar por Rango de Fecha y Hora")
start_time, end_time = st.sidebar.select_slider(
    "Selecciona el rango de tiempo:",
    options=partition_timestamps,
    value=(partition_timestamps[0], partition_timestamps[-1]),
    format_func=lambda x: x.strftime("%Y-%m-%d %H:%M")
)

# 🔹 Filtro por "Host"
available_hosts = df["host_inst"].unique()
selected_hosts = st.sidebar.multiselect(
    "Selecciona los Hosts a visualizar:",
    options=available_hosts,
    default=available_hosts
)

# Filtrar datos según los parámetros seleccionados
filtered_df = df[
    (df["timestamp"] >= start_time) &
    (df["timestamp"] <= end_time) &
    (df["host_inst"].isin(selected_hosts))
]

# Si no hay datos en el rango seleccionado, mostrar mensaje
if filtered_df.empty:
    st.warning("No hay datos en el rango de fecha, hora o host seleccionado.")
else:
    # Reducir cantidad de puntos para evitar sobrecarga visual
    #sample_rate = max(1, len(filtered_df) // 100)  # Muestra cada N puntos si hay más de 100
    #sampled_df = filtered_df.iloc[::sample_rate]

    # 📊 Gráfico 1: Latencia por Host (Líneas + Puntos con colores optimizados)
    st.header("📈 Latencia por Host")
    fig1 = px.line(
        filtered_df, x="timestamp", y="exec_time", color="host_inst",
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Set1,  # 🎨 Paleta de colores con mayor contraste
        labels={"exec_time": "⏳ Tiempo de Ejecución (ms)", "timestamp": "📆 Timestamp"},
        hover_data={"timestamp": "|%Y-%m-%d %H:%M:%S", "exec_time": True, "host_inst": True},
        title="Latencias Generales por Host"
    )

    # 🔹 Mejorar diseño visual
    fig1.update_layout(
        xaxis_title="📆 Timestamp",
        yaxis_title="⏳ Tiempo de Ejecución (ms)",
        hovermode="x unified",
        template="plotly_white",
        legend=dict(title="Host", bgcolor="rgba(255,255,255,0.6)")  # Fondo semitransparente para la leyenda
    )

    st.plotly_chart(fig1, use_container_width=True)
    
    ##########################################################
    # Filtrar datos con latencia > 200 ms
    high_latency_df = filtered_df[filtered_df["exec_time"] > 200]
    
    # 📊 Gráfico 2: Latencias > 200 ms (Puntos)
    if not high_latency_df.empty:
        st.header("🚨 Latencias Altas (>200 ms)")

        fig2 = px.scatter(
            high_latency_df, x="timestamp", y="exec_time", color="host_inst",
            color_discrete_sequence=px.colors.qualitative.Dark24,  # 🎨 Paleta oscura para mayor contraste
            labels={"exec_time": "⏳ Tiempo de Ejecución (ms)", "timestamp": "📆 Timestamp"},
            hover_data={"timestamp": "|%Y-%m-%d %H:%M:%S", "exec_time": True, "host_inst": True},
            title="Distribución de Latencias Altas"
        )

        # 🔹 Mejorar diseño visual
        fig2.update_layout(
            xaxis_title="📆 Timestamp",
            yaxis_title="⏳ Tiempo de Ejecución (ms)",
            hovermode="x unified",
            template="plotly_white",
            legend=dict(title="Host", bgcolor="rgba(255,255,255,0.6)")
        )

        st.plotly_chart(fig2, use_container_width=True)
         
    else:
        st.success("✅ No hay latencias superiores a 200 ms en el rango seleccionado.")
    ##########################################################
    # 📊 Crear tabla de conteo de ocurrencias
    status_counts = filtered_df["status"].value_counts().reset_index()
    status_counts.columns = ["Estado", "Cantidad"]

    # 📊 Mostrar tabla en Streamlit
    st.header("📊 Análisis de Estados de Conexión")
    st.dataframe(status_counts, use_container_width=True)
    ##########################################################
    # 📌 Convertir el timestamp a formato datetime y establecer como índice
    filtered_df["timestamp"] = pd.to_datetime(filtered_df["timestamp"])
    filtered_df.set_index("timestamp", inplace=True)

    # 📌 Agrupar por intervalos de tiempo (ejemplo: cada 5 minutos) y calcular métricas
    time_stats_df = filtered_df.resample("5min").agg({
        "exec_time": ["median", lambda x: np.percentile(x, 90), lambda x: np.percentile(x, 95)]
    }).dropna()

    # Renombrar columnas
    time_stats_df.columns = ["Mediana", "Slowest 10%", "Slowest 5%"]
    time_stats_df = time_stats_df.reset_index()

    # 📊 Gráfico: Variación de la Mediana y Percentiles en el Tiempo
    st.header("📈 Variación de Mediana y Percentiles en el Tiempo")
    fig = px.line(
        time_stats_df, x="timestamp", y=["Mediana", "Slowest 10%", "Slowest 5%"],
        markers=True,
        title="Evolución de Mediana y Percentiles 90/95",
        labels={"timestamp": "📆 Tiempo", "value": "⏳ Tiempo de Ejecución (ms)"},
        template="plotly_white"
    )

    fig.update_traces(mode="lines+markers")  # Mostrar puntos sobre las líneas

    # 📌 Mejorar visualmente el gráfico
    fig.update_layout(
        xaxis_title="📆 Tiempo",
        yaxis_title="⏳ Tiempo de Ejecución (ms)",
        legend_title="Métrica",
        hovermode="x unified",
        legend=dict(bgcolor="rgba(255,255,255,0.6)")
    )

    st.plotly_chart(fig, use_container_width=True)

if st.sidebar.button("🔄 Refrescar Datos"):
    st.cache_data.clear()  # Borra caché manualmente
    st.rerun()
