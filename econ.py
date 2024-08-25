import streamlit as st
import requests
import json
from docx import Document
from docx.shared import Inches
from io import BytesIO

# Configuración de la página
st.set_page_config(page_title="Asistente de Economía - Escuela de Salamanca", page_icon="📚")

# Título de la aplicación
st.title("Asistente de Economía - Escuela de Salamanca")

# Acceder a las claves de API de los secretos de Streamlit
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]

def buscar_informacion(query):
    url = "https://google.serper.dev/search"
    payload = json.dumps({
        "q": query + " Escuela de Salamanca economía"
    })
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def generar_respuesta(prompt, contexto):
    url = "https://api.together.xyz/inference"
    payload = json.dumps({
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "prompt": f"Contexto: {contexto}\n\nPregunta: {prompt}\n\nResponde la pregunta basándote en el contexto proporcionado y tu conocimiento sobre los conceptos económicos según la Escuela de Salamanca. Incluye referencias a obras específicas de los autores de esta escuela cuando sea posible.\n\nRespuesta:",
        "max_tokens": 5512,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "stop": ["Pregunta:"]
    })
    headers = {
        'Authorization': f'Bearer {TOGETHER_API_KEY}',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()['output']['choices'][0]['text'].strip()

def create_docx(pregunta, respuesta, fuentes):
    doc = Document()
    doc.add_heading('Asistente de Economía - Escuela de Salamanca', 0)

    doc.add_heading('Pregunta', level=1)
    doc.add_paragraph(pregunta)

    doc.add_heading('Respuesta', level=1)
    doc.add_paragraph(respuesta)

    doc.add_heading('Fuentes', level=1)
    for fuente in fuentes:
        doc.add_paragraph(fuente, style='List Bullet')

    doc.add_paragraph('\nNota: Este documento fue generado por un asistente de IA. Verifica la información con fuentes académicas para un análisis más profundo.')

    return doc

# Interfaz de usuario
pregunta = st.text_input("Ingresa tu pregunta sobre conceptos económicos según la Escuela de Salamanca:")

if st.button("Obtener respuesta"):
    if pregunta:
        with st.spinner("Buscando información y generando respuesta..."):
            # Buscar información relevante
            resultados_busqueda = buscar_informacion(pregunta)
            contexto = "\n".join([result.get('snippet', '') for result in resultados_busqueda.get('organic', [])])

            # Generar respuesta
            respuesta = generar_respuesta(pregunta, contexto)

            # Mostrar respuesta
            st.write("Respuesta:")
            st.write(respuesta)

            # Mostrar fuentes
            st.write("Fuentes:")
            fuentes = []
            for resultado in resultados_busqueda.get('organic', [])[:3]:
                fuente = f"{resultado['title']}: {resultado['link']}"
                st.write(f"- [{resultado['title']}]({resultado['link']})")
                fuentes.append(fuente)

            # Crear documento DOCX
            doc = create_docx(pregunta, respuesta, fuentes)

            # Guardar el documento DOCX en memoria
            docx_file = BytesIO()
            doc.save(docx_file)
            docx_file.seek(0)

            # Opción para exportar a DOCX
            st.download_button(
                label="Descargar resultados como DOCX",
                data=docx_file,
                file_name="respuesta_economia_salamanca.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

    else:
        st.warning("Por favor, ingresa una pregunta.")

# Agregar información en el pie de página
st.markdown("---")
st.markdown("**Nota:** Este asistente utiliza IA para generar respuestas basadas en información disponible en línea sobre la Escuela de Salamanca. "
            "Siempre verifica la información con fuentes académicas para un análisis más profundo de los conceptos económicos.")
