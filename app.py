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

seleccion = st.sidebar.selectbox("Selecciona hoja a visualizar", list(sheets_urls.keys()))
df = pd.read_csv(sheets_urls[seleccion])

if seleccion == "Registro de alumnos":
    st.subheader("📋 Registro de alumnos")
    st.dataframe(df)

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

    # Detectar columna de correo en la hoja de asistencia
    correo_asistencia = next((col for col in df.columns if "correo" in col.lower()), None)

    if correo_asistencia:
        # Normalizar correos
        df[correo_asistencia] = df[correo_asistencia].astype(str).str.strip().str.lower()

        # Contar asistencias por correo
        conteo_asistencia = df[correo_asistencia].value_counts()

        # Graficar
        fig, ax = plt.subplots(figsize=(10,4))
        conteo_asistencia.plot(kind="bar", ax=ax, color='green')
        ax.set_title("Asistencia por correo")
        ax.set_xlabel("Correo")
        ax.set_ylabel("Número de asistencias")
        plt.xticks(rotation=90)
        st.pyplot(fig)

    else:
        st.error("No se encontró una columna de correos en el registro de asistencia.")


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

    df_alumnos = pd.read_csv(sheets_urls["Registro de alumnos"])
    col_correo = next((c for c in df_alumnos.columns if "correo" in c.lower()), None)
    col_nombre = next((c for c in df_alumnos.columns if "nombre" in c.lower()), None)

    df_alumnos["correo_match"] = df_alumnos[col_correo].astype(str).str.strip().str.lower()
    df_alumnos["nombre_normalizado"] = df_alumnos[col_nombre].astype(str).str.strip().str.lower()

    df_resultado = pd.DataFrame()
    df_resultado["Alumno"] = df_alumnos["nombre_normalizado"]
    df_resultado["Correo"] = df_alumnos["correo_match"]

    examenes_urls = {
        "Diagnóstico": sheets_urls["Examen diagnóstico"],
        "Sem.1": sheets_urls["Examen Semanal 01"],
        "Sem.2": sheets_urls["Examen Semanal 02"],
        "Sem.3": sheets_urls["Examen Semanal 03"],
        "Sem.4": sheets_urls["Examen Semanal 04"],
    }

    def extraer_puntajes_por_correo(url):
        df = pd.read_csv(url)
        correo_col = next((c for c in df.columns if "correo" in c.lower()), None)
        puntaje_col = next((c for c in df.columns if "punt" in c.lower() or "calif" in c.lower()), None)
        if not (correo_col and puntaje_col):
            return pd.DataFrame()
        df[correo_col] = df[correo_col].astype(str).str.strip().str.lower()
        df[puntaje_col] = df[puntaje_col].astype(str).str.extract(r"(\d+)").astype(float)
        df = df[[correo_col, puntaje_col]].drop_duplicates()
        df.columns = ["correo_match", "Puntaje"]
        return df

    for nombre_examen, url in examenes_urls.items():
        df_ex = extraer_puntajes_por_correo(url)
        if not df_ex.empty:
            df_merge = df_alumnos.merge(df_ex, on="correo_match", how="left")
            df_resultado[nombre_examen] = df_merge["Puntaje"]

    columnas_examenes_existentes = [col for col in examenes_urls.keys() if col in df_resultado.columns]
    if columnas_examenes_existentes:
        df_resultado["Promedio"] = df_resultado[columnas_examenes_existentes].mean(axis=1)
    else:
        st.warning("No se encontró ninguna calificación de examen.")

    st.dataframe(df_resultado)

    st.subheader("📈 Distribución de promedios")
    conteo_promedios = df_resultado["Promedio"].round().value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 4))
    conteo_promedios.plot(kind="bar", ax=ax, color="orange")
    ax.set_title("Cantidad de alumnos por promedio redondeado")
    ax.set_xlabel("Promedio")
    ax.set_ylabel("Cantidad de alumnos")
    plt.xticks(rotation=0)
    st.pyplot(fig)

    csv_eval = df_resultado.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar evaluación final completa", csv_eval, "evaluacion_final_completa.csv")

elif seleccion == "Examen diagnóstico":
    st.subheader("📋 Examen diagnóstico")
    st.dataframe(df)
    graficar_puntaje(df, seleccion)

elif seleccion.startswith("Examen Semanal") or "extraordinario" in seleccion.lower():
    st.subheader(f"📋 {seleccion}")
    st.dataframe(df)
    graficar_puntaje(df, seleccion)
