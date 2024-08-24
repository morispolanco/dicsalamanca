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
    "Absentismo", "Absolutismo", "Abstracción", "Accidente", "Acto",
    "Alegoría", "Alma", "Analogía", "Analogía del ser", "Anagogía",
    "Anexión", "Antipapa", "Apropiaciones", "Arbitrismo", "Aristocracia",
    "Armisticio", "Ascética", "Asiento", "Autoritarismo", "Autoridad",
    "Autonomía", "Beatificación", "Belleza", "Beneficio eclesiástico", "Bienaventuranzas",
    "Bien común", "Bula papal", "Calvinismo", "Canonización", "Canon bíblico",
    "Capitulación", "Capellanía", "Caridad", "Carta magna", "Casus belli",
    "Casuismo", "Casuística", "Causa", "Causa primera", "Causa segunda",
    "Celibato", "Censura", "Cesión territorial", "Cielo", "Ciencia media",
    "Cisma", "Colegio episcopal", "Colación canónica", "Colonización", "Competencia",
    "Comunión", "Concepción inmaculada", "Conciliarismo", "Concilio", "Concupiscencia",
    "Confesionalidad", "Confederación", "Confirmación", "Conquista", "Consejo evangélico",
    "Conservación", "Consubstanciación", "Constitución", "Constitucionalismo", "Contemplación",
    "Contrarreforma", "Contrato", "Contrato social", "Cooperación", "Cooperación al mal",
    "Costumbre", "Costumbre internacional", "Creación", "Creacionismo", "Cuerpo",
    "Declaración de guerra", "Decreto-ley", "Degradación", "Democracia", "Demonología",
    "Derecho canónico", "Derecho de descubrimiento", "Derecho de gentes", "Derecho de ocupación",
    "Derecho eclesiástico", "Derecho internacional", "Derecho natural", "Derecho positivo",
    "Derecho subjetivo", "Desarrollo doctrinal", "Desconcentración", "Descentralización",
    "Despotismo", "Despotismo ilustrado", "Deuterocanónicos", "Diezmo", "Dignidad humana",
    "Dispensa", "Disimulación", "Dictadura", "Dominio", "Dominium",
    "Eclesiología", "Economía", "Efecto", "Encarnación", "Encíclica",
    "Encomienda", "Entredicho", "Epiqueia", "Equiprobabilismo", "Erga omnes",
    "Escatología", "Escolástica tardía", "Escotismo", "Escuela de Coímbra", "Escuela de Salamanca",
    "Escándalo", "Esencia", "Espíritu", "Esperanza", "Estado",
    "Estado compuesto", "Estado de derecho", "Estado de perfección", "Estado unitario", "Estanco",
    "Estimativa", "Eucaristía", "Evangelización", "Ex cathedra", "Ex opere operantis",
    "Ex opere operato", "Excomunión", "Exégesis", "Existencia", "Éxtasis",
    "Facultades del alma", "Fantasía", "Fe", "Febronianismo", "Federalismo",
    "Finalidad", "Forma", "Fortaleza", "Frutos del Espíritu Santo", "Fuero",
    "Fuero eclesiástico", "Futuribles", "Galicanismo", "Generacianismo", "Gobierno divino",
    "Golpe de Estado", "Gracia", "Guerra justa", "Hábito", "Hacienda",
    "Herejía", "Hermenéutica", "Hipóstasis", "Humanismo", "Ilustración",
    "Imperium", "Imperio de la ley", "Inducción", "Indulgencia", "Infalibilidad",
    "Infalibilidad papal", "Infierno", "Inflación", "Inmortalidad", "Inmunidad eclesiástica",
    "Inquisición", "Inspiración", "Institución canónica", "Intelecto", "Interés",
    "Interés público", "Intervención", "Intuición", "Investidura", "Irregularidad",
    "Ius civile", "Ius cogens", "Ius commercii", "Ius communicationis", "Ius gentium",
    "Ius migrandi", "Ius naturale", "Ius peregrinandi", "Ius praedicandi", "Jansenismo",
    "Jerarquía normativa", "Josefinismo", "Juicio particular", "Juicio universal", "Jurisdicción",
    "Justicia", "Justicia conmutativa", "Justicia distributiva", "Justificación", "Laxismo",
    "Lealtad institucional", "Legalidad", "Legitimidad", "Ley", "Ley divina",
    "Ley eterna", "Ley fundamental", "Ley humana", "Ley natural", "Ley positiva",
    "Liberalismo", "Libertad", "Libertad de conciencia", "Libertad religiosa", "Libre albedrío",
    "Libre arbitrio", "Libre comercio", "Limbo", "Limosna", "Liturgia",
    "Magisterio", "Magnicidio", "Majestad", "Materia", "Materia y forma sacramental",
    "Matrimonio", "Mayorazgo", "Meditación", "Memoria", "Mérito",
    "Metempsicosis", "Milagro", "Misa", "Misericordia", "Misiones divinas",
    "Mística", "Mita", "Modernidad", "Molinismo", "Monarquía",
    "Monopolio", "Monopolio real", "Moral", "Naturaleza", "Naturaleza humana",
    "Necesidad pública", "Nepotismo", "Neutralidad", "Noche oscura", "Nominalismo",
    "Obediencia", "Oblación", "Obraje", "Ocasión próxima", "Ockhamismo",
    "Oferta y demanda", "Oligarquía", "Ontología", "Oración mental", "Oración vocal",
    "Orden sagrado", "Ordenanza", "Ortodoxia", "Pacta sunt servanda", "Pacto social",
    "Padres apologistas", "Padres apostólicos", "Padres de la Iglesia", "Papado", "Parlamentarismo",
    "Parusía", "Pasión", "Patrística", "Patronato", "Patronato regio",
    "Pecado", "Pecado actual", "Pecado mortal", "Pecado original", "Pecado venial",
    "Penitencia", "Permuta", "Persona", "Pluralismo beneficial", "Pneumatología",
    "Pobreza", "Poder civil", "Poder eclesiástico", "Posesión canónica", "Potestad",
    "Potestad de jurisdicción", "Potestad de magisterio", "Potestad de orden", "Potestad reglamentaria", "Potencia",
    "Prebenda", "Precio justo", "Predestinación", "Premoción física", "Presencia real",
    "Presentación", "Primado papal", "Primicia", "Privilegio", "Privilegio del fuero",
    "Probabiliorismo", "Probabilismo", "Probabilismo moral", "Procesiones divinas", "Profecía",
    "Pronunciamiento", "Propiedad", "Propiedad privada", "Providencia", "Prudencia",
    "Purgatorio", "Razonamiento", "Razón", "Razón de Estado", "Realismo exagerado",
    "Realismo moderado", "Reciprocidad", "Reencarnación", "Reforma protestante", "Regalía",
    "Regalismo", "Regicidio", "Relaciones subsistentes", "Renuncia", "Repartimiento",
    "Represalia", "República", "Republicanismo", "Reserva de ley", "Resistencia activa",
    "Resistencia pasiva", "Resignación", "Resurrección", "Retorsión", "Revelación",
    "Revolución", "Rigorismo", "Rito", "Rubrica", "Sacramento",
    "Sacerdocio común", "Sacerdocio ministerial", "Sacrificio eucarístico", "Salario justo", "Salvación",
    "Santificación", "Satisfacción", "Secularización", "Sedición", "Segunda escolástica",
    "Sensus fidelium", "Sentidos externos", "Sentidos internos", "Señorío", "Separación de poderes",
    "Silogismo", "Simonía", "Sínodo", "Soberanía", "Sociedad",
    "Sociedad civil", "Solidaridad", "Soteriología", "Subsidiariedad", "Subsistencia",
    "Substancia", "Suarismo", "Suspensión", "Sustancia", "Teleología",
    "Templanza", "Tentación", "Terra nullius", "Tiranía", "Tiranía de ejercicio",
    "Tiranía de origen", "Tiranicidio", "Tolerancia", "Tolerancia religiosa", "Tomismo",
    "Totalitarismo", "Traducianismo", "Tradición", "Transmigración", "Transubstanciación",
    "Tratado de paz", "Tratado internacional", "Trinidad", "Tropología", "Tuciorismo",
    "Ultimátum", "Unidad", "Unión hipostática", "Unión mística", "Unión personal",
    "Unión real", "Universales", "Usura", "Utilidad pública", "Valor",
    "Valor del trabajo", "Vasallaje", "Verdad", "Vía iluminativa", "Vía purgativa",
    "Vía unitiva", "Vicariato regio", "Vicio", "Vida activa", "Vida contemplativa",
    "Vida mixta", "Virtud", "Visión beatífica", "Voluntad", "Voto"
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
    genera una definición del concepto desde el punto de vista de al menos 5 autores relevantes de esta escuela. 
    Para cada autor, incluye su nombre, una breve definición o perspectiva sobre el concepto, y si es posible, una cita o referencia específica.
    Finaliza con una breve síntesis de las diferentes perspectivas.

    Información:
    {info}
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
