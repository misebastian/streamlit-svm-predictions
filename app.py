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
model = joblib.load('best_logistic_model.pkl')

# Título de la aplicación
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Predicción de Lluvia con Naive Bayes</h1>", unsafe_allow_html=True)
st.write("Por favor, introduce los valores a continuación:")

# Crear columnas para una mejor disposición visual
col1, col2 = st.columns(2)

with col1:
    Temp_C = st.number_input('Temp_C', value=None, format="%.2f")
    Dew_Point_Temp_C = st.number_input('Dew Point Temp_C', value=None, format="%.2f")
    Rel_Hum = st.number_input('Rel Hum_%', value=None)
    Wind_Speed_km_h = st.number_input('Wind Speed_km/h', value=None)
    Visibility_km = st.number_input('Visibility_km', value=None, format="%.2f")

with col2:
    Press_kPa = st.number_input('Press_kPa', value=None, format="%.2f")
    Month = st.number_input('Month', value=1, min_value=1, max_value=12)
    Day = st.number_input('Day', value=1, min_value=1, max_value=31)
    Hour = st.number_input('Hour', value=0, min_value=0, max_value=23)

# Crear un botón para realizar la predicción
if st.button('Realizar Predicción'):
    # Definir los inputs en un DataFrame
    input_data = pd.DataFrame([[Temp_C, Dew_Point_Temp_C, Rel_Hum, Wind_Speed_km_h, Visibility_km, Press_kPa, Month, Day, Hour]],
                              columns=['Temp_C', 'Dew Point Temp_C', 'Rel Hum_%', 'Wind Speed_km/h', 'Visibility_km', 'Press_kPa', 'Month', 'Day', 'Hour'])

    # Reemplazar valores faltantes con las medias predefinidas
    for column in ['Temp_C', 'Dew Point Temp_C', 'Rel Hum_%', 'Wind Speed_km/h', 'Visibility_km', 'Press_kPa']:
        if pd.isna(input_data[column][0]):
            input_data[column] = df.at['mean', column]
    
    # Estandarizar las columnas numéricas en una sola línea
    input_data[["Temp_C", "Dew Point Temp_C", "Rel Hum_%", "Wind Speed_km/h", "Visibility_km", "Press_kPa"]] = (input_data[["Temp_C", "Dew Point Temp_C", "Rel Hum_%", "Wind Speed_km/h", "Visibility_km", "Press_kPa"]] - df.loc['mean']) / df.loc['std']

    # Realizar la predicción
    prediction = model.predict(input_data)

    # Mostrar el resultado con un mensaje más claro
    if prediction[0] == 1:
        st.markdown("<h2 style='text-align: center; color: red;'>La predicción es: Sí llueve ☔</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align: center; color: blue;'>La predicción es: No llueve 🌞</h2>", unsafe_allow_html=True)
