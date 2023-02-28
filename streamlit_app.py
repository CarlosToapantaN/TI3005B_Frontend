import streamlit as st
import streamlit_authenticator as stauth
import yaml

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    title = st.text_input('Matrícula')
    option = st.selectbox(
    'Elige el proyecto',
    ('Proyecto 1', 'Proyecto 2', 'Proyecto 3'))
    if st.button('Enviar'):
        st.write('Enviado')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')