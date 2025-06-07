import streamlit as st
import pickle

st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://images.unsplash.com/photo-1541818270-3437299a4c5e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80") center center/cover no-repeat;
    }
    .main .block-container {
        background-color: rgba(245, 245, 220, 0.7); /* A translucent background for content */
        border-radius: 10px;
        padding: 30px;
        box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.3); /* Soft shadow for depth */
    }
    h1, h2, h3, h4, h5, h6 {
        color: #B8860B; /* Goldenrod for headings */
        font-family: 'Playfair Display', serif; /* A more elegant font if available */
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
    }
    label {
        color: #4A4A4A;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #B8860B; /* Goldenrod button */
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
    }
    .stButton>button:hover {
        background-color: #DAA520; /* Darker gold on hover */
        color: white;
    }
    .stSuccess {
        background-color: #e6ffe6;
        color: #006400;
        border-left: 5px solid #006400;
        padding: 10px;
        border-radius: 5px;
    }
    .stError {
        background-color: #ffe6e6;
        color: #8B0000;
        border-left: 5px solid #8B0000;
        padding: 10px;
        border-radius: 5px;
    }
    .stWarning {
        background-color: #fffacd;
        color: #FF8C00;
        border-left: 5px solid #FF8C00;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_resource
def load_model(model_path='streamlit\mimodelo.pkl'):
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        st.success(f"Modelo '{model_path}' cargado correctamente.")
        return model
    except FileNotFoundError:
        st.error(f"Error: No se encontró el archivo del modelo '{model_path}'.")
        st.warning("Asegúrate de que tu archivo .pkl esté en la misma carpeta que este script de Streamlit.")
        st.stop() 
    except Exception as e:
        st.error(f"Error al cargar el modelo desde '{model_path}': {e}")
        st.stop() 

# Llama a la función para cargar el modelo.
model = load_model('streamlit\mimodelo.pkl') 

# Header Section
st.title("🚢 SOBREVIVIRÁ?🥂")
st.markdown("---") 

st.markdown(
    """
    <p style='font-size: 1.1em; color: #4A4A4A;'>
    Inserta las características de tu pasajer/a y descubre si sobreviviría al accidente!
    </p>
    """, unsafe_allow_html=True
)
st.markdown("---")


# Slider para la Clase del Pasajero 
st.header("Clase del Pasajero")
pclass_mapping = {"Clase Alta": 1, "Clase Media": 2, "Clase Baja": 3}
selected_pclass_label = st.select_slider(
    "Selecciona la **Clase del Pasajero**",
    options=list(pclass_mapping.keys()),
    value="Clase Media"
)
pclass = pclass_mapping[selected_pclass_label]



# Selectbox para el Género 
sex_mapping = {"Hombre": 1, "Mujer": 0} 
selected_sex_label = st.selectbox(
    "Selecciona el **Género**",
    options=list(sex_mapping.keys())
)
sex = sex_mapping[selected_sex_label]



# Caja de texto para la Edad 
age = st.number_input(
    "Introduce la **Edad del Pasajero**",
    min_value=0,
    max_value=100,
    value=30, 
    step=1,
    help="La edad debe ser un número entre 0 y 100."
)



# Caja numérica para introducir el Fare
fare = st.number_input(
    "Introduce el **Precio del billete (Fare)**",
    min_value=0.0,
    max_value=600.0,
    value=30.0,
    step=0.01, # Son decimales, asi que steps pequeños
    help="La tarifa del billete (puede ser un valor decimal)."
)



# Selectbox para el Puerto de Embarque con One-Hot Encoding
st.subheader("Puerto de Embarque")
selected_embarked = st.selectbox(
    "Selecciona el **Puerto de Embarque**",
    options=["C (Cherbourg)", "Q (Queenstown)", "S (Southampton)"],
    index=2 
)

embarked_C = 0
embarked_Q = 0
embarked_S = 0

if selected_embarked == "C (Cherbourg)":
    embarked_C = 1
elif selected_embarked == "Q (Queenstown)":
    embarked_Q = 1
elif selected_embarked == "S (Southampton)":
    embarked_S = 1
    
    


# Predicción 

if st.button("¿Sobrevivirá?"):
    
    input_data = [pclass, sex, age, fare, embarked_C, embarked_Q, embarked_S]
    print(input_data)

    prediction = model.predict([input_data])
    prediction_proba = model.predict_proba([input_data])
    print(prediction)

    if prediction[0] == 1:
        st.success(f"¡El pasajero **SOBREVIVIRÁ** con una probabilidad del {prediction_proba[0][1]*100:.2f}%!")
    else:
        st.error(f"El pasajero **NO SOBREVIVIRÁ** con una probabilidad del {prediction_proba[0][0]*100:.2f}%!")
            
