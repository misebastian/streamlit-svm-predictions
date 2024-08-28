import joblib
import streamlit as st
import pandas as pd

# Cargar el modelo guardado con joblib
model = joblib.load('best_logistic_model.pkl')

# Título de la aplicación
st.title("Predicción con Regresión Logística")

# Crear los inputs que coinciden con las características del modelo
Temp_C = st.number_input('Temp_C', value=0.0, format="%.2f")
Dew_Point_Temp_C = st.number_input('Dew Point Temp_C', value=0.0, format="%.2f")
Rel_Hum = st.number_input('Rel Hum_%', value=0)
Wind_Speed_km_h = st.number_input('Wind Speed_km/h', value=0)
Visibility_km = st.number_input('Visibility_km', value=0.0, format="%.2f")
Press_kPa = st.number_input('Press_kPa', value=0.0, format="%.2f")
Month = st.number_input('Month', value=1, min_value=1, max_value=12)
Day = st.number_input('Day', value=1, min_value=1, max_value=31)
Hour = st.number_input('Hour', value=0, min_value=0, max_value=23)

# Crear un botón para realizar la predicción
if st.button('Realizar Predicción'):
    # Asegurarse de que los nombres de las columnas coincidan exactamente con los usados durante el entrenamiento
    input_data = pd.DataFrame([[Temp_C, Dew_Point_Temp_C, Rel_Hum, Wind_Speed_km_h, Visibility_km, Press_kPa, Month, Day, Hour]],
                              columns=['Temp_C', 'Dew Point Temp_C', 'Rel Hum_%', 'Wind Speed_km/h', 'Visibility_km', 'Press_kPa', 'Month', 'Day', 'Hour'])

    # Realizar la predicción
    try:
        prediction = model.predict(input_data)
        st.write(f"La predicción es: {prediction[0]}")
    except Exception as e:
        st.write(f"Error al realizar la predicción: {e}")


