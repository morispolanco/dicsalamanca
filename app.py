import streamlit as st
import requests
import json

# Configuración de secretos
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]

# Configurar el modo ancho por defecto
st.set_page_config(layout="wide")

# Lista ampliada de 200 conceptos relacionados con la Escuela de Salamanca y temas afines
CONCEPTOS = [
    "Derecho natural", "Derecho de gentes", "Justicia", "Ley", "Soberanía",
    "Propiedad privada", "Precio justo", "Usura", "Contrato", "Libertad",
    "Libre albedrío", "Tiranía", "Guerra justa", "Conquista", "Colonización",
    "Esclavitud", "Indios", "Evangelización", "Poder civil", "Poder eclesiástico",
    "Derecho internacional", "Economía", "Mercado", "Valor", "Dinero",
    "Inflación", "Comercio", "Impuestos", "Bien común", "Estado",
    "Sociedad", "Individuo", "Derechos humanos", "Dignidad humana", "Igualdad",
    "Educación", "Conocimiento", "Razón", "Fe", "Teología",
    "Filosofía", "Ética", "Moral", "Virtud", "Pecado",
    "Salvación", "Gracia", "Naturaleza humana", "Sociedad civil", "Autoridad",
    "Probabilismo", "Monarquía", "República", "Tiranicidio", "Dominio",
    "Propiedad", "Comunidad", "Ley natural", "Ley positiva", "Ley divina",
    "Ley eterna", "Justicia conmutativa", "Justicia distributiva", "Bien común", "Prudencia",
    "Fortaleza", "Templanza", "Caridad", "Esperanza", "Misericordia",
    "Libre comercio", "Monopolio", "Competencia", "Oferta y demanda", "Valor del trabajo",
    "Salario justo", "Interés", "Cambio de divisas", "Banca", "Crédito",
    "Deuda pública", "Fiscalidad", "Tributos", "Diezmo", "Simonía",
    "Patronato regio", "Regalismo", "Conciliarismo", "Papado", "Reforma protestante",
    "Contrarreforma", "Inquisición", "Herejía", "Ortodoxia", "Dogma",
    "Casuística", "Probabilismo moral", "Tuciorismo", "Laxismo", "Rigorismo",
    "Conciencia", "Ley natural", "Derecho subjetivo", "Derecho objetivo", "Ius gentium",
    "Ius civile", "Ius naturale", "Derecho de resistencia", "Pacto social", "Contrato social",
    "Origen del poder", "Traslación del poder", "Legitimidad", "Tiranía de origen", "Tiranía de ejercicio",
    "Regicidio", "Magnicidio", "Razón de Estado", "Maquiavelismo", "Tacitismo",
    "Providencia", "Predestinación", "Libre arbitrio", "Gracia suficiente", "Gracia eficaz",
    "Jansenismo", "Molinismo", "Bañecianismo", "Congruismo", "Ciencia media",
    "Futuribles", "Premoción física", "Concurso divino", "Causa segunda", "Causa primera",
    "Metafísica", "Ontología", "Epistemología", "Lógica", "Retórica",
    "Gramática", "Dialéctica", "Física", "Cosmología", "Psicología",
    "Antropología", "Escatología", "Soteriología", "Cristología", "Eclesiología",
    "Mariología", "Pneumatología", "Angelología", "Demonología", "Hamartiología",
    "Justificación", "Santificación", "Predestinación", "Reprobación", "Limbo",
    "Purgatorio", "Indulgencias", "Sacramentos", "Eucaristía", "Penitencia",
    "Orden sacerdotal", "Matrimonio", "Celibato", "Votos religiosos", "Mística",
    "Ascética", "Oración mental", "Contemplación", "Éxtasis", "Revelación",
    "Tradición", "Magisterio", "Concilio", "Sínodo", "Bula papal",
    "Encíclica", "Canon bíblico", "Exégesis", "Hermenéutica", "Patrística",
    "Escolástica", "Tomismo", "Escotismo", "Nominalismo", "Realismo",
    "Humanismo", "Renacimiento", "Barroco", "Ilustración", "Modernidad",
    "Secularización", "Confesionalidad", "Tolerancia religiosa", "Libertad de conciencia", "Libertad religiosa"
]

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
    
    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "prompt": prompt,
        "max_tokens": 300,
        "temperature": 0.7,
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['output']['choices'][0]['text'].strip()
    else:
        return f"Error en la generación: {response.status_code} - {response.text}"

def main():
    st.title("200 Conceptos de la Escuela de Salamanca")
    
    # Crear dos columnas con proporción 1:2
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Lista de Conceptos")
        concepto_seleccionado = st.selectbox("Selecciona un concepto:", CONCEPTOS)
        
        st.subheader("O introduce tu propio concepto:")
        concepto_personalizado = st.text_input("Concepto personalizado:")
    
    with col2:
        st.subheader("Definición del Concepto")
        
        # Determinar qué concepto usar
        concepto_final = concepto_personalizado if concepto_personalizado else concepto_seleccionado
        
        if st.button("Generar Definición"):
            if concepto_final:
                with st.spinner("Buscando información y generando definición..."):
                    # Buscar información
                    info = buscar_informacion(f"{concepto_final} Escuela de Salamanca")
                    
                    # Extraer texto relevante de los resultados de búsqueda
                    texto_relevante = ""
                    for resultado in info.get('organic', [])[:3]:
                        texto_relevante += resultado.get('snippet', '') + " "
                    
                    # Generar definición
                    definicion = generar_definicion(concepto_final, texto_relevante)
                    
                    # Mostrar resultado
                    st.write(definicion)
            else:
                st.warning("Por favor, selecciona un concepto o introduce uno personalizado.")

if __name__ == "__main__":
    main()
