import joblib
import streamlit as st
import pandas as pd
import time  # Para simular el tiempo de carga
import streamlit.components.v1 as components

# Datos predefinidos de media y desviación estándar
data = {
    'Temp_C': [8.798144, 11.687883],
    'Dew Point Temp_C': [2.555294, 10.883072],
    'Rel Hum_%': [67.431694, 16.918881],
    'Wind Speed_km/h': [14.945469, 8.688696],
    'Visibility_km': [27.664447, 12.622688],
    'Press_kPa': [101.051623, 0.844005]
}
df = pd.DataFrame(data, index=['mean', 'std'])

# Cargar el modelo guardado con joblib
model = joblib.load('naive_bayes_model.pkl')

# Título de la aplicación con un diseño más moderno y tecnológico
st.markdown("""
    <div style="background-color:#0D47A1;padding:10px;border-radius:10px">
        <h1 style='text-align: center; color: #FFFFFF;'>Predicción de Lluvia con Naive Bayes</h1>
        <p style='text-align: center; color: #BBDEFB;'>Universidad del Norte. Maestría en Estadística Aplicada. Machine Learning.</p>
        <p style='text-align: center; color: #BBDEFB;'>Miguel Herrera, Carlos López, Javier de Moya</p>
        <p style='text-align: center; color: #BBDEFB;'>30 de Agosto de 2024, Barranquilla.</p>
    </div>
""", unsafe_allow_html=True)

st.write("Por favor, introduce los valores a continuación:")

# Crear columnas para una mejor disposición visual
col1, col2 = st.columns(2)

with col1:
    Temp_C = st.number_input('Temperatura (°C)', value=None, format="%.2f")
    Dew_Point_Temp_C = st.number_input('Punto de Rocío (°C)', value=None, format="%.2f")
    Rel_Hum = st.number_input('Humedad Relativa (%)', value=None)
    Wind_Speed_km_h = st.number_input('Velocidad del Viento (km/h)', value=None)
    Visibility_km = st.number_input('Visibilidad (km)', value=None, format="%.2f")

with col2:
    Press_kPa = st.number_input('Presión Atmosférica (kPa)', value=None, format="%.2f")
    Month = st.number_input('Mes', value=1, min_value=1, max_value=12)
    Day = st.number_input('Día', value=1, min_value=1, max_value=31)
    Hour = st.number_input('Hora', value=0, min_value=0, max_value=23)

# Crear un botón para realizar la predicción
if st.button('Realizar Predicción'):
    # Insertar animación de cargando
    loading_html = """
    <div style="text-align: center;">
        <div class="loader"></div>
        <p style="color: #0D47A1;">Cargando... Por favor espera.</p>
    </div>

    <style>
    .loader {
        border: 16px solid #f3f3f3;
        border-radius: 50%;
        border-top: 16px solid #0D47A1;
        border-bottom: 16px solid #0D47A1;
        width: 120px;
        height: 120px;
        animation: spin 2s linear infinite;
        margin: auto;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    """
    
    # Mostrar la animación de carga mientras se realiza la predicción
    with st.empty():
        components.html(loading_html, height=200)
        time.sleep(2)  # Simular tiempo de carga
        
        # Definir los inputs en un DataFrame
        input_data = pd.DataFrame([[Temp_C, Dew_Point_Temp_C, Rel_Hum, Wind_Speed_km_h, Visibility_km, Press_kPa, Month, Day, Hour]],
                                  columns=['Temp_C', 'Dew Point Temp_C', 'Rel Hum_%', 'Wind Speed_km/h', 'Visibility_km', 'Press_kPa', 'Month', 'Day', 'Hour'])

        # Reemplazar valores faltantes con las medias predefinidas
        for column in ['Temp_C', 'Dew Point Temp_C', 'Rel Hum_%', 'Wind Speed_km/h', 'Visibility_km', 'Press_kPa']:
            if pd.isna(input_data[column][0]):
                input_data[column] = df.at['mean', column]

        # Estandarizar las columnas numéricas
        input_data[["Temp_C", "Dew Point Temp_C", "Rel Hum_%", "Wind Speed_km/h", "Visibility_km", "Press_kPa"]] = (input_data[["Temp_C", "Dew Point Temp_C", "Rel Hum_%", "Wind Speed_km/h", "Visibility_km", "Press_kPa"]] - df.loc['mean']) / df.loc['std']

        # Realizar la predicción
        prediction = model.predict(input_data)

    # Mostrar el resultado con un diseño más llamativo
    if prediction[0] == 1:
        st.markdown("<h2 style='text-align: center; color: #F44336;'>La predicción es: Sí llueve ☔</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align: center; color: #2196F3;'>La predicción es: No llueve 🌞</h2>", unsafe_allow_html=True)
