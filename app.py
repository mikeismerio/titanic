import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Cargar datos
def load_data():
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

# Mapeo de ciudades de embarque a coordenadas
embark_coords = {
    "C": (49.2965, -0.7054),  # Cherburgo, Francia
    "Q": (53.3331, -3.0088),  # Queenstown, Irlanda
    "S": (50.9049, -1.4043)   # Southampton, Reino Unido
}

# Interfaz de la app
st.title("🌍 Mapa Interactivo de Pasajeros del Titanic")
st.write("Seleccione un pasajero para ver sus detalles y ubicación en el mapa.")

# Lista desplegable para seleccionar pasajero
passenger_names = df["Name"].tolist()
selected_passenger = st.selectbox("Seleccione un pasajero", passenger_names)

# Filtrar datos del pasajero seleccionado
passenger_data = df[df["Name"] == selected_passenger].iloc[0]

# Mostrar detalles del pasajero
st.write(f"**Nombre:** {passenger_data['Name']}")
st.write(f"**Edad:** {passenger_data['Age'] if pd.notna(passenger_data['Age']) else 'Desconocida'}")
st.write(f"**Clase:** {passenger_data['Pclass']}")
st.write(f"**Tarifa:** {passenger_data['Fare']}")
st.write(f"**Sobrevivió:** {'Sí' if passenger_data['Survived'] == 1 else 'No'}")
st.write(f"**Familiares a bordo:** {passenger_data['SibSp'] + passenger_data['Parch']}")

# Crear mapa interactivo
def create_map(data):
    m = folium.Map(location=[51.0, -10.0], zoom_start=3)
    
    embarkation = data["Embarked"]
    if embarkation in embark_coords:
        lat, lon = embark_coords[embarkation]
        popup_info = f"""
        <b>Nombre:</b> {data['Name']}<br>
        <b>Edad:</b> {data['Age'] if pd.notna(data['Age']) else 'Desconocida'}<br>
        <b>Clase:</b> {data['Pclass']}<br>
        <b>Tarifa:</b> {data['Fare']}<br>
        <b>Sobrevivió:</b> {'Sí' if data['Survived'] == 1 else 'No'}<br>
        <b>Familiares a bordo:</b> {data['SibSp'] + data['Parch']}
        """
        folium.Marker(location=[lat, lon], popup=popup_info, 
                      icon=folium.Icon(color='green' if data['Survived'] == 1 else 'red')).add_to(m)
    
    return m

mapa = create_map(passenger_data)
folium_static(mapa)

# Requerimientos para la app
txt_requeriments = """
streamlit
pandas
folium
streamlit-folium
"""
with open("requirements.txt", "w") as f:
    f.write(txt_requeriments)
