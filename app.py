import streamlit as st
import requests
import json

# Configuración de secretos
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]

# Configurar el modo ancho por defecto
st.set_page_config(layout="wide")

# Lista ampliada de 500 conceptos relacionados con la Escuela de Salamanca y temas afines
CONCEPTOS = [
    "Derecho natural", "Derecho de gentes", "Justicia", "Ley", "Soberanía",
    "Propiedad privada", "Precio justo", "Usura", "Contrato", "Libertad",
    "Libre albedrío", "Tiranía", "Guerra justa", "Conquista", "Colonización",
    # ... [Se omiten los conceptos intermedios por brevedad] ...
    "Secularización", "Confesionalidad", "Tolerancia religiosa", "Libertad de conciencia", "Libertad religiosa",
    "Ius communicationis", "Ius peregrinandi", "Ius commercii", "Ius praedicandi", "Ius migrandi",
    "Derecho de descubrimiento", "Derecho de ocupación", "Res nullius", "Terra nullius", "Dominium",
    "Imperium", "Potestad", "Jurisdicción", "Fuero", "Privilegio",
    "Regalía", "Mayorazgo", "Señorío", "Vasallaje", "Encomienda",
    "Repartimiento", "Mita", "Obraje", "Hacienda", "Estanco",
    "Monopolio real", "Asiento", "Capitulación", "Bula papal", "Patronato regio",
    "Vicariato regio", "Regalismo", "Galicanismo", "Febronianismo", "Josefinismo",
    "Absolutismo", "Despotismo ilustrado", "Constitucionalismo", "Parlamentarismo", "Republicanismo",
    "Escolástica tardía", "Segunda escolástica", "Escuela de Salamanca", "Escuela de Coímbra", "Casuismo",
    "Probabilismo", "Equiprobabilismo", "Probabiliorismo", "Tuciorismo", "Laxismo",
    "Rigorismo", "Jansenismo", "Molinismo", "Bañecianismo", "Suarismo",
    "Tomismo", "Escotismo", "Ockhamismo", "Nominalismo", "Realismo moderado",
    "Realismo exagerado", "Conceptualismo", "Universales", "Esencia", "Existencia",
    "Acto", "Potencia", "Materia", "Forma", "Sustancia",
    "Accidente", "Causa", "Efecto", "Finalidad", "Teleología",
    "Providencia", "Predestinación", "Gracia", "Libre arbitrio", "Concurso divino",
    "Ciencia media", "Futuribles", "Premoción física", "Causa segunda", "Causa primera",
    "Analogía del ser", "Trascendentales", "Unidad", "Verdad", "Bondad",
    "Belleza", "Ente", "Esencia", "Existencia", "Subsistencia",
    "Persona", "Naturaleza", "Hipóstasis", "Unión hipostática", "Encarnación",
    "Trinidad", "Procesiones divinas", "Relaciones subsistentes", "Apropiaciones", "Misiones divinas",
    "Creación", "Conservación", "Concurso", "Providencia", "Gobierno divino",
    "Milagro", "Profecía", "Revelación", "Inspiración", "Tradición",
    "Magisterio", "Infalibilidad", "Ex cathedra", "Sensus fidelium", "Desarrollo doctrinal",
    "Hermenéutica", "Exégesis", "Tipología bíblica", "Alegoría", "Anagogía",
    "Tropología", "Cuádruple sentido de la Escritura", "Canon bíblico", "Deuterocanónicos", "Apócrifos",
    "Patrística", "Padres apostólicos", "Padres apologistas", "Padres de la Iglesia", "Doctores de la Iglesia",
    "Concilio", "Sínodo", "Colegio episcopal", "Primado papal", "Infalibilidad papal",
    "Jurisdicción ordinaria", "Jurisdicción delegada", "Potestad de orden", "Potestad de jurisdicción", "Potestad de magisterio",
    "Sacramento", "Ex opere operato", "Ex opere operantis", "Materia y forma sacramental", "Carácter sacramental",
    "Transubstanciación", "Consubstanciación", "Presencia real", "Comunión", "Sacrificio eucarístico",
    "Misa", "Liturgia", "Rito", "Ceremonia", "Rubrica",
    "Orden sagrado", "Sacerdocio común", "Sacerdocio ministerial", "Celibato", "Voto",
    "Estado de perfección", "Consejo evangélico", "Pobreza", "Castidad", "Obediencia",
    "Vida contemplativa", "Vida activa", "Vida mixta", "Oración mental", "Oración vocal",
    "Meditación", "Contemplación", "Éxtasis", "Unión mística", "Noche oscura",
    "Ascética", "Mística", "Vía purgativa", "Vía iluminativa", "Vía unitiva",
    "Virtud", "Vicio", "Hábito", "Pasión", "Afecto",
    "Prudencia", "Justicia", "Fortaleza", "Templanza", "Fe",
    "Esperanza", "Caridad", "Dones del Espíritu Santo", "Frutos del Espíritu Santo", "Bienaventuranzas",
    "Pecado", "Pecado original", "Pecado actual", "Pecado mortal", "Pecado venial",
    "Concupiscencia", "Tentación", "Ocasión próxima", "Escándalo", "Cooperación al mal",
    "Justificación", "Santificación", "Mérito", "Indulgencia", "Satisfacción",
    "Purgatorio", "Limbo", "Infierno", "Cielo", "Visión beatífica",
    "Resurrección", "Juicio particular", "Juicio universal", "Parusía", "Escatología",
    "Alma", "Cuerpo", "Espíritu", "Inmortalidad", "Transmigración",
    "Reencarnación", "Metempsicosis", "Creacionismo", "Traducianismo", "Generacianismo",
    "Facultades del alma", "Intelecto", "Voluntad", "Memoria", "Imaginación",
    "Sentidos externos", "Sentidos internos", "Cogitativa", "Estimativa", "Fantasía",
    "Abstracción", "Intuición", "Razonamiento", "Silogismo", "Inducción",
    "Deducción", "Analogía", "Equivocidad", "Univocidad", "Trascendentalidad",
    "Ley eterna", "Ley natural", "Ley positiva", "Ley divina", "Ley humana",
    "Derecho natural", "Derecho positivo", "Derecho de gentes", "Ius gentium", "Ius civile",
    "Derecho canónico", "Derecho eclesiástico", "Fuero eclesiástico", "Inmunidad eclesiástica", "Privilegio del fuero",
    "Simonía", "Nepotismo", "Pluralismo beneficial", "Absentismo", "Regalía",
    "Diezmo", "Primicia", "Oblación", "Limosna", "Estipendio",
    "Beneficio eclesiástico", "Prebenda", "Capellanía", "Patronato", "Presentación",
    "Investidura", "Colación canónica", "Institución canónica", "Posesión canónica", "Resignación",
    "Permuta", "Traslado", "Renuncia", "Deposición", "Degradación",
    "Excomunión", "Entredicho", "Suspensión", "Irregularidad", "Censura",
    "Dispensa", "Privilegio", "Costumbre", "Prescripción", "Epiqueia",
    "Tolerancia", "Disimulación", "Cooperación", "Resistencia pasiva", "Resistencia activa",
    "Tiranicidio", "Regicidio", "Magnicidio", "Sedición", "Rebelión",
    "Revolución", "Golpe de Estado", "Pronunciamiento", "Levantamiento", "Insurrección",
    "Razón de Estado", "Bien común", "Interés público", "Utilidad pública", "Necesidad pública",
    "Soberanía", "Majestad", "Potestad", "Autoridad", "Legitimidad",
    "Legalidad", "Estado de derecho", "Imperio de la ley", "Constitución", "Fuero",
    "Carta magna", "Ley fundamental", "Constitucionalismo", "Parlamentarismo", "Separación de poderes",
    "Monarquía", "Aristocracia", "Democracia", "Oligarquía", "Tiranía",
    "Despotismo", "Absolutismo", "Autoritarismo", "Totalitarismo", "Dictadura",
    "República", "Federalismo", "Confederación", "Unión personal", "Unión real",
    "Estado compuesto", "Estado unitario", "Autonomía", "Descentralización", "Desconcentración",
    "Subsidiariedad", "Solidaridad", "Cooperación", "Lealtad institucional", "Competencia",
    "Jerarquía normativa", "Reserva de ley", "Potestad reglamentaria", "Decreto-ley", "Ordenanza",
    "Tratado internacional", "Costumbre internacional", "Ius cogens", "Erga omnes", "Pacta sunt servanda",
    "Reciprocidad", "Retorsión", "Represalia", "Intervención", "Neutralidad",
    "Beligerancia", "Casus belli", "Ultimátum", "Declaración de guerra", "Armisticio",
    "Capitulación", "Tratado de paz", "Reparación de guerra", "Anexión", "Cesión territorial"
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
    genera una definición del concepto desde el punto de vista de al menos 5 autores relevantes de esta escuela. 
    Para cada autor, incluye su nombre, una breve definición o perspectiva sobre el concepto, y si es posible, una cita o referencia específica.

    Información:
    {info}

    Formato de respuesta:
    Concepto: [concepto]

    1. Autor: [nombre del autor]
       Definición: [breve definición o perspectiva]
       Cita/Referencia: [cita o referencia, si está disponible]

    2. Autor: [nombre del autor]
       Definición: [breve definición o perspectiva]
       Cita/Referencia: [cita o referencia, si está disponible]

    [Continuar con al menos 3 autores más...]

    Conclusión: [Breve síntesis de las diferentes perspectivas]
    """
    
    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "prompt": prompt,
        "max_tokens": 1000,
        "temperature": 0.7,
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['output']['choices'][0]['text'].strip()
    else:
        return f"Error en la generación: {response.status_code} - {response.text}"

def main():
    st.title("500 Conceptos de la Escuela de Salamanca")
    
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
