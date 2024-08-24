import streamlit as st
import requests
import json

# Configuración de secretos
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]

# Configurar el modo ancho por defecto
st.set_page_config(layout="wide")

# Lista de 99 conceptos económicos relacionados con la Escuela de Salamanca y temas afines, ordenados alfabéticamente
CONCEPTOS = sorted([
    "acción humana", "acción social", "acumulación de riquezas", "agricultura", "alcabalas", "alquiler", "alma", "altruismo", "amor del prójimo", "arbitraje", "arrendamiento", "beneficencia", "beneficio", "bienes", "bienes comunales", "bienes raíces", "bienes tangibles", "capital", "caridad", "circulante", "circulación monetaria", "comercio", "compasión", "comprensión", "confianza", "contrabando", "contrato", "cooperación", "crédito", "deuda", "deuda pública", "dignidad", "dinero", "disciplina", "distribución de riquezas", "equidad", "ética", "excedente", "fiscalización", "fortaleza económica", "ganancia", "gastos", "gremios", "herencia", "honor", "hombres de negocios", "humildad", "igualdad", "impuestos", "inflación", "inversión", "justicia", "latifundio", "liberalidad", "libre mercado", "magnanimidad", "mancomunidad", "mercado", "mercancías", "mercantilismo", "miseria", "misericordia", "moneda", "monopolio", "moral", "moral económica", "pecunia", "precio", "precio justo", "prejuicio", "prestación", "préstamo", "productividad", "proteccionismo", "pueblo", "riquezas", "renta", "santa inquisición", "servicios", "sociedad", "soberanía", "solidaridad", "suma teológica", "superávit", "tenencia", "trabajo", "tributación", "trueque", "usura", "valor", "venta justa", "virtud", "voluntad", "zafra"
])

def buscar_informacion(query):
    url = "https://google.serper.dev/search"
    payload = json.dumps({
        "q": query
    })
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)
    return response.json()

def generar_definicion(concepto, info):
    url = "https://api.together.xyz/inference"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"""Basándote en la siguiente información sobre el concepto '{concepto}' y tu conocimiento sobre la Escuela de Salamanca, 
    genera una definición del concepto desde el punto de vista de al menos 10 autores relevantes de esta escuela. 
    Para cada autor, incluye su nombre, una breve definición o perspectiva sobre el concepto, y si es posible, una cita o referencia específica.
    Finaliza con una breve síntesis de las diferentes perspectivas.

    Información:
    {info}
    """
    
    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "prompt": prompt,
        "max_tokens": 2200,
        "temperature": 0.7,
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['output']['choices'][0]['text'].strip()
    else:
        return f"Error en la generación: {response.status_code} - {response.text}"

def main():
    st.title("99 Conceptos económicos de la Escuela de Salamanca")
    
    # Crear dos columnas con proporción 1:3
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Lista de Conceptos")
        concepto_seleccionado = st.selectbox("Selecciona un concepto:", CONCEPTOS)
        
        st.subheader("O introduce tu propio concepto:")
        concepto_personalizado = st.text_input("Concepto personalizado:")
    
    with col2:
        st.subheader("Definiciones del Concepto")
        
        # Determinar qué concepto usar
        concepto_final = concepto_personalizado if concepto_personalizado else concepto_seleccionado
        
        if st.button("Generar Definiciones"):
            if concepto_final:
                with st.spinner("Buscando información y generando definiciones..."):
                    # Buscar información
                    info = buscar_informacion(f"{concepto_final} Escuela de Salamanca")
                    
                    # Extraer texto relevante de los resultados de búsqueda
                    texto_relevante = ""
                    for resultado in info.get('organic', [])[:5]:
                        texto_relevante += resultado.get('snippet', '') + " "
                    
                    # Generar definiciones
                    definiciones = generar_definicion(concepto_final, texto_relevante)
                    
                    # Mostrar resultado
                    st.markdown(definiciones)
            else:
                st.warning("Por favor, selecciona un concepto o introduce uno personalizado.")

if __name__ == "__main__":
    main()
