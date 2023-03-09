import numpy as np
import streamlit as st
import streamlit_authenticator as stauth
import yaml
import pymongo
from datetime import datetime
import pandas as pd

# Connect to the MongoDB database
client = pymongo.MongoClient("mongodb+srv://equipo3:password3@cluster0.gkaurda.mongodb.net/?retryWrites=true&w=majority")

stremlit_db = client["streamlitApp"]

enrolled_students = stremlit_db["enrolledStudents"]
social_service_db = client["DireccionSS"]
students = social_service_db["students"]
partner_projects = social_service_db["partnerProjects"]
projects_collection = social_service_db["projects"]

def overlap(start1, end1, start2, end2):
    return start1 <= end2 and end1 >= start2

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
    if username == "socioformador1":
        partner_id = "SF246543"
    elif username == "socioformador2":
        partner_id = "SF680682"

    partner_project_doc = partner_projects.find_one({"partnerID": partner_id})
    st.write(f'Bienvenido *{name}*')
    tab1, tab2 = st.tabs(["Inscribir", "Ver Estudiantes Inscritos"])
    with tab1:
        studentID = st.text_input('**Matrícula**')
        projects = partner_project_doc["projectsIDs"]
        if studentID:
            document = students.find_one({"studentID": studentID})
            if document:
                name = document["name"]
                major = document["major"]
                hasInductionWeek = document["hasInductionWeek"]
                if hasInductionWeek:
                    hasIW = "Sí"
                else:
                    hasIW = "No"
                st.write("Nombre: ", name)
                st.write("Carrera: ", major)
                st.write("Requisito Semana Inducción: ", hasIW)
            else:
                st.error("No se ha encontrado el estudiante")
        option = st.selectbox(
        '**Elige el proyecto**', [""]+projects)
        if option:
            selected_project = projects_collection.find_one({"projectID": option})
            project_name = selected_project["name"]
            project_start_date = selected_project["startDate"].strftime("%d/%m/%Y")
            project_end_date = selected_project["endDate"].strftime("%d/%m/%Y")

            st.write("Nombre: ", project_name)
            st.write("Fecha de Inicio: ", project_start_date)
            st.write("Fecha de Fin: ", project_end_date)

        if st.button('Enviar'):
            if not studentID:
                st.error("Por favor escribe la matrícula del estudiante")
            elif not option:
                st.error("Por favor selecciona un proyecto")
            else:   
                existing_record = enrolled_students.find_one({"studentID": studentID})
                new_project = projects_collection.find_one({"projectID": option})

                if existing_record:
                    existing_project = projects_collection.find_one({"projectID": existing_record["projectID"]})
                    start1 = existing_project["startDate"]
                    end1 = existing_project["endDate"]
                    start2 = new_project["startDate"]
                    end2 = new_project["endDate"]

                if existing_record and overlap(start1, end1, start2, end2):
                    st.error("El estudiante ya tiene un proyecto asignado durante este periodo")
                elif not hasInductionWeek:
                    st.error("El alumno no cumple con el requisito de semana de inducción")
                elif new_project["quota"] <= 0:
                    st.error("El proyecto ha llegado al límite de estudiantes")
                else:
                    st.write('Enviado')
                    document = {
                    "studentID": studentID,
                    "projectID": option
                    }
                    enrolled_students.insert_one(document)
                    result = projects_collection.update_one(
                            {"projectID": option},
                            {"$inc": {"quota": -1}}
                        )
    with tab2:
        # Create a sample dataframe
        students_data = []
        for student in enrolled_students.find({}, {'_id': 0}):
            students_data.append(student)
        df = pd.DataFrame(students_data)
        df.columns = ['Matrícula', 'Proyecto']
        df.index += 1
        st.table(df[['Matrícula', 'Proyecto']])

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')