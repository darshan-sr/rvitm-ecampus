import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from streamlit_option_menu import option_menu
import base64 

import streamlit_authenticator as stauth

from datetime import datetime
from deta import Deta


import textwrap
import datetime
import zipfile

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders
from pathlib import Path


st.set_page_config(page_title='E-Campus Student Login',
page_icon='RVlogo.png', 
initial_sidebar_state="expanded") 


def add_logo(logo_url: str, height: int = 250):


    logo = f"url(data:image/png;base64,{base64.b64encode(Path(logo_url).read_bytes()).decode()})"
    

    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: {logo};
                background-repeat: no-repeat;
                padding-top: {height - 40}px;
                background-position: 20px 20px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

add_logo("HD_transparent_picture.png")


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


with open('style1.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("sidebarlogo.jpg")

page_bg_img = f"""

<style>

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: topleft;
background-repeat: no-repeat;
background-attachment: fixed;
}}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)




def StudentMarks(xls,input_str):

        data = pd.read_excel(xls)
        student_data = data.loc[data['USN'] == input_str]
        BACK = student_data[data.columns[44]].values[0]
        NAME = student_data[data.columns[2]].values[0] 
        USN = student_data[data.columns[1]].values[0]
        with open('style1.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)   

        with pd.ExcelFile(xls) as xlsx:
            sheets = xlsx.sheet_names
            BACK = 0
            for sheet_name in sheets:
                data = pd.read_excel(xlsx, sheet_name=sheet_name)
                student_data = data.loc[data['USN'] == input_str]
                BACK += int(student_data[data.columns[44]].values[0])     

      
      
        with pd.ExcelFile(xls) as xlsx:
            sheets = xlsx.sheet_names
            CGPA = []
            for sheet_name in sheets:
                data = pd.read_excel(xlsx, sheet_name=sheet_name)
                student_data = data.loc[data['USN'] == input_str]
                CGPA.append(student_data[data.columns[40]].values[0])
      
            CGPAA = sum(CGPA)/ len(CGPA) 
            TCGPA = round(CGPAA/1,1)

        st.markdown('### STUDENT DETAILS:')
        col1, col2= st.columns(2)
        col1.metric("NAME:",NAME)
        col2.metric("USN:",USN)
        col1, col2= st.columns(2)
        col1.metric("FAILED SUBJETS:",BACK)
        col2.metric("Average Percentage:",TCGPA)


        
        sheet_names = xls.sheet_names
        student_data = []
        for sheet_name in sheet_names:
            data = pd.read_excel(xls, sheet_name=sheet_name)
            student_record = data.loc[data['USN'] == input_str]
            student_data.append({
                'sheet_name': sheet_name,
                'percentage': student_record[student_record.columns[40]].values[0]
            })
    
        student_data_df = pd.DataFrame(student_data)
        student_data_df['text'] = student_data_df['percentage'].apply(lambda x: '{:.2f}%'.format(x))
        fig = px.bar(student_data_df, x='sheet_name', y='percentage',text='text',title=f"Comparison of {NAME}'s Percentage")
        fig.update_layout(xaxis_title='',yaxis_title='Percentage',width=700, height=600,yaxis=dict(range=[0, 100]))
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        st.plotly_chart(fig)





        sheet_name = st.selectbox("Select the semester", xls.sheet_names)
        data = pd.read_excel(xls, sheet_name=sheet_name)
    
        student_data = data.loc[data['USN'] == input_str]
        
        st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;'><h3>Marks Sheet for the "+sheet_name+" </h3></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
        st.write("The below table presents a comprehensive view of the student's marks sheet for the specific semester, including the percentage, total marks, and grade obtained by the student ")
        

        
        subjects = []
        for i in range(3, 36, 4):
          if not pd.isnull(data.iloc[0, i]):
            student_data[data.columns[i+2]] = pd.to_numeric(student_data[data.columns[i+2]], errors='coerce')

            subject = {}
            subject["Subject Name"] = data.iloc[0, i]
            subject["Internal Marks"] = student_data[data.columns[i]].values[0]
            subject["External Marks"] = student_data[data.columns[i+1]].values[0]
            subject["Total"] = student_data[data.columns[i+2]].values[0]
            subject["Results"] = student_data[data.columns[i+3]].values[0]

                #Assign the grades and grade points based on the total marks
            subject["Grade"] = "F"
            subject["Grade Points"] = 0
            if subject["Total"] >= 90:
                subject["Grade"] = "O"
                subject["Grade Points"] = 10
            elif subject["Total"] >= 80:
                subject["Grade"] = "A+"
                subject["Grade Points"] = 9
            elif subject["Total"] >= 70:
                subject["Grade"] = "A"
                subject["Grade Points"] = 8
            elif subject["Total"] >= 60:
                subject["Grade"] = "B+"
                subject["Grade Points"] = 7
            elif subject["Total"] >= 55:
                subject["Grade"] = "B"
                subject["Grade Points"] = 6
            elif subject["Total"] >= 50:
                subject["Grade"] = "C"
                subject["Grade Points"] = 5
            elif subject["Total"] >= 40:
                subject["Grade"] = "P"
                subject["Grade Points"] = 4
            subjects.append(subject)

        # CSS to inject contained in a string
        table_html = data.to_html(index=False)
        st.markdown("<style>table {width:50%;} td, th {border: 2px solid #a4a8ab;} td:last-child, th:last-child {border-right: 2px solid #a4a8ab;} tr:last-child td {border-bottom: 2px solid #a4a8ab;} table.dataframe {display: none;}</style>", unsafe_allow_html=True)
        st.write(table_html, unsafe_allow_html=True)
        hide_table_row_index = """
                    <style>
                    thead tr th:first-child {display:none}
                    tbody th {display:none}
                    </style>
                    """
        
        # Inject CSS with Markdown
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        
        st._legacy_table(pd.DataFrame(subjects))


  

        Total= int(student_data[data.columns[39]].values[0])
        Percentage= round(student_data[data.columns[40]].values[0],2)
        Grade= student_data[data.columns[41]].values[0]
        Results=student_data[data.columns[42]].values[0]
        Passed_Subjects=int(student_data[data.columns[43]].values[0])
        Failed_Subjects=int(student_data[data.columns[44]].values[0])
        Absent_Subjects=int(student_data[data.columns[45]].values[0])
        st.markdown('')
        col1, col2,col3= st.columns(3)
        col1.metric("TOTAL:",Total)
        col2.metric("PERCENTAGE:","{:.2f}%".format(Percentage))
        col3.metric("GRADE:",Grade)
        
        col4,col5,col6 = st.columns(3)
        col4.metric("RESULTS:",Results)
        col5.metric("PASSED SUBJECTS:",Passed_Subjects)
        col6.metric("FAILED SUBJECTS",Failed_Subjects+Absent_Subjects)
        

        
        if student_data.empty:
            st.error("No data found for selected student.")
        else:
            # Extract the marks of the student in the 5th and 9th columns
            subject_count = 10
            subject_marks = []
            subject_names = []
            
            for i in range(subject_count):
                subject_marks.append(student_data[data.columns[5+4*i]].values[0])
                subject_names.append(data.iloc[0,3+4*i])
            


            st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
            st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
            st.markdown("<div style='text-align:center;'><h3>BAR CHART OF MARKS IN EVERY SUBJECT </h3></div>", unsafe_allow_html=True)
            st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
            st.write("The below bar chart provides a visual representation of the student's performance in each subject of the semester, highlighting the marks obtained by the student in each subject and allowing for a quick and easy comparison of the student's performance across all subjects.")
            st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
            
            # Create a bar chart of the extracted marks
            chart_choice = st.selectbox("Select the type of Chart you need:", ["Bar Chart","Grouped Bar Chart","Area Graph","Funnel"] )

            if chart_choice == "Bar Chart": 
              with st.spinner("Loading data..."):
                fig = px.bar(x=subject_names, y=subject_marks)
                fig.update_layout(xaxis_title='', yaxis_title='Total Marks', width=700, height=600)
                st.plotly_chart(fig)
            if chart_choice == "Area Graph": 
              with st.spinner("Loading data..."):
                fig = px.area(x=subject_names, y=subject_marks)
                fig.update_layout(xaxis_title='', yaxis_title='Total Marks', width=700, height=600)
                st.plotly_chart(fig)

            if chart_choice == "Funnel": 
              with st.spinner("Loading data..."):
                fig = px.funnel(x=subject_names, y=subject_marks)
                fig.update_layout(xaxis_title='', yaxis_title='Total Marks', width=700, height=600)
                st.plotly_chart(fig)

            if chart_choice == "Grouped Bar Chart":
              with st.spinner("Loading data..."):
                subject_count = 9
                subject_internal_marks = []
                subject_external_marks = []
                subject_names = []
                
                for i in range(subject_count):
                    subject_internal_marks.append(student_data[data.columns[3+4*i]].values[0])
                    subject_external_marks.append(student_data[data.columns[4+4*i]].values[0])
                    subject_names.append(data.iloc[0,3+4*i])
                
                fig = px.bar(x=subject_names, y=[subject_internal_marks, subject_external_marks], barmode='group')
                fig.update_layout(xaxis_title='', yaxis_title='Total Marks', width=800, height=600)
                fig.data[0].update(name='Internal Marks', showlegend=True, marker=dict(color='rgb(99,110,245)'))
                fig.data[1].update(name='External Marks', showlegend=True, marker=dict(color='rgb(241,86,64)'))
    
                st.plotly_chart(fig)


    
def attendance():
 
 
 selected = option_menu(
        menu_title=None,
        options=["Login","Signup"],
        icons=["person-workspace","person"],
        orientation="horizontal",
    )

 if selected == "Login":

    DETAA = "d0mmbh4h7yn_aVTdWVFf5UQTxWHZZmeX144mkXaiD9Ht"
    det = Deta(DETAA)
    dt = det.Base("students_db")
    def fetch_student_users():
        max_attempts = 800
        attempts = 0
        while attempts < max_attempts:
            try:
                res = dt.fetch()
                return res.items
            except Exception as e:
                attempts += 1
                if attempts == max_attempts:
                    raise e

    userss = fetch_student_users()
    usernamess = [user["key"] for user in userss]
    namess = [user["name"] for user in userss]
    passwordss = [user["password"] for user in userss]

    student_authenticator = stauth.Authenticate(namess, usernamess, passwordss,
        "student_dashboard", "student", cookie_expiry_days=0)
    namess, authentication_statuss, usernames = student_authenticator.login("LOGIN", "main")

    if authentication_statuss == False:
        st.error("Username/password is incorrect")


    if authentication_statuss:

      
        st.sidebar.success("Welcome "+namess+"")
        student_authenticator.logout("Logout", "sidebar")
        tab1, tab2 = st.tabs(["Marks Analysis", "Attendance"])

        with tab1:
             input_str = usernames

             if "21IS" in input_str:
                 url = "https://docs.google.com/spreadsheets/d/1LFIKxpYN1tNYqD03U6RYb58Slq32lk2P/export?format=xlsx"
                 xls = pd.ExcelFile(url, engine='openpyxl')
                 with st.spinner("Loading data..."):
                     StudentMarks(xls, input_str)
         
             if "20IS" in input_str:
               
                 url = "https://docs.google.com/spreadsheets/d/1bL2IYl-hJOwD9WUETCB98q4BgL9rAwyL/export?format=xlsx"
                 xls = pd.ExcelFile(url,engine='openpyxl')
                 with st.spinner("Loading data..."):
                     StudentMarks(xls,input_str)

        with tab2:
            st.info("Coming Soon...")



 if selected == "Signup":
    DETAA = "d0mmbh4h7yn_aVTdWVFf5UQTxWHZZmeX144mkXaiD9Ht"
    det = Deta(DETAA)
    dt = det.Base("students_db")
    
    
    def insert_user(username, name, email, password):
        """Returns the user on a successful user creation, otherwise raises and error"""
        return dt.put({"key": username, "name": name, "emai": email, "password": password})

    

    with st.form("signup_form"):
        col1, col2 = st.columns(2)
        with col1: 
         firstname = st.text_input("First Name")
        with col2:
         lastname = st.text_input("Last Name")
        name = ''+firstname+'\u00a0'+lastname+''
        username = st.text_input("Enter your USN",placeholder="1RF00XX000 (Enter in caps)")
        email = st.text_input("Enter College Email ID:",placeholder="example.rvitm@rvei.edu.in")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
    
        if st.form_submit_button("Sign Up"):
            if password != confirm_password:
                st.error("Passwords do not match.")
            else:
                usernames = [username]
                names = [name]
                passwords = [confirm_password]
                email = [email]
                hashed_passwords = stauth.Hasher(passwords).generate()
                for (username, name, email, hash_password) in zip(usernames, names, email, hashed_passwords):
                    insert_user(username, name, email, hash_password)
                st.success("You have successfully signed up, Please login to continue")
    


attendance()
