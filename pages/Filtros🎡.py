import streamlit as st
import pandas as pd

df = pd.read_csv("dataset\\planiffy_users.csv")  

st.subheader("🔹 Filtro por Edad")
Age_min, Age_max = st.slider("Selecciona el rango de edad", int(df['Age'].min()), int(df['Age'].max()), (20, 40))
df_Age = df[df['Age'].between(Age_min, Age_max)]
st.write(df_Age)

st.subheader("🔹 Filtro por País")
Country = st.multiselect("Selecciona países", sorted(df['Country'].unique()))
df_Country = df[df['Country'].isin(Country)] if Country else df
st.write(df_Country)

st.subheader("🔹 Filtro por Tipo de Suscripción")
plans = st.multiselect("Selecciona tipo(s) de suscripción", sorted(df['Subscription_Type'].unique()))
df_Subscription = df[df['Subscription_Type'].isin(plans)] if plans else df
st.write(df_Subscription)

st.subheader("🔹 Filtro por Género Favorito")
genres = st.multiselect("Selecciona género(s) favorito(s)", sorted(df['Favorite_Genre'].unique()))
df_genre = df[df['Favorite_Genre'].isin(genres)] if genres else df
st.write(df_genre)

st.subheader("🔹 Filtro por Horas de Visualización")
min_watch, max_watch = st.slider("Selecciona el rango de horas de visualización", 
                                 float(df['Watch_Time_Hours'].min()), 
                                 float(df['Watch_Time_Hours'].max()), 
                                 (float(df['Watch_Time_Hours'].min()), float(df['Watch_Time_Hours'].max())))
df_watch = df[df['Watch_Time_Hours'].between(min_watch, max_watch)]
st.write(df_watch)

st.subheader("🔹 Filtro por Último Inicio de Sesión")
df['Last_Login'] = pd.to_datetime(df['Last_Login'])
date_min = df['Last_Login'].min().date()
date_max = df['Last_Login'].max().date()
start_date, end_date = st.date_input("Selecciona rango de fechas de último login", [date_min, date_max])
df_login = df[(df['Last_Login'] >= pd.to_datetime(start_date)) & (df['Last_Login'] <= pd.to_datetime(end_date))]
st.write(df_login)

st.subheader("🔹 Filtro por Nombre")
names = st.multiselect("Selecciona nombre(s)", sorted(df['Name'].unique()))
df_names = df[df['Name'].isin(names)] if names else df
st.write(df_names)

st.subheader("🔹 Filtro por ID de Usuario")
user_ids = st.multiselect("Selecciona ID(s) de usuario", sorted(df['User_ID'].unique()))
df_ids = df[df['User_ID'].isin(user_ids)] if user_ids else df
st.write(df_ids)

st.subheader("🔹 Búsqueda por texto libre")
search = st.text_input("Buscar por nombre, país o género favorito:")
if search:
    df_search = df[
        df['Name'].str.contains(search, case=False) |
        df['Country'].str.contains(search, case=False) |
        df['Favorite_Genre'].str.contains(search, case=False)
    ]
    st.write(df_search)