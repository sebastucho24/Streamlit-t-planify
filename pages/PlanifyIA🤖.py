import streamlit as st
import pandas as pd
import traceback
import os

# Configuración inicial
st.set_page_config(page_title="Planify Insights", layout="centered")
st.title("📅 Pregunta sobre los usuarios de Planify")
st.markdown("Haz preguntas sobre los datos de usuarios de Planify cargados desde el CSV.")

# Ruta correcta al CSV
csv_path = "dataset/planiffy_users.csv"

# Cargar datos del CSV
try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    st.error(f"No se encontró el archivo en: {csv_path}")
    st.stop()
except Exception as e:
    st.error(f"Error al cargar el CSV: {e}")
    st.stop()

# Botón para mostrar/ocultar la vista previa de los datos
if st.button("Mostrar vista previa de los usuarios"):
    st.subheader("📄 Vista previa de los usuarios")
    st.dataframe(df)

# Entrada del usuario
st.title("🤖 Hola, ¡Soy PlanifyIA!")
prompt = st.text_input("¿Qué deseas saber sobre los usuarios?", placeholder="Ej. ¿Cuántos usuarios premium hay?")
enviar = st.button("Generar Respuesta")

# Función para responder solo usando pandas y el CSV
def responder_con_csv(prompt, df):
    prompt_lower = prompt.lower()
    try:
        # Ejemplo de respuestas automáticas simples
        if "usuarios premium" in prompt_lower:
            count = (df['Subscription_Type'].str.lower() == "premium").sum()
            return f"Hay {count} usuarios con suscripción Premium."
        elif "usuarios por país" in prompt_lower or "usuarios en cada país" in prompt_lower:
            conteo = df['Country'].value_counts()
            return f"Usuarios por país:\n{conteo.to_string()}"
        elif "promedio de edad" in prompt_lower:
            avg = df['Age'].mean()
            return f"La edad promedio de los usuarios es {avg:.2f} años."
        elif "género favorito más popular" in prompt_lower or "género favorito" in prompt_lower:
            top = df['Favorite_Genre'].value_counts().idxmax()
            return f"El género favorito más popular es: {top}."
        elif "horas de visualización" in prompt_lower:
            avg = df['Watch_Time_Hours'].mean()
            return f"El promedio de horas de visualización es {avg:.2f} horas."
        elif "usuarios activos" in prompt_lower or "último inicio" in prompt_lower:
            df['Last_Login'] = pd.to_datetime(df['Last_Login'])
            recientes = df[df['Last_Login'] > pd.Timestamp.now() - pd.Timedelta(days=30)]
            return f"Usuarios activos en los últimos 30 días: {len(recientes)}"
        else:
            return (
                "Solo puedo responder preguntas relacionadas con los usuarios y datos de Planify "
                "que estén en el archivo CSV cargado. Por favor, realiza una consulta sobre los datos de Planify."
            )
    except Exception as e:
        return f"Error al analizar los datos: {e}"

# Procesar la respuesta
if enviar and prompt:
    with st.spinner("Analizando los datos y generando respuesta..."):
        respuesta = responder_con_csv(prompt, df)
        st.subheader("📌 Respuesta:")
        st.markdown(respuesta)
else:
    st.info("Haz una pregunta relacionada con los usuarios de Planify.")