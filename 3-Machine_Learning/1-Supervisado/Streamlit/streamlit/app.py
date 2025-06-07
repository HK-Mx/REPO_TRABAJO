import streamlit as st

st.set_page_config(
    page_title="My App",
    page_icon="😎",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
st.title("My App!!!")
st.title("Uyuyuyuyuy :blue[cool] :sunglasses:")

import streamlit as st

saludo = st.button("Saludar", type="primary")


if saludo:
    st.markdown('''
    :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
    :gray[pretty] :rainbow[colors] and :blue-background[highlight] text.''')
    

col1, col2 = st.columns([3,1])
with col1:
    input_1 = st.selectbox(
    "How would you like to be contacted?",
    range(0,10)
    )
with col2:
    input_2 = st.selectbox(
    "How would you like",
    range(0,10)
    )
st.sidebar.markdown('''
    :rainbow[Yeeepa] ''')


def modelo(input_1, input_2):
    # suma = input_1+input_2
    # loco = input_1+suma**3
    if int(input_1) + int(input_2) > 25:
        return "perro"
    else: 
        return "rinoceronte"
    

# input_1 = st.number_input("Cuantas colas tiene er bisho?", 1,100,2)
# input_2 = st.number_input("Cuanto apesta el bisho", 1,100,6 ) #min,max,default

predict_button = st.button("Predict!")
if predict_button:
    st.markdown(modelo(input_1,input_2))




