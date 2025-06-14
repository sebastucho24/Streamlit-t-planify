import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Gráficas Interactivas de Usuarios", layout="wide")
st.title("📊 Panel de Gráficas Interactivas")

# Obtener datos de la API
@st.cache_data
def obtener_usuarios():
    try:
        respuesta = requests.get("http://localhost:3001/")
        respuesta.raise_for_status()
        data = respuesta.json()
        usuarios_dict = data.get("data", {}).get("usuarios", {})
        if isinstance(usuarios_dict, dict):
            usuarios = list(usuarios_dict.values())
        else:
            usuarios = usuarios_dict
        return usuarios
    except Exception as e:
        st.error(f"❌ Error al obtener los usuarios: {e}")
        return []

usuarios = obtener_usuarios()

if not usuarios:
    st.warning("No se encontraron usuarios registrados.")
    st.stop()

# Convertir a DataFrame
df = pd.DataFrame(usuarios)

# Procesar campos para gráficas
df['fecha_registro'] = pd.to_datetime(df['fecha_registro'])
df['num_proyectos'] = df['proyectos'].apply(lambda x: len(x) if isinstance(x, list) else 0)
df['tiene_proyectos'] = df['num_proyectos'] > 0

# Gráfica 1: Usuarios por tipo de cuenta
st.subheader("Distribución por tipo de cuenta")
fig1 = px.pie(df, names='tipo_cuenta', title='Usuarios por tipo de cuenta')
st.plotly_chart(fig1, use_container_width=True)

# Gráfica 2: Usuarios registrados por mes
st.subheader("Usuarios registrados por mes")
df['mes_registro'] = df['fecha_registro'].dt.to_period('M').astype(str)
registro_mes = df['mes_registro'].value_counts().sort_index().reset_index()
registro_mes.columns = ['Mes', 'Usuarios registrados']
fig2 = px.bar(registro_mes, x='Mes', y='Usuarios registrados', title='Usuarios registrados por mes')
st.plotly_chart(fig2, use_container_width=True)

# Gráfica 3: Número de proyectos por usuario
st.subheader("Distribución de proyectos por usuario")
fig3 = px.histogram(df, x='num_proyectos', nbins=10, title='Proyectos por usuario')
st.plotly_chart(fig3, use_container_width=True)

# Gráfica 4: Top 10 usuarios con más proyectos
st.subheader("Top 10 usuarios con más proyectos")
top_usuarios = df.nlargest(10, 'num_proyectos')[['nombre', 'num_proyectos']]
fig4 = px.bar(top_usuarios, x='nombre', y='num_proyectos', title='Top 10 usuarios con más proyectos')
st.plotly_chart(fig4, use_container_width=True)

# Gráfica 5: Proyectos por tipo de cuenta
st.subheader("Proyectos totales por tipo de cuenta")
proyectos_tipo = df.groupby('tipo_cuenta')['num_proyectos'].sum().reset_index()
fig5 = px.bar(proyectos_tipo, x='tipo_cuenta', y='num_proyectos', title='Proyectos por tipo de cuenta')
st.plotly_chart(fig5, use_container_width=True)

# Gráfica 6: Usuarios con y sin proyectos
st.subheader("Usuarios con y sin proyectos")
tiene_proyectos_count = df['tiene_proyectos'].value_counts().reset_index()
tiene_proyectos_count.columns = ['¿Tiene proyectos?', 'Cantidad']
fig6 = px.pie(tiene_proyectos_count, names='¿Tiene proyectos?', values='Cantidad', title='Usuarios con/sin proyectos')
st.plotly_chart(fig6, use_container_width=True)

# Gráfica 7: Proyectos activos vs inactivos (si hay campo 'estado' en proyectos)
proyectos = []
for usuario in usuarios:
    for proyecto in usuario.get('proyectos', []):
        proyectos.append({
            'usuario': usuario['nombre'],
            'estado': proyecto.get('estado', 'desconocido'),
            'nombre': proyecto.get('nombre', 'Sin nombre')
        })
if proyectos:
    df_proy = pd.DataFrame(proyectos)
    st.subheader("Estados de los proyectos")
    fig7 = px.histogram(df_proy, x='estado', color='estado', title='Proyectos por estado')
    st.plotly_chart(fig7, use_container_width=True)

# Gráfica 8: Cantidad de tareas por usuario (si hay tareas)
tareas_usuario = []
for usuario in usuarios:
    total_tareas = 0
    for proyecto in usuario.get('proyectos', []):
        total_tareas += len(proyecto.get('tareas', []))
    tareas_usuario.append({'usuario': usuario['nombre'], 'tareas': total_tareas})
df_tareas = pd.DataFrame(tareas_usuario)
st.subheader("Cantidad de tareas por usuario")
fig8 = px.bar(df_tareas, x='usuario', y='tareas', title='Tareas por usuario')
st.plotly_chart(fig8, use_container_width=True)

st.info("Puedes interactuar con las gráficas para explorar los datos.")