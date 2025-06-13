
# 📊 Comparador de Archivos Excel – Alianza vs Dartis

Esta es una aplicación web interactiva construida con [Streamlit](https://streamlit.io) que permite comparar dos archivos Excel (`.xls` o `.xlsx`) y mostrar:

- ✅ Coincidencias entre ambos archivos según una columna en común.
- 📌 Filas exclusivas del archivo de **Alianza**.
- 📌 Filas exclusivas del archivo de **Dartis**.
- 🔍 Búsqueda y filtrado dinámico por texto.
- 📥 Exportación del resultado completo en un solo archivo Excel.

## 🧰 Requisitos

```bash
pip install streamlit pandas openpyxl
```

## ▶️ ¿Cómo ejecutarlo localmente?

```bash
streamlit run app.py
```

## 🌐 ¿Cómo desplegarlo en la nube (Streamlit Cloud)?

1. Crea una cuenta gratuita en [streamlit.io/cloud](https://streamlit.io/cloud).
2. Sube este repositorio a GitHub.
3. Desde tu panel de Streamlit Cloud:
   - Haz clic en **“New App”**.
   - Selecciona tu repositorio y archivo `app.py`.

## 🛡️ Licencia

Este proyecto está bajo la licencia MIT.
