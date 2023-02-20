import streamlit as st

import base64 

from pathlib import Path

st.set_page_config(page_title='About E-Campus ',
page_icon='RVlogo.png', 
initial_sidebar_state="expanded") 

with open('style1.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 

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




st.markdown("<div style='text-align:center;'><h1>About RVITM-eCampus</h1></div>", unsafe_allow_html=True,)
st.title("")
aboutmessage = "Welcome to RVITM-eCampus, the academic web application of RV Institute of Technology & Management. Our platform is designed to streamline the academic processes for students, teachers, and administrators with the use of cutting-edge technologies like Python, Firebase, Django, Plotly, and ReportLab. Our goal is to provide an easy-to-use, efficient, and accurate solution for result analysis, progress report generation, and student attendance management."
aboutmessage2 = "Please note that our web application is still in its starting phase and is under development. Nevertheless, we are dedicated to continuously improving and adding new features to make the educational process more efficient and accessible."
aboutmessage3 = "RVITM-eCampus is built with the user in mind and is designed to simplify the complexities of the academic process, making it easy to access and understand for everyone involved. With its user-friendly interface and powerful analytical tools, you can quickly analyze student performance, generate progress reports, and monitor attendance with ease."
aboutmessage4 = "We are committed to providing the best possible experience for our users and continuously work towards improving our platform with new features and updates. Our goal is to support the academic community at RV Institute of Technology & Management and help make the educational process more efficient, accessible, and meaningful for all."
aboutmessage5 = "Thank you for choosing RVITM-eCampus. We hope you find it useful and we look forward to serving you."
st.write(aboutmessage)
st.write(aboutmessage2)
st.write(aboutmessage3)
st.write(aboutmessage4)
st.write(aboutmessage5)

st.title("")
with st.expander("Message from ISE HOD"):
    st.markdown("<div style='text-align:center;'><h2>Message from ISE HOD</h2></div>", unsafe_allow_html=True,)
    st.title("")
    

    col1, col2 = st.columns(2)
    
    profile_pic = "isehod_img-modified.png"
    with col1:
        st.image(profile_pic, width=230)

        st.markdown("<div style=''><h4>Dr LATHA CA</h4></div>", unsafe_allow_html=True,)
        st.write("Professor & Head of Department")
    
    with col2:
        
        st.write('I want to Congratulate our third semester ISE students Mr. Darshan Gowda and Mr. Abhijath Dakshesh, for their Beautiful, User friendly, Efficient software, "RVITM e-campus". This has made the lives of Faculty, Students and Parents very easy, saving a lot of time in processing and arriving at various statistics required for varied purposes and accreditations. I also thank and congratulate ISE faculty Ms. Sahana Damale for the Initiate, Guidance and Motivating the duo for the same.')
        st.write("I look forward many such projects which are useful in our day-to-day life , not only from the duo and also from other students... Wishing them all the Best and Prosperity......-Dr LATHA C A")


with st.expander("Message from Teacher Co-ordinator"):
    st.markdown("<div style='text-align:center;'><h2>Message from Teacher Co-ordinator</h2></div>", unsafe_allow_html=True,)
    st.title("")

    col1, col2 = st.columns(2)
    
    profile_pic = "11.-Sahana_Photo-modified.png"
    with col1:
        st.image(profile_pic, width=230)

        st.markdown("<div style=''><h4>SAHANA DAMALE</h4></div>", unsafe_allow_html=True,)
        st.write("Assistant Professor ")
    
    with col2:

        st.write("The student result analysis tool is a software application that is designed to help educators and administrators to analyze and interpret student performance data. This tool provides a comprehensive and easy-to-use interface that allows users to view, analyze and compare student results across multiple subjects, classes, and assessment types.")
        st.write("One of the key benefits of a student result analysis tool is the ability to quickly identify areas where students are excelling and areas where they are struggling. ")
        st.write("Another important feature of a student result analysis tool is the ability to generate reports and share data with stakeholders. ")
        st.write("It is commendable for Mr. Darshan Gowda and Mr. Abhijat Dakshesh to have developed the student result analysis tool. Developing such a tool requires a strong understanding of data analysis, programming, and user experience design, as well as an appreciation for the needs of educators and administrators.  ")