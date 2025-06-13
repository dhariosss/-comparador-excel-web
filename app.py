
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Comparador de Excel - Alianza vs Dartis", layout="wide")
st.title("📊 Comparador de Archivos Excel - Alianza vs Dartis")

st.markdown("Sube dos archivos Excel para comparar sus contenidos en base a una columna en común.")

archivo_alianza = st.file_uploader("📁 Documento Alianza", type=[".xls", ".xlsx"], key="alianza")
archivo_dartis = st.file_uploader("📁 Documento Dartis", type=[".xls", ".xlsx"], key="dartis")

if archivo_alianza and archivo_dartis:
    try:
        df_alianza = pd.read_excel(archivo_alianza)
        df_dartis = pd.read_excel(archivo_dartis)

        columnas_comunes = sorted(list(set(df_alianza.columns) & set(df_dartis.columns)))

        if columnas_comunes:
            columna_clave = st.selectbox("🔑 Selecciona la columna para comparar:", columnas_comunes)

            if columna_clave:
                df_coincidencias = pd.merge(df_alianza, df_dartis, on=columna_clave)
                df_solo_alianza = df_alianza[~df_alianza[columna_clave].isin(df_dartis[columna_clave])]
                df_solo_dartis = df_dartis[~df_dartis[columna_clave].isin(df_alianza[columna_clave])]

                st.subheader("✅ Coincidencias")
                filtro1 = st.text_input("Filtrar Coincidencias", key="f1")
                st.dataframe(df_coincidencias[df_coincidencias.apply(lambda row: filtro1.lower() in str(row.values).lower(), axis=1)] if filtro1 else df_coincidencias, use_container_width=True)

                st.subheader("📌 Solo en Documento Alianza")
                filtro2 = st.text_input("Filtrar Solo en Alianza", key="f2")
                st.dataframe(df_solo_alianza[df_solo_alianza.apply(lambda row: filtro2.lower() in str(row.values).lower(), axis=1)] if filtro2 else df_solo_alianza, use_container_width=True)

                st.subheader("📌 Solo en Documento Dartis")
                filtro3 = st.text_input("Filtrar Solo en Dartis", key="f3")
                st.dataframe(df_solo_dartis[df_solo_dartis.apply(lambda row: filtro3.lower() in str(row.values).lower(), axis=1)] if filtro3 else df_solo_dartis, use_container_width=True)

                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_coincidencias.to_excel(writer, sheet_name="Coincidencias", index=False)
                    df_solo_alianza.to_excel(writer, sheet_name="Solo en Alianza", index=False)
                    df_solo_dartis.to_excel(writer, sheet_name="Solo en Dartis", index=False)
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
