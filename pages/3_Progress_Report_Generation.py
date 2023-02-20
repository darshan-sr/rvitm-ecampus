import streamlit as st
import pandas as pd
import base64 

import streamlit_authenticator as stauth

from datetime import datetime


from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph,Image
import io
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import textwrap
import datetime
import zipfile

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders


st.set_page_config(page_title='E-Campus Progress Report',
page_icon='RVlogo.png', 
initial_sidebar_state="expanded") 

# Hide default header footer and hamburger menu
from pathlib import Path
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
from deta import Deta
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


def generate_pdf(df, row,Branch_Choice,test_choice,submission_d,date_of_generation):  
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0, leftMargin=50, rightMargin=50, bottomMargin=0)
    
    styles = getSampleStyleSheet()

    # Creating a bold and capitalized Times New Roman style
    bold_times_style = styles["Heading1"]
    bold_times_style.fontName = "Times-Bold"
    bold_times_style.fontSize = 12 
    bold_times_style.alignment = 1
    bold_times_style.textTransform = "uppercase"
    bold_times_style.spaceAfter = 1
    bold_times_style.spaceBefore = 1
 


    bold_style = styles["Heading2"]
    bold_style.fontName = "Times-Bold"
    bold_style.fontSize = 10
    bold_style.spaceAfter = 1
    bold_style.spaceBefore = 1
    # bold_style.textTransform = "uppercase"


    elements = [] 

    image_path = "Header_RV.png"
    image = Image(image_path, width=8.756*inch, height=1.8*inch)
    image.vAlign = "TOP"
    elements.append(image)

    heading = Paragraph(Branch_Choice, bold_times_style)
    elements.append(heading)
 
    heading = Paragraph(test_choice, bold_times_style)
    elements.append(heading)


    style_sheet = getSampleStyleSheet()
    style = style_sheet['Normal']
    text = "To, "
    para = Paragraph(text, style)
    elements.append(para)
    
    father = str(df.iloc[row, 4])
    heading = Paragraph("\u00a0 \u00a0 \u00a0Mr/Mrs \u00a0"+father+",", bold_style)
    elements.append(heading)

    student_name = df.iloc[row,1]
    USN = df.iloc[row,2]
    style_sheet = getSampleStyleSheet()
    style = style_sheet['Normal']
    text = "\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0The progress report of your ward "+str(student_name)+","+str(USN)+" studying in III Semester BE ( ISE ) is given below: "
    para = Paragraph(text, style)
    elements.append(para)

    wrapped_sl = textwrap.fill("Sl. No", width=3)
    wrapped_attendance  = textwrap.fill("Attendance Percentage", width=10)
    wrapped_classheld  = textwrap.fill("Classes Held", width=7)
    wrapped_classattended = textwrap.fill("Classes Attended", width=9)
    wrapped_testmarks = textwrap.fill("Test Marks (Max 40)", width=10)
    wrapped_assignment = textwrap.fill("Assignment (Max 10)", width=10)
    data = [[wrapped_sl,"Subject Name",wrapped_classheld,wrapped_classattended,wrapped_attendance,wrapped_testmarks,wrapped_assignment]]

    for i in range(6):
        subject = df.iloc[0, 8 + i * 4]
        try:
           classesheld = int(df.iloc[row, 8 + i * 4])
        except ValueError:
            classesheld = 1
        try:
            classattended = int(df.iloc[row, 9 + i * 4])
        except ValueError:
            classattended = 1
        try:
            attendance = int(classattended / classesheld * 100)
        except ValueError:
            attendance = 1
        marks = df.iloc[row, 10 + i * 4]
        assignment = df.iloc[row, 11 + i * 4]
        wrapped_subject = textwrap.fill(subject, width=30)

        data.append([str(i+1), wrapped_subject, classesheld, classattended, "{}%".format(attendance), marks, assignment])

    table = Table(data, colWidths=None, rowHeights=None, style=None, splitByRow=1, repeatRows=0, repeatCols=0, rowSplitRange=None, spaceBefore=20, spaceAfter=20, cornerRadii=[1.5,1.5,1.5,1.5])
    

    table.setStyle(TableStyle([      
    
    ('BACKGROUND', (0, 0), (-1, 0), '#FFFFFF'),
    ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('fontsize', (-1,-1), (-1,-1), 14),
    ('ALIGNMENT', (1, 1), (1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 15),
    ('BACKGROUND', (0, 1), (-1, -1), '#FFFFFF'),
    ('GRID', (0, 0), (-1, -1), 1, "black")
  ]))

    elements.append(table)

    style_sheet = getSampleStyleSheet()
    style = style_sheet['Normal']
    text = "Remarks : Kindly advise your ward, if the attendance percentage is less than 85% and Test marks are less than 40%. "
    para = Paragraph(text, style)
    elements.append(para)

    style = style_sheet['Normal']
    text = "\u00a0 "
    para = Paragraph(text, style)
    elements.append(para)


    counsellor_mail = str(df.iloc[row,7])
    style_sheet = getSampleStyleSheet()
    style = style_sheet['Normal']
    text = "Please download, sign and send the scanned copy of the report to “"+counsellor_mail+"” on or before "+submission_d+"."
    para = Paragraph(text, style)
    elements.append(para)

    image_path = "RV_Signature.png"
    image = Image(image_path, width=9*inch, height=1.93*inch)
    elements.append(image)

    doc.build(elements)
    
    buffer.seek(0)
    return buffer

def progress_pdf():

    Branch_Choice = st.selectbox("Choose the Branch for which you're generating Progress Report:",["INFORMATION SCIENCE & ENGINEERING","COMPUTER SCIENCE & ENGINEERING","ELECTRONICS & COMMUNICATION ENGINEERING","MECHANICAL ENGINEERING"])

    test_choice = st.selectbox("Choose the test: ",["PROGRESS REPORT-I","PROGRESS REPORT-II","PROGRESS REPORT-III"])

    date_of_generation = st.date_input("Date of Generation:",datetime.date.today())

    submission_d = st.date_input("The Ward Should Sumbit the Signed Progress Report to Counsellor Before:",
    datetime.date.today())
    submission_d=str(submission_d)
    
    semester = st.selectbox("Select the Semester: ",["1st Semester","2nd Semester", "3rd Semester"," 4th Semester", "5th Semester", "6th Semester","7th Semester","8th Semester"])
    
    uploaded_file = st.file_uploader("Upload the Marks Sheet Excel File for the test:", type=["xlsx"])
    
    if uploaded_file is not None:
      tab1, tab2, tab3 = st.tabs(["Generate & Download Report","Preview Progress Report" ,"Confirm & Send Email"])
      with tab1:
        df = pd.read_excel(uploaded_file)
        st.write("Generating Progress Report...")
        
        progress_bar = st.progress(0)
        
        # Create a zip file in memory
        zip_file = io.BytesIO()
        with zipfile.ZipFile(zip_file, mode='w') as archive:
            for i in range(2,df.shape[0]):
                buffer = io.BytesIO()
                generate_pdf(df, i,Branch_Choice,test_choice,submission_d,date_of_generation)
                file_name = f"{df.iloc[i, 2]}.pdf"

                archive.writestr(file_name, buffer.getvalue())
        
            b64 = base64.b64encode(zip_file.getvalue()).decode()
            download_link = f'<a href="data:application/zip;base64,{b64}" download="report.zip">Download all PDFs in zip</a>'
            st.markdown(download_link, unsafe_allow_html=True)
                    
            progress_value = int((i - 1) / (df.shape[0] - 2) * 100)
            progress_bar.progress(progress_value)
        
      with tab2:
      
        df = pd.read_excel(uploaded_file)
        st.write("Generating Preview of Progress Report...")
        
        # Show a progress bar while the PDFs are being generated
        progress_bar = st.progress(0)
        
        # Generate the PDFs for each student and store it in a dictionary with the student name as the key
        pdfs = {}
        for i in range(2, df.shape[0]):
            buffer = generate_pdf(df, i, Branch_Choice, test_choice, submission_d, date_of_generation)
            file_name = f"{df.iloc[i, 2]}.pdf"
         
            b64 = base64.b64encode(buffer.getvalue()).decode()
            pdfs[file_name] = b64
            
            progress_value = int((i - 1) / (df.shape[0] - 2) * 100)
            progress_bar.progress(progress_value)
        
        # Show a selectbox to select the PDF to preview
        selected_pdf = st.selectbox("Select a student", list(pdfs.keys()))
        if selected_pdf is not None:
            b64 = pdfs[selected_pdf]
            st.write("""
            <iframe
                src="data:application/pdf;base64,{b64}"
                style="border: none; width: 100%; height: 970px;"
            ></iframe>
            """.format(b64=b64), unsafe_allow_html=True)

      with tab3:

       df = pd.read_excel(uploaded_file)
       SMTP_SERVER = "smtp.gmail.com"
       SMTP_PORT = 587
       with st.form("login_form"):
         st.write("Enter the mail ID login from which you want to send the mail:")
         
         SMTP_USERNAME = st.text_input('Input mail ID',help="Credentials are safe and not stored anywhere")
         SMTP_PASSWORD = st.text_input('Input password',type='password')
         st.checkbox("I confirm that the Report generated are correct")
         submitted = st.form_submit_button("Confirm & send email")

       if submitted:
        st.write("Sending Email...")
        total_emails = df.shape[0] - 2
        email_sent = 0
        progress_bar = st.progress(0)

        for i in range(2, df.shape[0]):
            buffer = generate_pdf(df, i, Branch_Choice, test_choice, submission_d,date_of_generation)
            file_name = f"{df.iloc[i, 2]}.pdf"
            email = df.iloc[i, 3]
            father = str(df.iloc[i, 4])
            student_name = str(df.iloc[i, 1])

            msg = MIMEMultipart()
            msg['From'] = SMTP_USERNAME
            msg['To'] = COMMASPACE.join([email])
            msg['Subject'] = ""+test_choice+"\u00a0 "+semester
            
            body = "Dear "+father+" ,\n\nHerewith enclosed the "+semester+" "+test_choice+"\u00a0  of your ward "+student_name+".\n\nThanks & Regards,\nRVITM"
            text = MIMEText(body)
            msg.attach(text)
        
            # Attach the generated PDF
            part = MIMEBase('application', "octet-stream")
            part.set_payload((buffer.getvalue()))
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=file_name)
            msg.attach(part)
        
            # Connect to the SMTP server and send the email
            smtpObj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login(SMTP_USERNAME, SMTP_PASSWORD)
            smtpObj.sendmail(SMTP_USERNAME, [email], msg.as_string())
            smtpObj.quit()
        
            st.write("Email sent to\u00a0"+student_name+"\u00a0 parent's mail - ", email)

            email_sent += 1
            progress_bar.progress(email_sent / total_emails)
        st.success("All Progress Reports sent successfully")




def progress_report():
    
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
      st.sidebar.success("Welcome "+username+"")
      authenticator.logout("Logout", "sidebar")

      progress_pdf()
    


        

            


progress_report()

