import joblib
import streamlit as st
import pandas as pd

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

    # Mostrar el resultado con animaciones
    if prediction[0] == 1:
        st.markdown("""
        <div style='text-align: center;'>
            <h2 style='color: #F44336;'>La predicción es: Sí llueve ☔</h2>
            <div class="cloud">
                <div class="rain"></div>
                <div class="rain"></div>
                <div class="rain"></div>
            </div>
        </div>

        <style>
        .cloud {
            position: relative;
            background: #444;
            width: 200px;
            height: 60px;
            margin: 20px auto;
            border-radius: 100px;
        }

        .cloud:before, .cloud:after {
            content: '';
            position: absolute;
            background: #444;
            width: 100px;
            height: 80px;
            position: absolute;
            top: -40px;
            border-radius: 100px;
        }

        .cloud:before {
            left: 10px;
        }

        .cloud:after {
            right: 10px;
        }

        .rain {
            position: absolute;
            width: 2px;
            height: 10px;
            background: #0D47A1;
            bottom: -20px;
            left: 50%;
            margin-left: -1px;
            animation: rain 0.5s infinite linear;
        }

        .rain:nth-child(2) {
            left: 60%;
            animation-delay: 0.3s;
        }

        .rain:nth-child(3) {
            left: 40%;
            animation-delay: 0.6s;
        }

        @keyframes rain {
            0% { transform: translateY(0); }
            100% { transform: translateY(20px); }
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='text-align: center;'>
            <h2 style='color: #2196F3;'>La predicción es: No llueve 🌞</h2>
            <div class="sun"></div>
        </div>

        <style>
        .sun {
            position: relative;
            background: #FFEB3B;
            width: 100px;
            height: 100px;
            margin: 20px auto;
            border-radius: 50%;
            box-shadow: 0 0 50px #FFEB3B;
        }

        .sun:before, .sun:after {
            content: '';
            position: absolute;
            background: #FFEB3B;
            width: 80px;
            height: 20px;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(45deg);
        }

        .sun:after {
            width: 20px;
            height: 80px;
        }
        </style>
        """, unsafe_allow_html=True)
