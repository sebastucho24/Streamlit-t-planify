import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://localhost:3001/users"  # Ajusta si usas otro puerto

@st.cache_data
def get_usuarios():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error al cargar usuarios")
        return []

usuarios = get_usuarios()

st.title("📅 Planificador de Proyectos (tipo Planify)")

# FILTRO 1: Buscar usuario por nombre
busqueda_usuario = st.text_input("🔎 Buscar usuario por nombre")

usuarios_filtrados = [u for u in usuarios if busqueda_usuario.lower() in u["nombre"].lower()]
usuario_nombres = [f"{u['id']}: {u['nombre']}" for u in usuarios_filtrados]

if not usuario_nombres:
    st.warning("No se encontraron usuarios.")
    st.stop()

usuario_seleccionado = st.selectbox("Selecciona un usuario", usuario_nombres)
usuario = next((u for u in usuarios if f"{u['id']}: {u['nombre']}" == usuario_seleccionado), None)

if usuario:
    st.subheader(f"Planes de {usuario['nombre']}")

    # FILTRO 2: Buscar planes por palabra clave
    filtro_planes = st.text_input("🔍 Filtrar planes por título o descripción")

    planes = [
        p for p in usuario["planes"]
        if filtro_planes.lower() in p["titulo"].lower() or filtro_planes.lower() in p["descripcion"].lower()
    ]

    # FILTRO 3: Estado de tarea
    estado_tarea = st.selectbox("🧩 Filtrar tareas por estado", ["Todos", "pendiente", "completado"])

    if planes:
        for plan in planes:
            with st.expander(f"📁 {plan['titulo']}"):
                st.write(plan["descripcion"])
                for tarea in plan["tareas"]:
                    if estado_tarea == "Todos" or tarea["estado"] == estado_tarea:
                        st.checkbox(
                            f"📝 {tarea['titulo']} - {tarea['estado']}",
                            value=tarea["estado"] == "completado",
                            disabled=True
                        )
    else:
        st.info("Este usuario no tiene planes que coincidan con los filtros.")

    st.divider()

    # AGREGAR PLAN
    st.subheader("➕ Agregar nuevo plan")
    titulo_plan = st.text_input("Título del plan")
    descripcion_plan = st.text_area("Descripción del plan")

    if st.button("Agregar Plan"):
        if titulo_plan:
            nuevo_plan = {
                "id": 9999,
                "titulo": titulo_plan,
                "descripcion": descripcion_plan,
                "tareas": []
            }
            usuario["planes"].append(nuevo_plan)
            st.success(f"Plan '{titulo_plan}' agregado.")

    st.divider()

    # AGREGAR TAREA
    if usuario["planes"]:
        st.subheader("📝 Agregar tarea a un plan")
        plan_seleccionado = st.selectbox("Selecciona un plan", [p["titulo"] for p in usuario["planes"]])
        tarea_titulo = st.text_input("Título de la tarea")
        tarea_estado = st.selectbox("Estado", ["pendiente", "completado"])

        if st.button("Agregar Tarea"):
            for plan in usuario["planes"]:
                if plan["titulo"] == plan_seleccionado:
                    nueva_tarea = {
                        "id": 9999,
                        "titulo": tarea_titulo,
                        "estado": tarea_estado
                    }
                    plan["tareas"].append(nueva_tarea)
                    st.success(f"Tarea '{tarea_titulo}' agregada al plan '{plan_seleccionado}'.")



    # Gráfica de pastel con los planes creados
    if usuario["planes"]:
        st.subheader("🥧 Distribución de Planes creados")
        df_planes = pd.DataFrame({"Planes": [p["titulo"] for p in usuario["planes"]]})
        conteo_planes = df_planes["Planes"].value_counts().reset_index()
        conteo_planes.columns = ["Plan", "Cantidad"]

        fig_pie = px.pie(conteo_planes, names="Plan", values="Cantidad", title="Planes creados por usuario")
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No hay planes creados para mostrar en la gráfica de pastel.")
