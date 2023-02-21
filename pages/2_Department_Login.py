import streamlit as st
import pandas as pd
import base64 
import streamlit_authenticator as stauth
from pathlib import Path
from deta import Deta

st.set_page_config(page_title='E-Campus Login',
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


DETA_KEY = "d0mmbh4h7yn_nrn34JKugUPMyyXjW67tZRSYEhokL2Tj"
deta = Deta(DETA_KEY)
db = deta.Base("department-usersdb")

def insert_user(username, name, password):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db.put({"key": username, "name": name, "password": password})

def fetch_all_users():
    """Returns a dict of all users"""
    max_attempts = 1000
    attempts = 0
    while attempts < max_attempts:
        try:
            res = db.fetch()
            return res.items
        except Exception as e:
            attempts += 1
            if attempts == max_attempts:
                raise e


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


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



def department_login():

    users = fetch_all_users()
    usernames = [user["key"] for user in users]
    names = [user["name"] for user in users]
    hashed_passwords = [user["password"] for user in users]

    authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
        "sales_dashboard", "abcdef", cookie_expiry_days=0)
    name, authentication_status, username = authenticator.login("LOGIN", "main")

    if authentication_status == False:
        st.error("Username/password is incorrect")


    if authentication_status:
        try:
            if username == 'isedept' or username == 'csedept' or username == 'ecedept' or username == 'medept':
                 with st.spinner("Loading..."):
                  st.sidebar.success("Welcome "+username+"")
                  authenticator.logout("Logout", "sidebar")
            
                  if username == "isedept":
                    
            
                    batch_choice = st.selectbox("Select the year of the Batch", ["2021 Batch", "2020 Batch","2019 Batch", "2022 Batch"])
                    if batch_choice == "2021 Batch":
                        url = "https://docs.google.com/spreadsheets/d/1LFIKxpYN1tNYqD03U6RYb58Slq32lk2P/export?format=xlsx"
                        xls = pd.ExcelFile(url,engine='openpyxl')
                        sheet_name = st.selectbox("Select a sheet", xls.sheet_names)
                        df = pd.read_excel(xls, sheet_name=sheet_name)
                        st.dataframe(df)
                        st.markdown("[Update on this Google sheet](https://docs.google.com/spreadsheets/d/1LFIKxpYN1tNYqD03U6RYb58Slq32lk2P)")
                        uploaded_file = st.file_uploader("Choose a file", type="xlsx")
                        if uploaded_file:
                            try:
                                url = ("https://docs.google.com/spreadsheets/d/1bL2IYl-hJOwD9WUETCB98q4BgL9rAwyL")
                                with open("https://docs.google.com/spreadsheets/d/1LFIKxpYN1tNYqD03U6RYb58Slq32lk2P", "wb") as f:
                                    f.write(uploaded_file.read())
                                st.success("File uploaded Successfully!")
                            except:
                                st.error("Upload Failed")
                    if batch_choice == "2020 Batch":
                        url = "https://docs.google.com/spreadsheets/d/1bL2IYl-hJOwD9WUETCB98q4BgL9rAwyL/export?format=xlsx"
                        xls = pd.ExcelFile(url,engine='openpyxl')
                        sheet_name = st.selectbox("Select a sheet", xls.sheet_names)
                        df = pd.read_excel(xls, sheet_name=sheet_name)
                        st.dataframe(df)
                        st.markdown("[Update on this Google sheet](https://docs.google.com/spreadsheets/d/1bL2IYl-hJOwD9WUETCB98q4BgL9rAwyL)")
                        uploaded_file = st.file_uploader("Choose a file", type="xlsx")
                        if uploaded_file:
                         try:
                            url = ("https://docs.google.com/spreadsheets/d/1bL2IYl-hJOwD9WUETCB98q4BgL9rAwyL")
                            with open("https://docs.google.com/spreadsheets/d/1bL2IYl-hJOwD9WUETCB98q4BgL9rAwyL", "wb") as f:
                                f.write(uploaded_file.read())
                            st.success("File uploaded Successfully!")
                         except:
                            st.error("Upload Failed")
            
                  if username == "csedept":
                    
            
                    batch_choice = st.selectbox("Select the year of the Batch", ["2021 Batch", "2020 Batch","2019 Batch", "2022 Batch"])
                    if batch_choice == "2021 Batch":
                        url = "https://docs.google.com/spreadsheets/d/1LFIKxpYN1tNYqD03U6RYb58Slq32lk2P/export?format=xlsx"
                        xls = pd.ExcelFile(url,engine='openpyxl')
                        df = pd.read_excel(url,engine='openpyxl')
                        st.dataframe(df)
                    uploaded_file = st.file_uploader("Choose a file", type="xlsx")
                    if uploaded_file:
                        try:
                            url = ("https://docs.google.com/spreadsheets/d/1bL2IYl-hJOwD9WUETCB98q4BgL9rAwyL")
                            with open("2021.ISE-6.xlsx", "wb") as f:
                                f.write(uploaded_file.read())
                            st.success("File uploaded Successfully!")
                        except:
                            st.error("Upload Failed")
                    
                  if username == "ecedept":
                    
            
                    batch_choice = st.selectbox("Select the year of the Batch", ["2021 Batch", "2020 Batch","2019 Batch", "2022 Batch"])
                    if batch_choice == "2021 Batch":
                        url = "https://docs.google.com/spreadsheets/d/1LFIKxpYN1tNYqD03U6RYb58Slq32lk2P/export?format=xlsx"
                        xls = pd.ExcelFile(url,engine='openpyxl')
                        df = pd.read_excel(url,engine='openpyxl')
                        st.dataframe(df)
                    uploaded_file = st.file_uploader("Choose a file", type="xlsx")
                    if uploaded_file:
                        try:
                            url = ("https://docs.google.com/spreadsheets/d/1bL2IYl-hJOwD9WUETCB98q4BgL9rAwyL")
                            with open("2021.ISE-6.xlsx", "wb") as f:
                                f.write(uploaded_file.read())
                            st.success("File uploaded Successfully!")
                        except:
                            st.error("Upload Failed")
            
                  if username == "medept":
                    
            
                    batch_choice = st.selectbox("Select the year of the Batch", ["2021 Batch", "2020 Batch","2019 Batch", "2022 Batch"])
                    if batch_choice == "2021 Batch":
                        url = "https://docs.google.com/spreadsheets/d/1LFIKxpYN1tNYqD03U6RYb58Slq32lk2P/export?format=xlsx"
                        xls = pd.ExcelFile(url,engine='openpyxl')
                        df = pd.read_excel(url,engine='openpyxl')
                        st.dataframe(df)
                    uploaded_file = st.file_uploader("Choose a file", type="xlsx")
                    if uploaded_file:
                        try:
                            url = ("https://docs.google.com/spreadsheets/d/1bL2IYl-hJOwD9WUETCB98q4BgL9rAwyL")
                            with open("2021.ISE-6.xlsx", "wb") as f:
                                f.write(uploaded_file.read())
                            st.success("File uploaded Successfully!")
                        except:
                            st.error("Upload Failed")
            else:
                st.info('Please Logout of Student account to continue!')
        except Exception as e:
            st.info('Please Logout of Student account to continue!', e)           
                
            


        

department_login()

            



