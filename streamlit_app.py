import numpy as np
import streamlit as st
import streamlit_authenticator as stauth
import yaml
import pymongo

# Connect to the MongoDB database
client = pymongo.MongoClient("mongodb+srv://equipo3:password3@cluster0.gkaurda.mongodb.net/?retryWrites=true&w=majority")

db = client["test1"]

studentProject = db["collection1"]
db2 = client["DireccionSS"]
students = db2["students"]
#projects = db2["projects"]
partnerProjects = db2["partnerProjects"]
projects_collection = db2["projects"]

partner_id = "SF246543"
partner_project_doc = partnerProjects.find_one({"partnerID": partner_id})

projects = partner_project_doc["projectsIDs"]

def overlap(start1, end1, start2, end2):
    return start1 <= end2 and end1 >= start2

if partner_project_doc:
    # get the list of projectIDs for that partner
    projects = partner_project_doc["projectsIDs"]
else:
    print(f"No document found for partner ID {partner_id}")

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
            hasInductionWeek = document["hasInductionWeek"]
            if hasInductionWeek:
                hasIW = "Sí"
            else:
                hasIW = "No"
            st.text_input("Nombre", name)
            st.text_input("Carrera", major)
            st.text_input("Requisito Semana Inducción", hasIW)
        else:
            st.error("No se ha encontrado el estudiante")
    option = st.selectbox(
    'Elige el proyecto', projects)
    if st.button('Enviar'):
        existing_record = studentProject.find_one({"studentID": studentID})
        new_project = projects_collection.find_one({"projectID": option})
        print(new_project)
        print(existing_record)

        if existing_record:
            existing_project = projects_collection.find_one({"projectID": existing_record["projectID"]})
            print(existing_project)
            start1 = existing_project["startDate"]
            end1 = existing_project["endDate"]
            start2 = new_project["startDate"]
            end2 = new_project["endDate"]
            print(start1,end1,start2,end2)

        if existing_record and overlap(start1, end1, start2, end2):
            st.error("Este estudiante ya tiene un proyecto asignado durante este periodo")
        elif not hasInductionWeek:
            st.error("Este alumno no cumple con el requisito de semana de inducción")
        elif new_project["quota"] <= 0:
            st.error("El proyecto ha llegado al límite de estudiantes")
        else:
            st.write('Enviado')
            document = {
            "studentID": studentID,
            "projectID": option
            }
            studentProject.insert_one(document)
            result = projects_collection.update_one(
                    {"projectID": option},
                    {"$inc": {"quota": -1}}
                )

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')