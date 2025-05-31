import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Carga el dataset real
df = pd.read_csv("dataset/planiffy_users.csv")

# Asegúrate que la columna 'Last_Login' sea tipo fecha
df['Last_Login'] = pd.to_datetime(df['Last_Login'])

st.title("Análisis de usuarios Planiffy")

# Filtro de búsqueda por nombre (input de texto)
search_name = st.text_input("Buscar usuario por nombre (parcial o completo):").strip().lower()

# Filtro por tipo de plan
plan_types = df['Subscription_Type'].unique().tolist()
selected_plan = st.selectbox("Filtrar por tipo de plan:", options=["Todos"] + plan_types)

# Filtrar datos según búsqueda por nombre y tipo de plan
filtered_data = df.copy()

if search_name:
    filtered_data = filtered_data[filtered_data['Name'].str.lower().str.contains(search_name)]

if selected_plan != "Todos":
    filtered_data = filtered_data[filtered_data['Subscription_Type'] == selected_plan]

st.write(f"Mostrando {len(filtered_data)} usuario(s)")

if len(filtered_data) == 0:
    st.warning("No se encontraron usuarios que coincidan con los filtros.")
else:
    # Gráfica 1: Distribución de edades
    st.subheader("Distribución de Edades")
    fig1, ax1 = plt.subplots()
    ax1.hist(filtered_data['Age'], bins=10, color='skyblue', edgecolor='black')
    ax1.set_xlabel('Edad')
    ax1.set_ylabel('Cantidad de Usuarios')
    st.pyplot(fig1)

    # Gráfica 2: Usuarios por país (gráfico de barras)
    st.subheader("Usuarios por País")
    country_counts = filtered_data['Country'].value_counts()
    fig2 = px.bar(x=country_counts.index, y=country_counts.values, labels={'x':'País', 'y':'Número de Usuarios'}, color=country_counts.values, color_continuous_scale='Blues')
    st.plotly_chart(fig2)

    # Gráfica 3: Tipo de suscripción (gráfico circular)
    st.subheader("Distribución de Tipo de Suscripción")
    sub_counts = filtered_data['Subscription_Type'].value_counts()
    fig3 = px.pie(values=sub_counts.values, names=sub_counts.index, title="Tipos de suscripción")
    st.plotly_chart(fig3)

    # Gráfica 4: Tiempo de visualización por usuario (barras horizontales)
    st.subheader("Tiempo de Visualización por Usuario")
    fig4, ax4 = plt.subplots()
    ax4.barh(filtered_data['Name'], filtered_data['Watch_Time_Hours'], color='orange')
    ax4.set_xlabel('Horas de Visualización')
    ax4.set_ylabel('Usuario')
    st.pyplot(fig4)

    # Gráfica 5: Géneros favoritos (barras)
    st.subheader("Géneros Favoritos")
    genre_counts = filtered_data['Favorite_Genre'].value_counts()
    fig5 = px.bar(x=genre_counts.index, y=genre_counts.values, labels={'x':'Género', 'y':'Número de Usuarios'}, color=genre_counts.values, color_continuous_scale='Viridis')
    st.plotly_chart(fig5)
