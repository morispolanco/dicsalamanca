import streamlit as st
import requests

# Cargar las claves API desde los secretos de Streamlit
serper_api_key = st.secrets["SERPER_API_KEY"]
together_api_key = st.secrets["TOGETHER_API_KEY"]

# Título de la aplicación
st.title("Definición de Conceptos desde la Escuela de Salamanca")

# Input para el concepto que el usuario quiere definir
concepto = st.text_input("Introduce el concepto que deseas definir:")

# Información sobre los miembros de la Escuela de Salamanca
escuela_salamanca = {
    "Primer grupo": [
        "Arias Piñel (1512-1563)", "Antonio de Padilla y Meneses (-1580)", "Bartolomé de Albornoz (1519-1573)",
        "Bartolomé de Medina (1527-1581)", "Diego de Chaves (1507-1592)", "Diego de Covarrubias (1512-1577)",
        "Diego Pérez de Mesa (1563-1632)", "Domingo Báñez (1528-1604)", "Domingo de Soto (1494-1560)",
        "Fernán Pérez de Oliva (1494-1531)", "Francisco de Vitoria (1492-1546)", "Francisco Sarmiento de Mendoza (1525-1595)",
        "Francisco Suárez (1548-1617)", "Gregorio de Valencia (1549-1603)", "Jerónimo Muñoz (1520-1591)",
        "Juan de Horozco y Covarrubias (1540-1610)", "Juan de la Peña (1513-1565)", "Juan de Matienzo (1520-1579)",
        "Juan de Ribera (1532-1611)", "Juan Gil de la Nava (-1551)", "Leonardus Lessius (1554-1623)",
        "Luis de León (1527-1591)", "Martín de Azpilcueta (1492-1586)", "Martín de Ledesma (1509-1574)",
        "Melchor Cano (1509-1560)", "Pedro de Sotomayor (1511-1564)", "Tomás de Mercado (1523-1575)"
    ],
    "Segundo grupo": [
        "Alonso de la Vera Cruz (1507-1584)", "Cristóbal de Villalón (-1588)", "Fernando Vázquez de Menchaca (1512​-1569)",
        "Francisco Cervantes de Salazar (1513/18-1575)", "Juan de Lugo y Quiroga (1583-1660)", "Juan de Salas (1553-1612)",
        "Luis de Molina (1535-1600)", "Pedro de Aragón (1545/46-1592)", "Pedro de Valencia (1555-1620)"
    ],
    "Tercer grupo": [
        "Antonio de Hervías (-1590)", "Bartolomé de Carranza (1503-1576)", "Bartolomé de las Casas (1484-1566)",
        "Cristóbal de Fonseca (1550-1621)", "Domingo de Salazar (1512-1594)", "Domingo de Santo Tomás (1499-1570)",
        "Gabriel Vásquez (1549-1604)", "Gómez Pereira (1500–1567)", "Juan de Mariana (1536-1624)", 
        "Juan de Medina (1489-1545)", "Juan Pérez de Menacho (1565-1626)", "Luis de Alcalá (1490-1549)", 
        "Luis Saravia de la Calle (?)", "Miguel Bartolomé Salón (1539-1621)", "Pedro de Fonseca (1528-1599)",
        "Pedro de Oñate (1567-1646)", "Rodrigo de Arriaga (1592-1667)"
    ]
}

# Mostrar información sobre los grupos
st.sidebar.header("Grupos de la Escuela de Salamanca")
for grupo, miembros in escuela_salamanca.items():
    with st.sidebar.expander(grupo):
        st.write("\n".join(miembros))

# Botón para generar la definición
if st.button("Generar Definición"):
    if concepto:
        # Consulta a la API de Serper para buscar información relevante
        serper_response = requests.get(
            "https://google.serper.dev/search",  # Reemplaza con el endpoint adecuado
            headers={"Authorization": f"Bearer {serper_api_key}"},
            params={"q": concepto, "num_results": 5}
        )

        # Procesar la respuesta de Serper
        serper_data = serper_response.json()
        definiciones = [item['snippet'] for item in serper_data['results']]

        # Usar la API de Together para refinar la definición y citar autores de la Escuela de Salamanca
        prompt = f"Define el concepto '{concepto}' desde el punto de vista de autores de la Escuela de Salamanca y cita fuentes relevantes. Los autores pueden incluir: {', '.join(escuela_salamanca['Primer grupo'])}, {', '.join(escuela_salamanca['Segundo grupo'])}, {', '.join(escuela_salamanca['Tercer grupo'])}."
        together_response = requests.post(
            "https://api.together.xyz/v1/chat/completions",  # Reemplaza con el endpoint adecuado
            headers={"Authorization": f"Bearer {together_api_key}"},
            json={"prompt": prompt, "temperature": 0.7}
        )

        # Mostrar la definición generada
        if together_response.status_code == 200:
            definicion = together_response.json()["choices"][0]["text"]
            st.subheader(f"Definición de '{concepto}':")
            st.write(definicion)
        else:
            st.error("Error al generar la definición. Por favor, intenta de nuevo.")
    else:
        st.warning("Por favor, introduce un concepto.")
