import streamlit as st
import requests
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Panel de Usuarios - Admin/Consultor", layout="wide")

# Rol del usuario
rol = st.sidebar.selectbox("Selecciona tu rol:", ["Administrador", "Consultor"])
st.title(f"🔐 Panel de Gestión - Rol: {rol}")

# Función para obtener los usuarios desde la API
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

# Solo filtro por nombre
filtro_nombre = st.text_input("🔍 Buscar por nombre:").lower()

usuarios_filtrados = [
    u for u in usuarios
    if filtro_nombre in u['nombre'].lower()
]

st.subheader("📄 Resultados")
for usuario in usuarios_filtrados:
    with st.expander(f"👤 {usuario['nombre']} ({usuario['email']})"):
        st.markdown(f"""
        - **ID:** {usuario.get('id')}
        - **Tipo de cuenta:** {usuario.get('tipo_cuenta')}
        - **Fecha de registro:** {usuario.get('fecha_registro')}
        - **Proyectos registrados:** {len(usuario.get('proyectos', []))}
        """)
        proyectos = usuario.get("proyectos", [])
        st.markdown("### 📁 Proyectos:")
        if proyectos:
            for idx, proyecto in enumerate(proyectos):
                st.markdown(f"""
                - **Nombre:** {proyecto.get('nombre')} ({proyecto.get('estado')})
                - **Descripción:** {proyecto.get('descripcion')}
                - **Fecha de creación:** {proyecto.get('fecha_creacion')}
                """)
                tareas = proyecto.get("tareas", [])
                # Interruptor para mostrar tareas
                mostrar_tareas = st.toggle(f"Ver tareas de '{proyecto.get('nombre')}'", key=f"tareas_{usuario.get('id')}_{idx}")
                if mostrar_tareas and tareas:
                    st.markdown("#### 📋 Tareas:")
                    for t in tareas:
                        with st.container():
                            st.markdown(f"""
                            - **Título:** {t.get('titulo')}
                            - **Descripción:** {t.get('descripcion')}
                            - **Inicio:** {t.get('fecha_inicio')}
                            - **Fin:** {t.get('fecha_fin')}
                            - **Estado:** {t.get('estado')}
                            - **Prioridad:** {t.get('prioridad')}
                            """)
                            st.markdown("---")
                elif mostrar_tareas and not tareas:
                    st.info("Este proyecto no tiene tareas.")
        else:
            st.info("Este usuario no tiene proyectos.")

        # Botón para mostrar resumen en gráficas (dentro del usuario)
        if st.button(f"Mostrar resumen en gráficas de {usuario['nombre']}", key=f"graf_{usuario.get('id')}"):
            proyectos = usuario.get("proyectos", [])
            if proyectos:
                # Gráfica 1: Proyectos por estado
                estados = [p.get('estado', 'Sin estado') for p in proyectos]
                fig1 = px.histogram(x=estados, labels={'x': 'Estado del Proyecto', 'y': 'Cantidad'}, title="Proyectos por estado")
                st.plotly_chart(fig1, use_container_width=True)

                # Gráfica 2: Cantidad de tareas por proyecto
                proyectos_nombres = [p.get('nombre', 'Sin nombre') for p in proyectos]
                tareas_cant = [len(p.get('tareas', [])) for p in proyectos]
                fig2 = px.bar(x=proyectos_nombres, y=tareas_cant, labels={'x': 'Proyecto', 'y': 'Cantidad de tareas'}, title="Tareas por proyecto")
                st.plotly_chart(fig2, use_container_width=True)

                # Gráfica 3: Tareas por estado (si hay tareas)
                tareas = []
                for p in proyectos:
                    for t in p.get('tareas', []):
                        tareas.append(t)
                if tareas:
                    estados_tareas = [t.get('estado', 'Sin estado') for t in tareas]
                    fig3 = px.histogram(x=estados_tareas, labels={'x': 'Estado de la tarea', 'y': 'Cantidad'}, title="Tareas por estado")
                    st.plotly_chart(fig3, use_container_width=True)

                    # Gráfica 4: Tareas por prioridad
                    prioridades = [t.get('prioridad', 'Sin prioridad') for t in tareas]
                    fig4 = px.pie(names=prioridades, title="Distribución de tareas por prioridad")
                    st.plotly_chart(fig4, use_container_width=True)

                    # Gráfica 5: Tareas por fecha de inicio (línea de tiempo)
                    fechas_inicio = [t.get('fecha_inicio') for t in tareas if t.get('fecha_inicio')]
                    if fechas_inicio:
                        fechas_inicio = [datetime.strptime(f, "%Y-%m-%d") for f in fechas_inicio]
                        fechas_inicio_df = px.histogram(x=fechas_inicio, nbins=10, labels={'x': 'Fecha de inicio', 'y': 'Cantidad'}, title="Tareas por fecha de inicio")
                        st.plotly_chart(fechas_inicio_df, use_container_width=True)

                    # Gráfica 6: Tareas por fecha de fin (línea de tiempo)
                    fechas_fin = [t.get('fecha_fin') for t in tareas if t.get('fecha_fin')]
                    if fechas_fin:
                        fechas_fin = [datetime.strptime(f, "%Y-%m-%d") for f in fechas_fin]
                        fechas_fin_df = px.histogram(x=fechas_fin, nbins=10, labels={'x': 'Fecha de fin', 'y': 'Cantidad'}, title="Tareas por fecha de fin")
                        st.plotly_chart(fechas_fin_df, use_container_width=True)

                else:
                    st.info("No hay tareas para mostrar en gráficas.")

                # Gráfica 7: Proyectos por año de creación
                fechas_proy = [p.get('fecha_creacion') for p in proyectos if p.get('fecha_creacion')]
                if fechas_proy:
                    anios = [datetime.strptime(f, "%Y-%m-%d").year for f in fechas_proy]
                    fig5 = px.histogram(x=anios, labels={'x': 'Año de creación', 'y': 'Proyectos'}, title="Proyectos por año de creación")
                    st.plotly_chart(fig5, use_container_width=True)

            else:
                st.info("No hay proyectos para mostrar en gráficas.")

if not usuarios_filtrados:
    st.warning("No se encontraron usuarios que coincidan con la búsqueda.")
