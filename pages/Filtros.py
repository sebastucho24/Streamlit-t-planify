import streamlit as st
import pandas as pd
import random


df = pd.read_csv("dataset\planiffy_users.csv")  

st.subheader("🔹 Ejercicio 2: Filtro por Edad")
Age_min, Age_max = st.slider("Selecciona el rango de edad", 15, 75, (20, 40))
df_Age = df[df['Age'].between(Age_min, Age_max)]
st.write(df_Age)
Age_min = 18
Age_max = 30

st.subheader("🔹 Ejercicio 3: Filtro por Municipio")
Country = st.multiselect("Selecciona municipios", sorted(df['Country'].unique()))
df_Country = df[df['Country'].isin(Country)] if Country else df
st.write(df_Country)