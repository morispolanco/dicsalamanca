import streamlit as st
import requests
import json

# Configuración de secretos
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]

# Configurar el modo ancho por defecto
st.set_page_config(layout="wide")

# Lista de 500 conceptos relacionados con la Escuela de Salamanca y temas afines, ordenados alfabéticamente
CONCEPTOS = sorted([
    "absolución", "abstención", "abuso de poder", "aceptación", "acuerdo", "acto humano", "acto moral", 
    "actuación", "acusación", "admiración", "adquisición de bienes", "adulterio", "afecto", "agricultura", 
    "altruismo", "amparo", "análisis económico", "análisis jurídico", "análisis moral", "análisis teológico", 
    "anomia", "anulación", "apetito", "apropiación", "arbitrio", "argumentación moral", "armonía social", 
    "arrepentimiento", "arte de gobernar", "ascetismo", "asociación voluntaria", "asociacionismo", "asunción de deuda", 
    "autoridad legítima", "avaricia", "ayuda al prójimo", "beneficencia", "benevolencia", "bien común", "bienes comunales", 
    "bienes públicos", "bienes raíces", "bienes temporal", "bienes terrenales", "cálculo moral", "causalidad moral", 
    "causa eficiente", "causa final", "causa material", "causa moral", "causa natural", "censura", "certeza moral", 
    "ciencia económica", "ciudadanía", "clasificación moral", "claustro", "coacción", "códigos morales", "cogitaciones", 
    "cohesión social", "colaboración", "colectivismo", "comercio", "comercio internacional", "comercio justo", "comercio regional", 
    "comodidad", "comparación social", "compasión", "competencia comercial", "competencia económica", "complementariedad", 
    "complejidad moral", "compromiso ético", "comunicación veraz", "comunidad", "comunidad cristiana", "conciencia", "conciencia ética", 
    "conciencia moral", "concordia", "confianza", "confianza económica", "confianza social", "conflicto de intereses", 
    "conflictos morales", "consanguinidad", "consenso", "consentimiento", "consentimiento informado", "consecuencia ética", 
    "consecuencialismo", "consideración moral", "constancia moral", "consultoría jurídica", "consumo", "contabilidad", "contingencia", 
    "contrabando", "contractualismo", "contratos", "control económico", "control social", "conversión", "cooperación", "costo-beneficio", 
    "creación de valor", "credibilidad", "crédito", "creencias", "criminalidad", "criterios jurídicos", "criterios morales", "culpabilidad", 
    "cumplimiento", "deberes", "debido proceso", "declaración de derechos", "defensoría", "deleite moral", "deliberación", "delincuencia", 
    "demanda", "democracia", "derecho aduanero", "derecho canónico", "derecho civil", "derecho común", "derecho consuetudinario", 
    "derecho contractual", "derecho divino", "derecho económico", "derecho eclesiástico", "derecho internacional", "derecho laboral", 
    "derecho mercantil", "derecho natural", "derecho penal", "derechos humanos", "desacuerdo moral", "desafío moral", "desigualdad", 
    "desinterés", "desobediencia civil", "devoción", "diálogo interreligioso", "dignidad humana", "dinero", "dinero justo", "dinero y moral", 
    "discernimiento", "disciplinas económicas", "diseño divino", "disputas jurídicas", "doctrina cristiana", "doctrina jurídica", 
    "doctrina moral", "dualismo", "dualidad moral", "educación moral", "eficiencia económica", "eficiencia moral", "egoísmo", "equidad", 
    "equilibrio económico", "esclavitud", "esperanza", "espiritualidad", "estado de naturaleza", "estudio de casos", "ética", 
    "ética aplicada", "ética bancaria", "ética comercial", "ética económica", "ética empresarial", "ética natural", "ética profesional", 
    "ética religiosa", "examen de conciencia", "excomunión", "expiación", "explicación", "extorsión", "fabricación moral", 
    "facilidades económicas", "falacia", "familia", "fe", "filiación", "filosofía moral", "filosofía política", "fiscalidad", 
    "florecimiento humano", "formación ética", "formación moral", "fraude", "frugalidad", "función social", "generosidad", 
    "gestión empresarial", "glotonería", "gobierno", "gracia", "gula", "gusto", "hazañas", "hechos morales", "herramientas económicas", 
    "hombres libres", "honestidad", "honor", "humanismo cristiano", "humanitarismo", "igualdad", "imparcialidad", "imperativo moral", 
    "inclinaciones naturales", "individualismo", "industria", "infalibilidad", "inflación", "injusticia", "inversión", "juicio moral", 
    "jurisprudencia", "justicia", "justicia distributiva", "justicia económica", "justicia social", "justificación", "labor", "laicidad", 
    "legitimación", "legitimidad", "liberalismo económico", "libertad", "libertad económica", "licitud", "lógica moral", "lujuria", 
    "luminosidad moral", "mal moral", "maleficio", "mandato moral", "mano invisible", "matrimonio", "mediación", "mercado", "merced", 
    "merecimiento", "migración", "minorías", "misericordia", "modelo económico", "modulación moral", "monopolio", "moral", 
    "moral absoluta", "moral de la intención", "moral de la obligación", "moral de la virtud", "moral de mercado", "moral del deber", 
    "moral natural", "moral normativa", "moral pública", "moral relativa", "moral teológica", "moral utilitaria", "moralidad", 
    "mortalidad", "mutabilidad", "necesidad económica", "necesidad vital", "negociación", "negligencia", "nobleza", "obediencia", 
    "obligación", "observación moral", "oferta", "orden divino", "orden económico", "orden moral", "orden natural", "orden social", 
    "ordenamiento jurídico", "origen moral", "pacto social", "paganismo", "paternidad", "paz social", "pecado", "pecado capital", 
    "pecado mortal", "pecado venial", "penitencia", "perdón", "perfección moral", "pericia económica", "perspectiva económica", 
    "persuasión moral", "phronesis", "piedad", "pluralismo", "pobreza", "poder", "politica económica", "posesión", 
    "postulados morales", "praxis", "pragmatismo", "precepto moral", "predestinado", "precio justo", "precio y valor", 
    "predicación", "predisposición", "preferencias morales", "prejuicio", "prescripción jurídica", "prestación", 
    "principio de legalidad", "principio de subsidiariedad", "privacidad", "probidad", "problemas morales", "procesos económicos", 
    "producción", "productividad", "profecía", "protección", "protección social", "providencia", "prudencia", "pudor", 
    "purificación", "purgatorio", "pureza", "realismo moral", "recaudación fiscal", "reconciliación", "reforma", 
    "regeneración", "reglas comerciales", "regulación", "remordimiento", "rendición de cuentas", "reparación", 
    "resarcimiento", "responsabilidad", "responsabilidad jurídica", "restricción moral", "reto moral", "salario", 
    "salvación", "santidad", "sindéresis", "sinergia", "sistema económico", "soberanía", "solidaridad", "soporte moral", 
    "suavidad moral", "subsidios", "sufragio", "superación moral", "supervisión", "sustancia moral", "templanza", 
    "tentación", "testimonio", "tiranía", "tolerancia", "trabajo", "tradición", "transacciones comerciales", "transparencia", 
    "trascendencia", "tributación", "unidad", "universales morales", "utilidad", "utilitarismo", "valor", "valores morales", 
    "verdad", "verosimilitud", "virtud", "virtud económica", "voluntad", "voluntariado", "voluntarismo", "voto", "xenofobia"
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
        "max_tokens": 2900,
        "temperature": 0.7,
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['output']['choices'][0]['text'].strip()
    else:
        return f"Error en la generación: {response.status_code} - {response.text}"

def main():
    # Crear tres columnas con proporción 1:2:1
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown(
            """
            <style>
            .sidebar {
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                color: gray;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            }
            .sidebar h2 {
                color: gray;
            }
            .header {
                background-color: gray;
                padding: 10px;
                border-radius: 10px;
                text-align: center;
                color: white;
                font-size: 24px;
                margin-bottom: 20px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # Mover el título a la franja gris
        st.markdown('<div class="header">Sobre esta aplicación</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar">', unsafe_allow_html=True)
        st.write("""
        Esta aplicación te permite explorar 500 conceptos relacionados con la Escuela de Salamanca.
        
        Selecciona un concepto de la lista o introduce uno personalizado para generar definiciones desde la perspectiva de autores relevantes de la Escuela de Salamanca.
        
        **Autor**: Moris Polanco  
        **Año**: 2024
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Título principal solo en la columna central
        st.title("500 Conceptos de la Escuela de Salamanca")
        
        st.subheader("Lista de Conceptos")
        concepto_seleccionado = st.selectbox("Selecciona un concepto:", CONCEPTOS)
        
        st.subheader("O introduce tu propio concepto:")
        concepto_personalizado = st.text_input("Concepto personalizado:")
        
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
                    
                    # Separar las citas por párrafos y mostrar resultado
                    definiciones_por_parrafos = definiciones.split('\n\n')
                    for parrafo in definiciones_por_parrafos:
                        st.markdown(parrafo)
                        st.markdown("")  # Esto añade una línea en blanco entre párrafos
            else:
                st.warning("Por favor, selecciona un concepto o introduce uno personalizado.")
    
    # La tercera columna se deja vacía para mantener el diseño centrado

if __name__ == "__main__":
    main()
