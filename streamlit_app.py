import numpy as np
import streamlit as st
import streamlit_authenticator as stauth
import yaml
import pymongo

# Connect to the MongoDB database
client = pymongo.MongoClient("mongodb+srv://equipo3:password3@cluster0.gkaurda.mongodb.net/?retryWrites=true&w=majority")

db = client["test1"]

studentProject = db["collection1"]
projects = db["collection2"]
cursor = projects.find()

db2 = client["DireccionSS"]
students = db2["students"]

projects = []
for document in cursor:
    project_id = document["projectID"]
    projects.append(project_id)    

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
    st.write(f'Bienvenido *{name}*')
    studentID = st.text_input('Matrícula')
    if studentID:
        document = students.find_one({"studentID": studentID})
        if document:
            name = document["name"]
            major = document["major"]
            st.text_input("Name", name)
            st.text_input("Major", major)
        else:
            st.error("No se ha encontrado el estudiante")
    option = st.selectbox(
    'Elige el proyecto', projects)
    if st.button('Enviar'):
        st.write('Enviado')
        document = {
        "studentID": title,
        "projectID": option
        }
        studentProject.insert_one(document)

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')