import streamlit as st
import base64 
from deta import Deta
from pathlib import Path

st.set_page_config(page_title='RVITM - Submit Feedback',
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



st.header(":mailbox: Submit a Feedback!")
st.title("")
st.write("We are collecting feedback for our RVITM E-Campus app which is used by college lectures and students. Your input on what can be improved and if there are any bugs will greatly assist in the continued development of the app. Your suggestions for new features would also be appreciated. Please fill out the contact form to share your thoughts and feedback. Your contributions will help make the app an even more useful tool for the college community")
st.title("")
DETA_KEY = "d0mmbh4h7yn_nrn34JKugUPMyyXjW67tZRSYEhokL2Tj"
deta = Deta(DETA_KEY)
db = deta.Base("feedback-db")


def insert_feedback(input_name,input_mail,input_message):
    """Insert a new user into the database"""
    db.put({"name": input_name, "mail": input_mail, "feedback": input_message})



with st.form("feedback_form"):
   
    col1, col2 = st.columns(2)
    with col1: 
     firstname = st.text_input("Your Name:",placeholder="First Name")
    with col2:
     lastname = st.text_input("",placeholder="Last Name")
    input_name = ''+firstname+''+lastname+''
    input_mail = st.text_input("Your college Mail ID: ",placeholder="example.rvitm@rvei.edu.in")
    input_message = st.text_area("Your Feedback: ",placeholder="Your Feedback Here")

    if st.form_submit_button("Submit Feedback"):

            insert_feedback(input_name,input_mail,input_message)
            st.success("Thanks for the Feedback!")
