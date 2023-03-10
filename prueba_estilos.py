import streamlit as st

#Configuración básica de la página com el título, el ícono (que se
#pone como un emoji), que tan grande quieres que sea el layout, etc.
st.set_page_config(
    page_title="Equipo 3",
    page_icon=":art:",
    layout="wide",
    initial_sidebar_state="expanded",  
)

#Cambiar el estilo de la página utilizando CSS
st.markdown(
    """
    <style>
        /* Add your CSS styles here */
        body {
            background-color: #f5f5f5;
            font-family: 'Helvetica', sans-serif;
        }

	p {
	    background-image: url(‘img_file.jpg’);
  	}

        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .stButton button {
            background-color: #ff8c00;
            color: #fff;
            border-radius: 5px;
            border-color: #ff8c00;
            padding: 10px 20px;
        }
        .stTextInput input[type="text"] {
            border-radius: 5px;
            border-color: #ff8c00;
            padding: 10px 20px;
            font-size: 18px;
        }
        .stTextArea textarea {
            border-radius: 5px;
            border-color: #ff8c00;
            padding: 10px 20px;
            font-size: 18px;
        }
        .stSelectbox select {
            border-radius: 5px;
            border-color: #ff8c00;
            padding: 10px 20px;
            font-size: 18px;
            background-color: #fff;
            color: #000;
        }
        .stCheckbox label {
            color: #000;
            font-size: 18px;
        }
        .stRadio label {
            color: #000;
            font-size: 18px;
        }
        .stNumberInput input[type="number"] {
            border-radius: 5px;
            border-color: #ff8c00;
            padding: 10px 20px;
            font-size: 18px;
        }
        .stSlider {
            background-color: #ffffff;
        }
        .stTable td, .stTable th {
            font-size: 18px;
        }
    </style>
""",
    unsafe_allow_html=True,
)

#Ejemplo de app para mostrar los cambios dependiendo del estilo escogido
def main():
    st.title("App de Prueba")
    st.write("Elementos de UI personalizables:")

    #Ejemplos de widgets de streamlit
    st.header("Botones")
    st.write("Este es un botón personalizable:")
    st.button("Presióname!")

    st.header("Inputs de texto")
    st.write("Este es un input de texto personalizable:")
    st.text_input("Pon tu nombre aquí:")

    st.header("Área de Texto")
    st.write("Esta es un área de texto personalizable:")
    st.text_area("Enter your message here:")

    st.header("Select box")
    st.write("Este es un select box personalizable:")
    st.selectbox("Selecciona una opción:", ["Opción 1", "Opción 2", "Opción 3"])

    st.header("Checkboxes")
    st.write("Este es un checkbox personalizable:")
    st.checkbox("Márcame")

    st.header("Opciones Múltiples")
    st.radio("Selecciona una opción:", ["Opción 1", "Opción 2", "Opción 3"])

    st.header("Inputs numéricos")
    st.write("Este es un input numérico personalizable:")
    st.number_input("Pon un número:", min_value=0, max_value=100)

    st.header("Slider")
    st.write("Este es un slider personalizable")
    st.slider("Desliza para seleccionar un valor:", 0, 100)

main()
