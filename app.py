import streamlit as st
import requests
import json
from together import Together

# Configuración de secretos
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]

# Configuración de Together AI
together = Together(api_key=TOGETHER_API_KEY)

def buscar_informacion(query):
    url = "https://google.serper.dev/search"
    payload = json.dumps({
        "q": query
    })
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def generar_definicion(concepto, info):
    prompt = f"""Basándote en la siguiente información sobre el concepto '{concepto}' y tu conocimiento sobre la Escuela de Salamanca, 
    genera una definición del concepto desde el punto de vista de un autor relevante de esta escuela. 
    Incluye el nombre del autor y, si es posible, una cita o referencia específica.

    Información:
    {info}

    Formato de respuesta:
    Concepto: [concepto]
    Autor: [nombre del autor de la Escuela de Salamanca]
    Definición: [definición del concepto]
    Cita/Referencia: [cita o referencia, si está disponible]
    """

    response = together.complete(
        prompt=prompt,
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        max_tokens=300,
        temperature=0.7,
    )
    
    return response['output']['choices'][0]['text'].strip()

def main():
    st.title("Conceptos de la Escuela de Salamanca")
    
    concepto = st.text_input("Introduce un concepto para definir:")
    
    if st.button("Generar Definición"):
        if concepto:
            with st.spinner("Buscando información y generando definición..."):
                # Buscar información
                info = buscar_informacion(f"{concepto} Escuela de Salamanca")
                
                # Extraer texto relevante de los resultados de búsqueda
                texto_relevante = ""
                for resultado in info.get('organic', [])[:3]:
                    texto_relevante += resultado.get('snippet', '') + " "
                
                # Generar definición
                definicion = generar_definicion(concepto, texto_relevante)
                
                # Mostrar resultado
                st.subheader("Definición generada:")
                st.write(definicion)
        else:
            st.warning("Por favor, introduce un concepto.")

if __name__ == "__main__":
    main()
