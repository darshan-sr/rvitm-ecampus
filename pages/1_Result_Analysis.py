import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from streamlit_option_menu import option_menu
import base64 
from deta import Deta
import streamlit_authenticator as stauth
from streamlit_extras.switch_page_button import switch_page
import random

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders

st.set_page_config(page_title='RVITM PhaliTantramsha',
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


def student_analysis():

 

    batch_choice = st.selectbox("Select the year of the Batch", ["2019 Batch", "2020 Batch","2021 Batch", "2022 Batch"])
    
    if batch_choice == "2021 Batch":
        branch_choice = st.selectbox("Select the Branch", ["CSE", "ISE","EC", "ME"])
        
        if branch_choice == "CSE":
          with st.spinner("Loading..."):
            try:
                url = ""
                xls = pd.ExcelFile(url, engine='openpyxl')
                plot_analysis(xls)
            except:
                st.warning("Data not found / yet to be updated")

        if branch_choice == "ISE":
          with st.spinner("Loading..."):
            try:
                url = "https://docs.google.com/spreadsheets/d/1LFIKxpYN1tNYqD03U6RYb58Slq32lk2P/export?format=xlsx"
                xls = pd.ExcelFile(url, engine='openpyxl')
                plot_analysis(xls)
            except:
                st.warning("Data not found / yet to be updated")             


        if branch_choice == "ECE":
          with st.spinner("Loading..."):
            try:
                url= ""
                xls = pd.ExcelFile(url, engine='openpyxl')
                plot_analysis(xls)
            except:
                st.warning("Data not found / yet to be updated")

        if branch_choice == "ME":
          with st.spinner("Loading..."):
            try:
                url = ""
                xls = pd.ExcelFile(url, engine='openpyxl')
                plot_analysis(xls)
            except FileNotFoundError:
                st.warning("Data not found / yet to be updated")
                

    if batch_choice =="2020 Batch":
        branch = st.selectbox("Select the Branch", ["CSE", "ISE","EC", "ME"])

        if branch == "ISE":
          with st.spinner("Loading..."):
            try:
                url="https://docs.google.com/spreadsheets/d/1bL2IYl-hJOwD9WUETCB98q4BgL9rAwyL/export?format=xlsx"
                xls = pd.ExcelFile(url, engine='openpyxl')
                plot_analysis(xls)
            except FileNotFoundError:
                st.warning("Data not found / yet to be updated")

    if batch_choice =="2019 Batch":
        branch = st.selectbox("Select the Branch", ["CSE", "ISE","EC", "ME"])

        if branch == "ISE":
            try:
                url=''
                xls = pd.ExcelFile(url, engine='openpyxl')
                plot_analysis(xls)
            except FileNotFoundError:
                st.warning("Data not found / yet to be updated")


def plot_analysis(xls):

    data = pd.read_excel(xls,sheet_name=None)

    st.markdown("<div style='text-align:center;'><h4>CLASS AVERAGE PERFORMANCE</h4></div>",unsafe_allow_html=True)
    
    averages = []
    
    for sheet_name, data in data.items():
        average = data.iloc[:, 40].mean()
        averages.append((sheet_name, average))
    
    
    averages_df = pd.DataFrame(averages, columns=["Sheet Name", "Average Percentage"])
    fig = px.bar(averages_df, x="Sheet Name", y="Average Percentage")
    fig.update_layout(xaxis_title='',yaxis_title='Average Percentage',width=700, height=600,yaxis=dict(range=[0, 100]))
    st.plotly_chart(fig)


    sheet_name = st.selectbox("Select the semester", xls.sheet_names)
    data = pd.read_excel(xls, sheet_name=sheet_name)
    
    
    st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;'><h3>   SELECT THE TYPE OF ANALYSIS YOU NEED     </h3></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;'><h4>          </h4></div>", unsafe_allow_html=True)
    
    tab1,tab2,tab3 = st.tabs(['\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0Semester wise Analysis\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0','\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0Subject wise Analysis\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0','\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0Student wise Analysis\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0'])


    with tab1:
      with st.spinner("Loading..."):
        st.markdown("<div style='text-align:center;'><h3>          </h3></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;'><h3>GRADE ANALYSIS 📈</h3></div>", unsafe_allow_html=True)
        
        # Plot a Pie Chart For Grades
        st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
        st.markdown("<h5>1. Pie Chart of Grade</h5></div>", unsafe_allow_html=True)
        st.write("This Pie Chart represents the distribution of students according to their grades. The different segments of the chart denote the percentage of students who have achieved a specific grade. The grades are categorized as FCD (First Class Distinction), FC (First Class), SC (Second Class), and FAIL (Failure).")
        
    
        # Create a list of valid grades
        valid_grades = ['FCD', 'FC', 'SC', 'FAIL', 'NE']
        column2 = data.columns[41]
        # Filter the data to only include rows where column2 is in the valid_grades list
        data_to_plot = data[data[column2].isin(valid_grades)]
        # Create the pie chart using the filtered data
        fig = go.Figure(data=[go.Pie( labels=data_to_plot[column2])])
        fig.update_layout( width=700, height=700)
        st.plotly_chart(fig)


        # Plot Histogram for Grades
        st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
        st.markdown("<h5>2. Histogram of Grade</h5></div>", unsafe_allow_html=True)
        st.write("This Histogram illustrates the distribution of students across different grade ranges, with FCD representing First class Distinction, FC representing First class, SC representing Second Class, and FAIL representing failure.")
        

        column2 = data.columns[41]
        fig = px.histogram(data, x=column2)
        fig.update_layout(width=600, height=600,yaxis_title='No. of Students')
        st.plotly_chart(fig)


        # Baclog Subjects Analysis

        st.markdown("<div style='text-align:center;'><h3>BACKLOG SUBJECTS ANALYSIS 📈</h3></div>", unsafe_allow_html=True)


        #No of students having backlog in each subject
        st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
        st.markdown("<h5>1. No. of Students having Backlogs in Each Subject</h5></div>", unsafe_allow_html=True)
        st.write("The Below Bar Chart represents the number of students who have failed in a particular subject")
        column1 = data.columns[6]
        column2 = data.columns[10]
        column3 = data.columns[14]
        column4 = data.columns[18]
        column5 = data.columns[22]
        column6 = data.columns[26]
        column7 = data.columns[30]
        column8 = data.columns[33]
        column9 = data.columns[37]
        subject_columns = [column1,column2,column3,column4,column5,column6,column7,column8,column9]
        subject_failures = data[subject_columns].eq('F').sum()
        subject_failures.index = [data.iloc[0,3],data.iloc[0, 7] ,data.at[0, data.columns[11]],data.at[0, data.columns[15]], data.at[0, data.columns[19]], data.at[0, data.columns[23]],data.at[0, data.columns[27]], data.at[0, data.columns[30]], data.at[0, data.columns[34]]]
        subject_failures = subject_failures.rename("Number of Failures")
        subject_failures.sort_values(ascending=True, inplace=True)
        fig = px.bar(subject_failures.reset_index(), x='index', y='Number of Failures')
        fig.update_layout(width=700, height=700,yaxis_title='Number of Failures',xaxis_title='')
        st.plotly_chart(fig)
        


        # Bar Chart between NAME and FAIL

        st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
        st.markdown("<h5>2. Bar Chart between Students and Number of Backlogs </h5></div>", unsafe_allow_html=True)
        st.write("The bar chart illustrates the number of subjects in which students have failed (backlogs) and their corresponding names. It provides a clear visual representation of the students who have failed and the number of subjects they have failed in, allowing for easy identification of students who may require additional support or resources.")
        x_data = data.iloc[:, 2]
        y_data = data.iloc[:, 44]
        # Create a boolean mask to filter y_data where it is not equal to 0
        mask = y_data != 0
        filtered_x_data = x_data[mask]
        filtered_y_data = y_data[mask]
        fig = go.Figure(data=[go.Bar(x=filtered_x_data, y=filtered_y_data)])
        fig.update_layout(width=700, height=600,yaxis_title='No. of Backlog Subjects')
        st.plotly_chart(fig)


        # Percentage Analysis

        st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;'><h3>PERCENTAGE ANALYSIS 📈</h3></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
        st.markdown("<h5>1. Percentage Histogram</h5></div>", unsafe_allow_html=True)
        st.write("The histogram presents the distribution of percentage marks obtained by students in a semester. It clearly shows the range of marks scored by the students and the frequency at which each mark range occurs, providing a comprehensive understanding of the students' performance in the semester.")
        fig = px.histogram(data, x=data.iloc[:, 40])
        fig.update_layout(width=600, height=600,yaxis_title='No. of Students',xaxis_title="Percentage")
        st.plotly_chart(fig)


        #Topper Analysis

        st.markdown("<div style='text-align:center;'><h3>SEMESTER TOPPER ANALYSIS 📈</h3></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)

        st.markdown("<h5>Top 10 Performers in the Semester </h5></div>", unsafe_allow_html=True)
        st.write("The below bar chart showcases the top 10 highest-scoring students in the Semester, displaying their names and marks for easy comparison and analysis.")
        sorted_data = data.sort_values(by='PERCENTAGE',ascending=True)
        sorted_data = sorted_data[[data.columns[2],'PERCENTAGE']].tail(12)
        fig = px.bar(sorted_data, x='PERCENTAGE', y=data.columns[2],color='PERCENTAGE',color_continuous_scale=['#90EE90', 'green','#006400'])
        fig.update_layout(width=600, height=500,xaxis_title='Percentage')
        st.plotly_chart(fig)
        st.empty().text_align = 'center'

        st.write("The below table displays the top 10 students who have performed exceptionally well in the Semester.")
                                                    

        sorted = data.sort_values(by='PERCENTAGE',ascending=False)
        sorted = sorted[['USN',data.columns[2],'TOTAL','GRADE','PERCENTAGE']].head(10)
        st._legacy_table(sorted[['USN',data.columns[2],'TOTAL','GRADE','PERCENTAGE']])



    with tab2:
    # if selected == "Subject Analysis":
      with st.spinner("Loading..."):

        subject_choices = [data.iloc[0, 3], data.iloc[0, 7], data.iloc[0, 11], data.iloc[0, 15], data.iloc[0, 19], data.iloc[0, 23], data.iloc[0, 27], data.iloc[0, 31], data.iloc[0, 35]]
        Subject_Choice = st.selectbox("Select the Subject:", subject_choices)

        st.header("")
        st.header("")

        st.markdown("<div style='text-align:center;'><h4>ANALYSIS FOR THE SUBJECT: "+Subject_Choice+"</h4></div>",unsafe_allow_html=True)

        
        for i in range(3, 36, 4):
            if data.iloc[0, i] == Subject_Choice:

                st.markdown("<div style='text-align:center;'><h1></h1></div>",unsafe_allow_html=True)
     
                # Histogram of Marks
     
                st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
                st.markdown("<h5>1. Histogram of Marks</h5></div>", unsafe_allow_html=True)
                st.write("The below histogram illustrates the distribution of marks of the students in the subject, enabling us to understand where the majority of the class stands in terms of their performance and identify any patterns in the data.")
                st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
                data[data.columns[2+i]] = pd.to_numeric(data[data.columns[2+i]], errors='coerce')
                Subject1_Marks = data.columns[2+i]
                data = data.sort_values(by=Subject1_Marks,ascending=True)
                fig = px.histogram(data, x=Subject1_Marks)
                fig.update_layout(width=600, height=600,xaxis_title= "Marks",yaxis_title="No. of Students")
                st.plotly_chart(fig)
     
     
                Student_Name = data.columns[2]
                data = data.sort_values(by=Subject1_Marks,ascending=True)
                st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
                st.markdown("<h5>2. Bar Chart of total marks</h5></div>", unsafe_allow_html=True)
                st.write("The bar chart below shows the marks of each student in the subject, sorted in ascending order. It makes it easy to compare and analyze the performance of each student. Click on the maximize button for a better view.")
                fig = px.bar(data, x=Student_Name, y=Subject1_Marks)
                fig.update_layout(width=690, height=600,yaxis_title="Total Marks")
                st.plotly_chart(fig)
     
     
                # Create a list of valid grades
                valid_grades = ['P', 'F', 'X','A']
                Subject1_Results = data.columns[3+i]
                st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
                st.markdown("<h5>3. Pie Chart of Overall Results</h5></div>", unsafe_allow_html=True)
                st.write("The below pie chart shows the overall results of the class in the subject, with each sector representing the pass rate (P), fail rate (F), and ineligible rate (X).")
                # Filter the data to only include rows where Subject1_Results is in the valid_grades list
                data_to_plot = data[data[Subject1_Results].isin(valid_grades)]
                # Create the pie chart using the filtered data
                fig = go.Figure(data=[go.Pie( labels=data_to_plot[Subject1_Results])])
                fig.update_layout( width=700, height=700)
                st.plotly_chart(fig)
     
     
                # Analysis of Student Having Backlog in the Subject
                st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
                st.markdown("<h5>4. Students having Backlog in the Subject</h5></div>", unsafe_allow_html=True)
                st.write("This below bar graph shows the students who have failed in the subject and their total marks")
                failed_data = data.loc[data[data.columns[3+i]].isin(['F', 'X', 'A','NE'])]
                student_name = failed_data[data.columns[2]]
                student_marks = failed_data[data.columns[2+i]]
                fig = go.Figure([go.Bar(x=student_name, y=student_marks)])
                fig.update_layout(xaxis_title="Student Name", yaxis_title="Total Marks",width=700, height=700)
                st.plotly_chart(fig)
     
     
                # Grade Analysis
                # Create a new column 'GRADE' based on the conditions provided
                st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
                st.markdown("<h5>5. Grade Distribution in the Subject</h5></div>", unsafe_allow_html=True)
                st.write("The below bar graph illustrates the distribution of grades among the students in the subject. Grades are determined by the following criteria: 'O' for scores 90 and above, 'A+' for scores between 80-89, 'A' for scores between 70-79, 'B+' for scores between 60-69, 'B' for scores between 55-59, 'C' for scores between 50-54, 'P' for scores between 40-49, and 'F' for scores between 0-39. Please note that 'O' stands for outstanding.")
                data[data.columns[2+i]] = pd.to_numeric(data[data.columns[2+i]], errors='coerce')
                data['GRADE'] = 'F'
                data.loc[(data[data.columns[2+i]] >= 90), 'GRADE'] = 'O'
                data.loc[((data[data.columns[2+i]] >= 80) & (data[data.columns[2+i]] < 90)), 'GRADE'] = 'A+'
                data.loc[((data[data.columns[2+i]] >= 70) & (data[data.columns[2+i]] < 80)), 'GRADE'] = 'A'
                data.loc[((data[data.columns[2+i]] >= 60) & (data[data.columns[2+i]] < 70)), 'GRADE'] = 'B+'
                data.loc[((data[data.columns[2+i]] >= 55) & (data[data.columns[2+i]] < 60)), 'GRADE'] = 'B'
                data.loc[((data[data.columns[2+i]] >= 50) & (data[data.columns[2+i]] < 55)), 'GRADE'] = 'C'
                data.loc[((data[data.columns[2+i]] >= 40) & (data[data.columns[2+i]] < 50)), 'GRADE'] = 'P'
     
                # Create the bar chart
                grade_counts = data['GRADE'].value_counts()
                fig = go.Figure(data=[go.Bar(x=grade_counts.index, y=grade_counts.values)])
                fig.update_layout( xaxis_title='GRADE', yaxis_title='Number of Students')
                st.plotly_chart(fig)
     
                st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
                st.markdown("<h5>6. Grade Distribution - Pie Chart</h5></div>", unsafe_allow_html=True)
                st.write("The Pie chart below illustrates the grade distribution of the subject in a clear and concise way, providing a visual representation of the number of students who achieved a specific grade, making it easy to understand and compare with the bar chart representation.")
     
                grades_count = data['GRADE'].value_counts() 
     
                fig = go.Figure(data=[go.Pie(labels=grades_count.index, values=grades_count.values)])
                fig.update_layout(width=700, height=700)
                st.plotly_chart(fig)
     
                st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
                st.markdown("<h5>7. Internal vs External Test Performance Comparison</h5></div>", unsafe_allow_html=True)
                st.write("The Below pie chart illustrates the comparison of the performance of the whole class in the subject, in terms of their internal test marks versus their external test marks, providing a clear visual representation of the performance of the class in both aspects.")
                data[data.columns[0+i]] = pd.to_numeric(data[data.columns[0+i]], errors='coerce')
                data[data.columns[1+i]] = pd.to_numeric(data[data.columns[1+i]], errors='coerce')
     
                column3_data = data[data.columns[0+i]].mean()
                column4_data = data[data.columns[1+i]].mean()
                labels = ['CIE', 'SEE']
                values = [column3_data, column4_data]
                fig = go.Figure(data=[go.Pie(labels=labels,values=values)])
                fig.update_layout(width=700, height=700)
                st.plotly_chart(fig)
     
     
                st.markdown("<h5>8. Top 10 Performers in the Subject</h5></div>", unsafe_allow_html=True)
                st.write("The below bar chart showcases the top 10 highest-scoring students in the subject, displaying their names and marks for easy comparison and analysis.")
                sorted_data = data.sort_values(by=data.columns[2+i],ascending=True)
                sorted_data = sorted_data[[data.columns[2],data.columns[2+i]]].tail(12)
                fig = px.bar(sorted_data, x=data.columns[2+i], y=data.columns[2],color=data.columns[2+i],color_continuous_scale=['#90EE90', 'green','#006400'])
                fig.update_layout(xaxis_title='Total Marks in the Subject')
                st.plotly_chart(fig)
     
                st.markdown("<h1></h1></div>", unsafe_allow_html=True)
                st.write("The below table displays the top 10 students who have performed exceptionally well in the subject, including their overall performance in the semester.")
                sorted = data.sort_values(by=data.columns[2+i],ascending=False)
                sorted = sorted[['USN',data.columns[2],data.columns[2+i],'GRADE','PERCENTAGE']].head(10)
                sorted = sorted.rename(columns={data.columns[2+i]: 'Total Marks'})
                # CSS to inject contained in a string
                hide_table_row_index = """
                            <style>
                            thead tr th:first-child {display:none}
                            tbody th {display:none}
                            </style>
                            """
                
                # Inject CSS with Markdown
                st.markdown(hide_table_row_index, unsafe_allow_html=True)
                st._legacy_table(sorted[['USN',data.columns[2],'Total Marks','GRADE','PERCENTAGE']])




    with tab3:
    # if selected == "Student wise Analysis":

      with st.spinner("Loading..."):
        data = pd.read_excel(xls, sheet_name=sheet_name)
 
  
        student_name = st.selectbox("Select a student:", data[data.columns[2]].unique(),index=1)

    
        # Filter the data to get the marks of the selected student
        student_data = data[data[data.columns[2]] == student_name]
        st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)

        NAME = student_data[data.columns[2]].values[0]
        USN = student_data[data.columns[1]].values[0]
        

        with open('style1.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

        st.markdown('### STUDENT DETAILS:')
        col1, col2= st.columns(2)
        col1.metric("NAME:",NAME)
        col2.metric("USN:",USN)


        st.markdown("<div style='text-align:center;'><h1>          </h1></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;'><h3>MARKS CARD FOR THE SEMESTER </h3></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
        st.write("The below table presents a comprehensive view of the student's marks sheet for the specific semester, including the percentage, total marks, and grade obtained by the student ")
        
        subjects = []
        for i in range(3, 36, 4):
          if not pd.isnull(data.iloc[0, i]):
            student_data[data.columns[i+2]] = pd.to_numeric(student_data[data.columns[i+2]], errors='coerce')

            subject = {}
            subject["Subject Name"] = data.iloc[0, i]
            subject["CIE Marks"] = student_data[data.columns[i]].values[0]
            subject["SEE Marks"] = student_data[data.columns[i+1]].values[0]
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
        
 
        col4.metric("RESULTS:", Results)
        col5.metric("PASSED SUBJECTS:",Passed_Subjects)
        col6.metric("FAILED SUBJECTS",Failed_Subjects)



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
            fig = px.bar(x=subject_names, y=subject_marks)
            fig.update_layout(xaxis_title='Subject', yaxis_title='Total Marks', width=700, height=600)
            st.plotly_chart(fig)

st.cache()
def USN_analysis():

    input_str = st.text_input("Enter USN:",placeholder="1RF00XX000",help="Make sure the USN is in capitals")
    st.button("Submit")
    
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





        sheet_name = st.selectbox("Select the semester:", xls.sheet_names,key='USN')
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




   







def loginpage():
 

 
#  tb1, tb2 = st.tabs(['\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0 \u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0Login\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0 \u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0   ','\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0 \u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0 \u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0Signup\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0 \u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0 \u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0'])
 selected = option_menu(
        menu_title=None,
        options=["Login","Signup"],
        icons=["person-workspace","person"],
        orientation="horizontal",
    ) 
 if selected == 'Login':

    DETAA = "d0mmbh4h7yn_aVTdWVFf5UQTxWHZZmeX144mkXaiD9Ht"
    det = Deta(DETAA)
    dt = det.Base("faculty_db")
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
        st.markdown("<div style='text-align:center;'><h1>RESULT ANALYSIS 📈</h1></div>", unsafe_allow_html=True,)
        st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
        st.markdown(
        f"""
        <style>
            .css-1hynsf2.e1tzin5v3{{
                visibility: hidden;

            }}
        </style>
        """,
        unsafe_allow_html=True,
        )


        try:

            if '1RF' not in usernames :
                st.sidebar.success("Welcome "+namess+"")
                student_authenticator.logout("Logout", "sidebar")
    
                tab1, tab2 = st.tabs(['\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0 \u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0Semester Results Analysis\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0 \u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0   ','\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0 \u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0 \u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0Student Performance Analysis\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0 \u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0 \u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0'])
                 
                with tab1:
                    student_analysis()
                
                
                with tab2:
                    USN_analysis()

    
            else:
                st.info('Please logout of Student Account to sign in as student')

        except Exception as e:
            st.info('Please logout of Department Account to login in as a student!')




 elif selected == 'Signup':
    DETAA = "d0mmbh4h7yn_aVTdWVFf5UQTxWHZZmeX144mkXaiD9Ht"
    det = Deta(DETAA)
    dt = det.Base("faculty_db")
    
    
    def insert_user(username, name, password):
        """Returns the user on a successful user creation, otherwise raises and error"""
        return dt.put({"key": username, "name": name, "password": password})

    
    with st.form("my_form"):
        col1, col2 = st.columns(2)
        with col1: 
            firstname = st.text_input("First Name")
        with col2:
            lastname = st.text_input("Last Name")
        name = ''+firstname+'\u00a0'+lastname+''
        username = st.text_input("Enter College/Work Email ID:", placeholder="example.rvitm@rvei.edu.in")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.form_submit_button("Send OTP"):
            if password != confirm_password:
                st.error("Passwords do not match.")
            else:
                # Generate a 6-digit random OTP
                otp = str(random.randint(100000, 999999))
                # Set up the email message
                sender_email = "rvit21bis025.rvitm@rvei.edu.in" 
                receiver_email = username
                message = f"Subject: OTP Verification\n\nYour OTP is: {otp}"
                # Send the email
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(sender_email, "rsst123456") 
                    server.sendmail(sender_email, receiver_email, message)
                # Store the OTP for later use
                st.session_state["otp"] = otp
                st.success("OTP sent to email.")
        
        # Check if the OTP has been sent and received before displaying the OTP form
        if "otp" in st.session_state:
            entered_otp = st.text_input("Enter OTP")
            if st.form_submit_button("Submit"):
                if entered_otp == st.session_state["otp"]:
                    # Create the user
                    usernames = [username]
                    names = [name]
                    passwords = [confirm_password]
                    hashed_passwords = stauth.Hasher(passwords).generate()
                    for (username, name,  hash_password) in zip(usernames, names,  hashed_passwords):
                        insert_user(username, name, hash_password)
                 
                    st.success("You have successfully signed up, Please login to continue!")
                else:
                    st.error("Incorrect OTP. Please try again.")



loginpage()