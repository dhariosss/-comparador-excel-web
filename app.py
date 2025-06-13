import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Comparador de Archivos Excel - Alianza vs Dartis", layout="centered")

st.markdown("""
    <div style='display: flex; align-items: center; gap: 10px;'>
        <div style='background-color: #22c55e; border-radius: 50%; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center;'>
            <span style='font-size: 30px; color: white;'>▩</span>
        </div>
        <h1 style='margin: 0;'>Comparador de Archivos Excel</h1>
    </div>
    <br>
""", unsafe_allow_html=True)

archivo_alianza = st.file_uploader("Documento Alianza:", type=[".xls", ".xlsx"], key="alianza")
archivo_dartis = st.file_uploader("Documento Dartis:", type=[".xls", ".xlsx"], key="dartis")

if archivo_alianza and archivo_dartis:
    try:
        df_alianza = pd.read_excel(archivo_alianza)
        df_dartis = pd.read_excel(archivo_dartis)

        columnas_comunes = sorted(list(set(df_alianza.columns) & set(df_dartis.columns)))

        if len(columnas_comunes) >= 1:
            columnas_seleccionadas = st.multiselect("Selecciona hasta 3 columnas para comparar:", columnas_comunes, max_selections=3)

            if columnas_seleccionadas:
                df_coincidencias = pd.merge(df_alianza, df_dartis, on=columnas_seleccionadas)
                df_solo_alianza = df_alianza.merge(df_coincidencias, on=columnas_seleccionadas, how='left', indicator=True)
                df_solo_alianza = df_solo_alianza[df_solo_alianza['_merge'] == 'left_only'].drop(columns=['_merge'])

                df_solo_dartis = df_dartis.merge(df_coincidencias, on=columnas_seleccionadas, how='left', indicator=True)
                df_solo_dartis = df_solo_dartis[df_solo_dartis['_merge'] == 'left_only'].drop(columns=['_merge'])

                df_todos = pd.concat([df_alianza[ columnas_seleccionadas ], df_dartis[ columnas_seleccionadas ]]).drop_duplicates()
                df_no_coinciden = df_todos[~df_todos.apply(tuple, axis=1).isin(df_coincidencias.apply(tuple, axis=1))]

                st.subheader("Coincidencias")
                filtro1 = st.text_input("Filtrar Coincidencias", key="f1")
                st.dataframe(df_coincidencias[df_coincidencias.apply(lambda row: filtro1.lower() in str(row.values).lower(), axis=1)] if filtro1 else df_coincidencias)

                st.subheader("Solo en Documento Alianza")
                filtro2 = st.text_input("Filtrar Solo en Alianza", key="f2")
                st.dataframe(df_solo_alianza[df_solo_alianza.apply(lambda row: filtro2.lower() in str(row.values).lower(), axis=1)] if filtro2 else df_solo_alianza)

                st.subheader("Solo en Documento Dartis")
                filtro3 = st.text_input("Filtrar Solo en Dartis", key="f3")
                st.dataframe(df_solo_dartis[df_solo_dartis.apply(lambda row: filtro3.lower() in str(row.values).lower(), axis=1)] if filtro3 else df_solo_dartis)

                st.subheader("Datos que no coinciden completamente")
                filtro4 = st.text_input("Filtrar Datos No Coincidentes", key="f4")
                st.dataframe(df_no_coinciden[df_no_coinciden.apply(lambda row: filtro4.lower() in str(row.values).lower(), axis=1)] if filtro4 else df_no_coinciden)

                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_coincidencias.to_excel(writer, sheet_name="Coincidencias", index=False)
                    df_solo_alianza.to_excel(writer, sheet_name="Solo en Alianza", index=False)
                    df_solo_dartis.to_excel(writer, sheet_name="Solo en Dartis", index=False)
                    df_no_coinciden.to_excel(writer, sheet_name="No Coinciden", index=False)
                output.seek(0)

                st.download_button(
                    label="💾 Descargar Resultados en Excel",
                    data=output,
                    file_name="resultado_comparacion.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.warning("Los archivos no tienen columnas en común para comparar.")

    except Exception as e:
        st.error(f"Error al leer los archivos: {e}")
