import streamlit as st 
import read_data # Ergänzen Ihr eigenes Modul
from PIL import Image
import read_pandas

tab1, tab2 = st.tabs(["Versuchsperson", "Plot"])

with tab1:
    st.write("# EKG APP")   
    st.write("## Versuchsperson auswählen")

    person_dict = read_data.load_person_data()
    person_data = read_data.get_person_list()

# Session State wird leer angelegt, solange er noch nicht existiert
    if 'current_user' not in st.session_state:
        st.session_state.current_user = 'None'
        st.write("Benutzername: ", "Hannah und Marie")
        
    st.session_state.current_user = st.selectbox(
        'Versuchsperson',
        options = person_data, key="sbVersuchsperson")

# Anlegen des Session State. Bild, wenn es kein Bild gibt
    if 'picture_path' not in st.session_state:
        st.session_state.picture_path = 'data/pictures/none.jpg'

# Suche den Pfad zum Bild, aber nur wenn der Name bekannt ist
    if st.session_state.current_user in person_data:
        st.session_state.picture_path = read_data.find_person_data_by_name(st.session_state.current_user)["picture_path"]

# Öffne das Bild und Zeige es an
    image = Image.open(st.session_state.picture_path)
    st.image(image, caption=st.session_state.current_user)


with tab2:
    st.write("# EKG APP")   
    st.write("## Plot")

    person_dict = read_data.load_person_data()
    person_data = read_data.get_person_list()

    # Wenn der Benutzername nicht gesetzt ist, dann kann auch kein Plot angezeigt werden
    if st.session_state.current_user == 'None':
        st.write("Bitte zuerst eine Versuchsperson auswählen!")
    else:
        # Lese die Daten der ausgewählten Person
        df = read_pandas.read_my_csv()
        #Berechne max HR im Datensatz
        max_hr = int(df["HeartRate"].max())

        # HR eingabefeld
        hf_max = int(st.number_input(
            'Maximale Herzfrequenz',
            min_value=100,
            max_value=230,
            value=max_hr,  # Standardwert ist der Maximalwert im Datensatz
            step=1
        ))

        # Lese die Daten der ausgewählten Person
        
        df, zones = read_pandas.heart_rate_zone(df, hf_max)
        fig_activity = read_pandas.make_plot(df, zones)
        st.plotly_chart(fig_activity, use_container_width=True)  # Zeigt den Plot in Streamlit an
    
    st.write("Maximale Power:", read_pandas.max_mean_power(df)[0])
    st.write("Mittlere Power:", read_pandas.max_mean_power(df)[1])