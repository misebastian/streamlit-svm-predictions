import streamlit as st
import pickle
import pandas as pd

# Cargar el modelo guardado
with open('best_logistic_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Título de la aplicación
st.title("Predicción con Regresión Logística")

# Crear los inputs que coinciden con las características del modelo
Temp_C = st.number_input('Temp_C')
Dew_Point_Temp_C = st.number_input('Dew Point Temp_C')
Rel_Hum = st.number_input('Rel Hum %')
Wind_Speed_km_h = st.number_input('Wind Speed km/h')
Visibility_km = st.number_input('Visibility km')
Press_kPa = st.number_input('Press kPa')
Month = st.number_input('Month')
Day = st.number_input('Day')
Hour = st.number_input('Hour')

# Crear un botón para realizar la predicción
if st.button('Realizar Predicción'):
    # Crear un DataFrame con los valores introducidos
    input_data = pd.DataFrame([[Temp_C, Dew_Point_Temp_C, Rel_Hum, Wind_Speed_km_h, Visibility_km, Press_kPa, Month, Day, Hour]],
                              columns=['Temp_C', 'Dew Point Temp_C', 'Rel Hum %', 'Wind Speed_km/h', 'Visibility_km', 'Press_kPa', 'Month', 'Day', 'Hour'])
    
    # Realizar la predicción
    prediction = model.predict(input_data)
    
    # Mostrar el resultado
    st.write(f"La predicción es: {prediction[0]}")
