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

def create_map(data):
    m = folium.Map(location=[51.0, -10.0], zoom_start=3)
    
    for _, row in data.iterrows():
        embarkation = row["Embarked"]
        if embarkation in embark_coords:
            lat, lon = embark_coords[embarkation]
            popup_info = f"""
            <b>Nombre:</b> {row['Name']}<br>
            <b>Edad:</b> {row['Age'] if pd.notna(row['Age']) else 'Desconocida'}<br>
            <b>Clase:</b> {row['Pclass']}<br>
            <b>Tarifa:</b> {row['Fare']}<br>
            <b>Sobrevivió:</b> {'Sí' if row['Survived'] == 1 else 'No'}<br>
            <b>Familiares a bordo:</b> {row['SibSp'] + row['Parch']}
            """
            folium.Marker(location=[lat, lon], popup=popup_info, 
                          icon=folium.Icon(color='green' if row['Survived'] == 1 else 'red')).add_to(m)
    
    return m

# Interfaz de la app
st.title("🌍 Mapa Interactivo de Pasajeros del Titanic")
st.write("Este mapa muestra la procedencia de los pasajeros del Titanic y sus detalles.")

# Crear mapa interactivo
mapa = create_map(df)
folium_static(mapa)
