import streamlit as st
import pandas as pd

# Configurar el diseño en modo amplio
st.set_page_config(layout="wide")

# Cargar datos
def load_data():
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

# Extraer apellido de los pasajeros
df["LastName"] = df["Name"].apply(lambda x: x.split(",")[0])

# Interfaz de la app
st.title("🚢 Explorador de Pasajeros del Titanic")
st.markdown("**Filtre y explore los datos de los pasajeros del Titanic con una interfaz intuitiva y mejorada.**")

# Filtros de selección con estilo
gender_filter = st.selectbox("🎭 Seleccione Género", ["Todos"] + df["Sex"].unique().tolist())
class_filter = st.selectbox("🏷️ Seleccione Clase", ["Todas"] + df["Pclass"].astype(str).unique().tolist())
family_filter = st.slider("👨‍👩‍👧 Número de Familiares a Bordo", 0, df["SibSp"].max() + df["Parch"].max(), (0, df["SibSp"].max() + df["Parch"].max()))

# Slider para filtrar por tarifa de pasaje
fare_min, fare_max = df["Fare"].min(), df["Fare"].max()
fare_filter = st.slider("💰 Rango de Tarifa del Pasaje", float(fare_min), float(fare_max), (float(fare_min), float(fare_max)))

# Aplicar filtros
filtered_df = df.copy()
if gender_filter != "Todos":
    filtered_df = filtered_df[filtered_df["Sex"] == gender_filter]
if class_filter != "Todas":
    filtered_df = filtered_df[filtered_df["Pclass"].astype(str) == class_filter]
filtered_df = filtered_df[(filtered_df["SibSp"] + filtered_df["Parch"]).between(family_filter[0], family_filter[1])]
filtered_df = filtered_df[filtered_df["Fare"].between(fare_filter[0], fare_filter[1])]

# Lista desplegable para seleccionar pasajero
passenger_names = filtered_df["Name"].tolist()
selected_passenger = st.selectbox("🔎 Busque un Pasajero", passenger_names)

# Filtrar datos del pasajero seleccionado
passenger_data = filtered_df[filtered_df["Name"] == selected_passenger].iloc[0]

# Filtrar familiares del pasajero seleccionado
family_data = df[(df["LastName"] == passenger_data["LastName"]) & (df["Name"] != passenger_data["Name"])]

# Mostrar detalles del pasajero con emojis
st.subheader("🛳️ Detalles del Pasajero")
st.write(f"**👤 Nombre:** {passenger_data['Name']}")
st.write(f"**📅 Edad:** {passenger_data['Age'] if pd.notna(passenger_data['Age']) else 'Desconocida'}")
st.write(f"**🎟️ Clase:** {passenger_data['Pclass']}")
st.write(f"**💰 Tarifa:** {passenger_data['Fare']}")
st.write(f"**🩸 Sobrevivió:** {'✅ Sí' if passenger_data['Survived'] == 1 else '❌ No'}")
st.write(f"**👨‍👩‍👧 Familiares a bordo:** {passenger_data['SibSp'] + passenger_data['Parch']}")

# Mostrar información de los familiares si existen
if not family_data.empty:
    st.subheader("👨‍👩‍👧 Familiares a Bordo")
    for _, row in family_data.iterrows():
        st.write(f"- **👤 Nombre:** {row['Name']} | **🩸 Sobrevivió:** {'✅ Sí' if row['Survived'] == 1 else '❌ No'}")

# Requerimientos para la app
txt_requeriments = """
streamlit
pandas
"""
with open("requirements.txt", "w") as f:
    f.write(txt_requeriments)
