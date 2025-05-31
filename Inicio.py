import streamlit as st
import base64
import os

# Configuración de la página
st.set_page_config(
    page_title="Nuevas Tecnologías de Programación",
    page_icon="💻",
    layout="wide"
)

# Estilos personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #003366;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #0066cc;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .stButton > button {
        background-color: #0066cc;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton > button:hover {
        background-color: #003366;
    }
</style>
""", unsafe_allow_html=True)

# Logo CESDE
def get_svg_logo():
    with open("assets/logo-Cesde-2023.svg", "r") as file:
        svg_content = file.read()
    svg_content = svg_content.replace('viewBox="0 0 264 53"', 'viewBox="0 0 264 53" width="300"')
    return svg_content

st.markdown(f"<div style='text-align: center; margin-bottom: 20px;'>{get_svg_logo()}</div>", unsafe_allow_html=True)

# Encabezados
st.markdown('<h1 class="main-header">PLANIFY</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="sub-header">Proyecto Integrador</h2>', unsafe_allow_html=True)

# Función para mostrar info de estudiante
def mostrar_estudiante(nombre, programa, semestre, repo_url, imagen_path):
    col1, col2 = st.columns([1, 2])
    with col1:
        if imagen_path and os.path.exists(imagen_path):
            st.image(imagen_path, width=200, caption=nombre or "Sin nombre", output_format="JPEG")
        else:
            # Imagen por defecto si no hay imagen personalizada
            st.image("assets/user-profile-icon-free-vector.jpg", width=200, caption=nombre or "Sin nombre", output_format="JPEG")
    with col2:
        st.markdown(f'<h3 style="color: #0066cc; margin-top: 0px;">{nombre or "Nombre no disponible"}</h3>', unsafe_allow_html=True)
        st.markdown(f'<p style="margin-top: 10px;">Programa: <span style="color: #0066cc; font-weight: bold;">{programa}</span></p>', unsafe_allow_html=True)
        st.markdown(f'<p>Semestre: <span style="color: #0066cc; font-weight: bold;">{semestre}</span></p>', unsafe_allow_html=True)
        st.markdown(f'<p>Repositorio: <a href="{repo_url}" target="_blank" style="color: #0066cc; font-weight: bold; text-decoration: none;">GitHub</a></p>', unsafe_allow_html=True)
    st.markdown("---")

# Lista de estudiantes
estudiantes = [
    {
        "nombre": "Juan Sebastian Correa",
        "programa": "Desarrollo de Software",
        "semestre": "2025-1 - III",
        "repo_url": "https://github.com/username/proyecto-ntp",
        "imagen_path": "assets/IMG_2044.jpg"
    },
    {
        "nombre": "Emanuel Martínez Valencia",
        "programa": "Desarrollo de Software",
        "semestre": "2025-1 - III",
        "repo_url": "https://github.com/laura/proyecto-ntp",
        "imagen_path": "assets/mtz.jpeg"
    },
    {
        "nombre": "Miguel Ángel Patiño Valencia",
        "programa": "Desarrollo de Software",
        "semestre": "2025-1 - III",
        "repo_url": "https://github.com/miguel/proyecto-ntp",
        "imagen_path": "assets/miguel.jpeg"
    },
    {
        "nombre": "Carlos",
        "programa": "Desarrollo de Software",
        "semestre": "2025-1 - III",
        "repo_url": "https://github.com/carlos/proyecto-ntp",
        "imagen_path": ""
    },
    {
        "nombre": "Stiven",
        "programa": "Desarrollo de Software",
        "semestre": "2025-1 - III",
        "repo_url": "https://github.com/ana/proyecto-ntp",
        "imagen_path": "assets/instasize_240620163131.jpg"
    }

]

# Mostrar todos los estudiantes
for estudiante in estudiantes:
    mostrar_estudiante(**estudiante)

# Pie de página
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    ©️ 2025 CESDE
</div>
""", unsafe_allow_html=True)