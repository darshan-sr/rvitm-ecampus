
import streamlit as st
from PIL import Image
import base64
from streamlit_extras.switch_page_button import switch_page


from pathlib import Path

st.set_page_config(page_title='RVITM E-Campus',
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


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 


st.markdown("<div style='text-align:center;'><h2> WELCOME TO RVITM E-Campus</h2></div>", unsafe_allow_html=True,)

st.markdown("<div style='text-align:center;'><h1> </h1></div>", unsafe_allow_html=True,)
st.markdown("<div style='text-align:center;'><p> RVITM E-Campus is a platform that simplifies the process of result analysis and tracking of students' CGPA. With the easy-to-use interface, you can now view and analyze your academic progress, check your results, and track your CGPA with just a few clicks. Our advanced analytics tools help you identify areas of improvement and excel in your academic journey. </p></div>", unsafe_allow_html=True,)
st.markdown("<div style='text-align:center;'><h1> </h1></div>", unsafe_allow_html=True,)

st.markdown("<div style='text-align:center;'><h1> </h1></div>", unsafe_allow_html=True,)



imgg = get_img_as_base64("Result-Analysis.png")


button = f'''

<style>

.css-113bm4q.edgvbvh10{{
    padding-left: 40px;
    padding-right: 40px;
    padding-top: 20px;
    padding-bottom: 80px;
    background-color:#ebebeb;
    font-family: 'Courier New', Courier, monospace;
    background-image: url("data:image/png;base64,{imgg}");
    background-size: cover;
    box-shadow: 0 0.05rem 0.75rem 0 rgba(58, 59, 69, 0.15) !important;
    background-repeat: no-repeat;
    border-top: 0.3rem solid #b72271 !important;
}}
</style>
'''
st.markdown(f'{button}</style>', unsafe_allow_html=True)

co1 , co2, co3 = st.columns(3)

with co1:
   if st.button("\u00a0\u00a0\u00a0RESULT ANALYSIS\u00a0\u00a0\u00a0",key=1):
    switch_page("Result Analysis")

with co2:
    if st.button("\u00a0\u00a0\u00a0\u00a0STUDENT LOGIN\u00a0\u00a0\u00a0\u00a0",key=2):
        switch_page("Student Login")

with co3:
    if st.button("DEPARTMENT LOGIN",key=3):
        switch_page("Department Login")