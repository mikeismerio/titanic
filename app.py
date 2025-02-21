import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Configurar el diseño en modo amplio
st.set_page_config(layout="wide")

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

# Extraer apellido de los pasajeros
df["LastName"] = df["Name"].apply(lambda x: x.split(",")[0])

# Interfaz de la app
st.title("🌍 Mapa Interactivo de Pasajeros del Titanic")
st.write("Seleccione filtros para explorar los datos y visualizar detalles de los pasajeros.")

# Filtros de selección
gender_filter = st.selectbox("Seleccione Género", ["Todos"] + df["Sex"].unique().tolist())
class_filter = st.selectbox("Seleccione Clase", ["Todas"] + df["Pclass"].astype(str).unique().tolist())
family_filter = st.slider("Número de Familiares a Bordo", 0, df["SibSp"].max() + df["Parch"].max(), (0, df["SibSp"].max() + df["Parch"].max()))

# Aplicar filtros
filtered_df = df.copy()
if gender_filter != "Todos":
    filtered_df = filtered_df[filtered_df["Sex"] == gender_filter]
if class_filter != "Todas":
    filtered_df = filtered_df[filtered_df["Pclass"].astype(str) == class_filter]
filtered_df = filtered_df[(filtered_df["SibSp"] + filtered_df["Parch"]).between(family_filter[0], family_filter[1])]

# Mapa Global con los pasajeros filtrados
st.subheader("🌍 Mapa Global de Procedencia de Pasajeros Filtrados")
def create_filtered_map(data):
    m = folium.Map(location=[51.0, -10.0], zoom_start=3)
    
    for _, row in data.iterrows():
        embarkation = row["Embarked"]
        if embarkation in embark_coords:
            lat, lon = embark_coords[embarkation]
            popup_info = f"""
            <b>Nombre:</b> {row['Name']}<br>
            <b>Clase:</b> {row['Pclass']}<br>
            <b>Tarifa:</b> {row['Fare']}<br>
            <b>Sobrevivió:</b> {'Sí' if row['Survived'] == 1 else 'No'}<br>
            """
            folium.Marker(location=[lat, lon], popup=popup_info, 
                          icon=folium.Icon(color='green' if row['Survived'] == 1 else 'red')).add_to(m)
    
    return m

filtered_map = create_filtered_map(filtered_df)
folium_static(filtered_map)

# Lista desplegable para seleccionar pasajero
passenger_names = filtered_df["Name"].tolist()
selected_passenger = st.selectbox("Seleccione un pasajero", passenger_names)

# Filtrar datos del pasajero seleccionado
passenger_data = filtered_df[filtered_df["Name"] == selected_passenger].iloc[0]

# Filtrar familiares del pasajero seleccionado
family_data = df[(df["LastName"] == passenger_data["LastName"]) & (df["Name"] != passenger_data["Name"])]

# Mostrar detalles del pasajero
st.subheader("🧑‍💼 Detalles del Pasajero")
st.write(f"**Nombre:** {passenger_data['Name']}")
st.write(f"**Edad:** {passenger_data['Age'] if pd.notna(passenger_data['Age']) else 'Desconocida'}")
st.write(f"**Clase:** {passenger_data['Pclass']}")
st.write(f"**Tarifa:** {passenger_data['Fare']}")
st.write(f"**Sobrevivió:** {'Sí' if passenger_data['Survived'] == 1 else 'No'}")
st.write(f"**Familiares a bordo:** {passenger_data['SibSp'] + passenger_data['Parch']}")

# Mostrar información de los familiares si existen
if not family_data.empty:
    st.subheader("👨‍👩‍👧 Familiares a Bordo")
    for _, row in family_data.iterrows():
        st.write(f"- **Nombre:** {row['Name']} | **Sobrevivió:** {'Sí' if row['Survived'] == 1 else 'No'}")

# Crear mapa interactivo individual
st.subheader("📍 Ubicación del Pasajero Seleccionado")
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
