import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Álgebra Lineal", layout="wide")
st.title("📊 Análisis de Google Sheets")

# Diccionario de hojas con URL CSV
sheets_urls = {
    "Registro de alumnos": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRYSDhkiKuFdP62wR2aywuIa1GDfugqUFZ9BHR66YvJPTIH0bXAAustRHNo1KtSJIMDMeuHSDawdv87/pub?gid=1047557526&single=true&output=csv",
    "Registro de asistencia": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRYSDhkiKuFdP62wR2aywuIa1GDfugqUFZ9BHR66YvJPTIH0bXAAustRHNo1KtSJIMDMeuHSDawdv87/pub?gid=160302779&single=true&output=csv",
    "Tareas y exámenes semanales": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRYSDhkiKuFdP62wR2aywuIa1GDfugqUFZ9BHR66YvJPTIH0bXAAustRHNo1KtSJIMDMeuHSDawdv87/pub?gid=1850795541&single=true&output=csv",
    "Examen diagnóstico": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRYSDhkiKuFdP62wR2aywuIa1GDfugqUFZ9BHR66YvJPTIH0bXAAustRHNo1KtSJIMDMeuHSDawdv87/pub?gid=290705130&single=true&output=csv",
    "Examen Semanal 01": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRYSDhkiKuFdP62wR2aywuIa1GDfugqUFZ9BHR66YvJPTIH0bXAAustRHNo1KtSJIMDMeuHSDawdv87/pub?gid=1368627497&single=true&output=csv",
    "Examen Semanal 02": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRYSDhkiKuFdP62wR2aywuIa1GDfugqUFZ9BHR66YvJPTIH0bXAAustRHNo1KtSJIMDMeuHSDawdv87/pub?gid=342872313&single=true&output=csv",
    "Examen Semanal 03": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRYSDhkiKuFdP62wR2aywuIa1GDfugqUFZ9BHR66YvJPTIH0bXAAustRHNo1KtSJIMDMeuHSDawdv87/pub?gid=1532672592&single=true&output=csv",
    "Examen Semanal 04": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRYSDhkiKuFdP62wR2aywuIa1GDfugqUFZ9BHR66YvJPTIH0bXAAustRHNo1KtSJIMDMeuHSDawdv87/pub?gid=1417956644&single=true&output=csv",
    "Evaluacion Final": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRYSDhkiKuFdP62wR2aywuIa1GDfugqUFZ9BHR66YvJPTIH0bXAAustRHNo1KtSJIMDMeuHSDawdv87/pub?gid=0&single=true&output=csv",
    "Ejercicios": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRYSDhkiKuFdP62wR2aywuIa1GDfugqUFZ9BHR66YvJPTIH0bXAAustRHNo1KtSJIMDMeuHSDawdv87/pub?gid=1976006833&single=true&output=csv",
    "Examen extraordinario": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRYSDhkiKuFdP62wR2aywuIa1GDfugqUFZ9BHR66YvJPTIH0bXAAustRHNo1KtSJIMDMeuHSDawdv87/pub?gid=1455297344&single=true&output=csv"
}

# Función global para graficar puntajes
def graficar_puntaje(df, examen):
    st.subheader(f"📊 Puntajes - {examen}")

    correo_col = next((col for col in df.columns if "correo" in col.lower()), None)
    puntaje_col = next((col for col in df.columns if "punt" in col.lower() or "calific" in col.lower()), None)

    if correo_col and puntaje_col:
        df[puntaje_col] = df[puntaje_col].astype(str).str.extract(r"(\d+)").astype(float)
        df = df.dropna(subset=[correo_col, puntaje_col])

        if df.empty:
            st.warning("No hay puntajes válidos para graficar.")
            return

        fig, ax = plt.subplots(figsize=(10, 4))
        df.set_index(correo_col)[puntaje_col].plot(kind="bar", ax=ax, color="orchid")
        plt.xticks(rotation=90)
        st.pyplot(fig)

        st.markdown("**Estadísticas generales:**")
        st.write(f"Promedio: {df[puntaje_col].mean():.2f}")
        st.write(f"Máximo: {df[puntaje_col].max():.2f}")
        st.write(f"Mínimo: {df[puntaje_col].min():.2f}")

        fig_hist, ax_hist = plt.subplots()
        df[puntaje_col].plot(kind="hist", bins=10, ax=ax_hist, color="plum")
        ax_hist.set_title("Distribución de puntajes")
        st.pyplot(fig_hist)

# Menú lateral y carga de datos
seleccion = st.sidebar.selectbox("Selecciona hoja a visualizar", list(sheets_urls.keys()))
df = pd.read_csv(sheets_urls[seleccion])

# Visualizaciones por hoja seleccionada
if seleccion == "Registro de alumnos":
    st.subheader("📋 Registro de alumnos")
    st.dataframe(df)

    # 👇 Tipo de correo (por dominio)
    correo_col = next((col for col in df.columns if "correo" in col.lower()), None)
    if correo_col:
        dominios = df[correo_col].dropna().astype(str).str.extract(r'@([\w\.]+)')[0]
        conteo_dominios = dominios.value_counts()
        st.markdown("**📧 Tipo de correo utilizado:**")
        fig1, ax1 = plt.subplots()
        conteo_dominios.plot(kind="bar", ax=ax1, color="skyblue")
        ax1.set_ylabel("Cantidad")
        ax1.set_title("Distribución por dominio de correo")
        plt.xticks(rotation=45)
        st.pyplot(fig1)

    # 👇 Cursó o no cursó la materia
    cursado_col = next((col for col in df.columns if "curs" in col.lower()), None)
    if cursado_col:
        conteo_curso = df[cursado_col].value_counts()
        st.markdown("**📘 ¿Ya cursó la materia?:**")
        fig2, ax2 = plt.subplots()
        conteo_curso.plot(kind="bar", ax=ax2, color="salmon")
        ax2.set_ylabel("Cantidad")
        ax2.set_title("Distribución de alumnos según si ya cursaron la materia")
        plt.xticks(rotation=0)
        st.pyplot(fig2)

elif seleccion == "Registro de asistencia":
    st.subheader("📋 Registro de asistencia")
    st.dataframe(df)
    correo_col = [col for col in df.columns if "correo" in col.lower()]
    if correo_col:
        asistencia = df[correo_col[0]].value_counts()
        fig, ax = plt.subplots(figsize=(10,4))
        asistencia.plot(kind="bar", ax=ax, color='green')
        plt.xticks(rotation=90)
        st.pyplot(fig)

elif seleccion == "Tareas y exámenes semanales":
    st.subheader("📋 Tareas y exámenes")
    st.dataframe(df)

elif seleccion == "Ejercicios":
    st.subheader("📋 Ejercicios entregados")
    st.dataframe(df)
    correo_col = next((col for col in df.columns if "correo" in col.lower()), None)
    if correo_col:
        entregas = df[correo_col].value_counts()
        fig, ax = plt.subplots(figsize=(10,4))
        entregas.plot(kind="bar", ax=ax, color='dodgerblue')
        plt.xticks(rotation=90)
        st.pyplot(fig)

elif seleccion == "Evaluacion Final":
    st.subheader("📋 Evaluación Final")
    st.dataframe(df)
    graficar_puntaje(df, seleccion)

elif seleccion == "Examen diagnóstico":
    st.subheader("📋 Examen diagnóstico")
    st.dataframe(df)
    graficar_puntaje(df, seleccion)

elif seleccion.startswith("Examen Semanal") or "extraordinario" in seleccion.lower():
    st.subheader(f"📋 {seleccion}")
    st.dataframe(df)
    graficar_puntaje(df, seleccion)
