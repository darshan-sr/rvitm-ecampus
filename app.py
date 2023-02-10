import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from streamlit_option_menu import option_menu
import base64 

import streamlit_authenticator as stauth
import database as db


from datetime import datetime
from google.cloud import firestore
from google.cloud.firestore import Client


from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph,Image
import io
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import textwrap
import datetime
import zipfile

# Set page Configuration 

st.set_page_config(page_title='Student progress Analysis',
page_icon='RVlogo.png', 
initial_sidebar_state="expanded") 

# Hide default header footer and hamburger menu




hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# applying CSS styling for the sidebar and adding the sidebar RV logo

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
st.sidebar.title("")
st.sidebar.title("")


# Student analysis Choice and the links for the excel sheets

def student_analysis():
    st.markdown("<div style='text-align:center;'><h1>STUDENT MARKS ANALYSIS 📈</h1></div>", unsafe_allow_html=True,)
    st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)
 

    batch_choice = st.selectbox("Select the year of the Batch", ["2019 Batch", "2020 Batch","2021 Batch", "2022 Batch"])
    
    if batch_choice == "2021 Batch":
        branch_choice = st.selectbox("Select the Branch", ["CSE", "ISE","EC", "ME"])
        
        if branch_choice == "CSE":
            try:
                xls = pd.ExcelFile('2021.CSE.StudentMarksSheet.xlsx')
                plot_analysis(xls)
            except:
                st.write("Data not found")

        if branch_choice == "ISE":

            url = "https://docs.google.com/spreadsheets/d/1LFIKxpYN1tNYqD03U6RYb58Slq32lk2P/export?format=xlsx"
            xls = pd.ExcelFile(url, engine='openpyxl')
            plot_analysis(xls)


        if branch_choice == "ECE":
            try:
                xls = pd.ExcelFile('/Users/darshangowda/Documents/SavedXLSX/2021/ECE/2021.ECE.StudentMarksSheet.xlsx')
                plot_analysis(xls)
            except:
                st.write("Data not found")

        if branch_choice == "ME":
            try:
                xls = pd.ExcelFile('/Users/darshangowda/Documents/SavedXLSX/2021/ME/2021.ME.StudentMarksSheet.xlsx')
                plot_analysis(xls)
            except FileNotFoundError:
                st.write("Data not found")

    if batch_choice =="2020 Batch":
        branch = st.selectbox("Select the Branch", ["CSE", "ISE","EC", "ME"])

        if branch == "ISE":
            xls = pd.ExcelFile("/Users/darshangowda/Documents/2020.ISE-7.xlsx")
            plot_analysis(xls)

# Plotting all the analysis for Class Analysis Section

def plot_analysis(xls):

    data = pd.read_excel(xls,sheet_name=None)
    
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
    selected = option_menu(
        menu_title=None,
        options=["Semester Analysis","Subject Wise Analysis","Student wise Analysis"],
        icons=["person-workspace","stack","person"],
        orientation="horizontal",
        
    )
    
    
    
    if selected == "Semester Analysis":
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



    elif selected == "Subject Wise Analysis":

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




    elif selected == "Student wise Analysis":

  
        student_name = st.selectbox("Select a student:", data[data.columns[2]].unique(),index=1)

    
        # Filter the data to get the marks of the selected student
        student_data = data[data[data.columns[2]] == student_name]
        st.markdown("<div style='text-align:center;'><h1></h1></div>", unsafe_allow_html=True)

        NAME = student_data[data.columns[2]].values[0]
        USN = student_data[data.columns[1]].values[0]
        

        with open('/Users/darshangowda/StreamlitApp/style1.css') as f:
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


def USN_analysis():

    input_str = st.text_input("Enter USN:",placeholder="1RF00XX000",help="Make sure the USN is in capitals")
    st.button("Submit")
    
    if "21IS" in input_str:
        url = "https://docs.google.com/spreadsheets/d/1LFIKxpYN1tNYqD03U6RYb58Slq32lk2P/export?format=xlsx"
        xls = pd.ExcelFile(url,engine='openpyxl')
        StudentMarks(xls,input_str)

    if "20IS" in input_str:
      
        url = "/Users/darshangowda/Documents/2020.ISE-7.xlsx"
        xls = pd.ExcelFile(url,engine='openpyxl')
        StudentMarks(xls,input_str)




def StudentMarks(xls,input_str):

        data = pd.read_excel(xls)
        student_data = data.loc[data['USN'] == input_str]
        BACK = student_data[data.columns[44]].values[0]
        NAME = student_data[data.columns[2]].values[0] 
        USN = student_data[data.columns[1]].values[0]
        with open('/Users/darshangowda/StreamlitApp/style1.css') as f:
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
            TCGPA = round(CGPAA/10,1)

        st.markdown('### STUDENT DETAILS:')
        col1, col2= st.columns(2)
        col1.metric("NAME:",NAME)
        col2.metric("USN:",USN)
        col1, col2= st.columns(2)
        col1.metric("FAILED SUBJETS:",BACK)
        col2.metric("CGPA:",TCGPA)


        
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
                subject_marks_text = ['{:.0f}'.format(x) for x in subject_marks]
                fig = px.bar(x=subject_names, y=subject_marks,text=subject_marks_text)
                fig.update_layout(xaxis_title='', yaxis_title='Total Marks', width=700, height=600)
                st.plotly_chart(fig)
            if chart_choice == "Area Graph": 
                fig = px.area(x=subject_names, y=subject_marks)
                fig.update_layout(xaxis_title='', yaxis_title='Total Marks', width=700, height=600)
                st.plotly_chart(fig)

            if chart_choice == "Funnel": 
                fig = px.funnel(x=subject_names, y=subject_marks)
                fig.update_layout(xaxis_title='', yaxis_title='Total Marks', width=700, height=600)
                st.plotly_chart(fig)

            if chart_choice == "Grouped Bar Chart":
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


def department_login():
    
    users = db.fetch_all_users()
    usernames = [user["key"] for user in users]
    names = [user["name"] for user in users]
    hashed_passwords = [user["password"] for user in users]

    authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
        "sales_dashboard", "abcdef", cookie_expiry_days=30)
    name, authentication_status, username = authenticator.login("LOGIN", "main")

    if authentication_status == False:
        st.error("Username/password is incorrect")


    if authentication_status:
        st.success("Logged in successfully")
        authenticator.logout("Logout", "sidebar")

        if username == "ISE":
            batch_choice = st.selectbox("Select the year of the Batch", ["2019 Batch", "2020 Batch","2021 Batch", "2022 Batch"])
            if batch_choice == "2021 Batch":
                uploaded_file = st.file_uploader("Choose a file", type="xlsx")
                if uploaded_file:
                    with open("/Users/darshangowda/Documents/SavedXLSX/2021/ISE/2021.ISE.StudentMarksSheet.xlsx", "wb") as f:
                        f.write(uploaded_file.read())
                    st.success("File saved in desired folder.")





def how_to_use():
    st.markdown("<div style='text-align:center;'><h1>GUIDE TO USE THE WEBSITE 👨🏻‍💻</h1></div>", unsafe_allow_html=True,)
    video_iframe = '<iframe width="700" height="405" src="https://youtube.com/dQw4w9WgXcQ" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    st.write(video_iframe, unsafe_allow_html=True)


def Submit_Feedback():
    
    st.header(":mailbox: Submit a Feedback!")
    st.title("")
    st.write("We are collecting feedback for our Student Marks Analysis app which is used by college lectures and students. Your input on what can be improved and if there are any bugs will greatly assist in the continued development of the app. Your suggestions for new features would also be appreciated. Please fill out the contact form to share your thoughts and feedback. Your contributions will help make the app an even more useful tool for the college community")
    st.title("")

    @st.experimental_singleton
    def get_db():
        db = firestore.Client.from_service_account_json("/Users/darshangowda/Desktop/feedback/key.json")
        return db


    def post_message(db: Client, input_name, input_mail, input_message):
        payload = {
            "name": input_name,
            "mail": input_mail,
            "message": input_message,
            "date": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        }
        doc_ref = db.collection("Feedback").document()
    
        doc_ref.set(payload)
        return


    def main():

        db = get_db()

        with st.form(key="form"):
            input_name = st.text_input("Your Name: ",placeholder="Name")
            input_mail = st.text_input("Your college Mail ID: ",placeholder="example.rvitm@rvei.edu.in")
            input_message = st.text_area("Your Feedback: ",placeholder="Your Feedback Here")
    
            if st.form_submit_button("Submit"):
                post_message(db, input_name, input_mail, input_message)
                st.success("Your Feedback was Submitted!")
            


    if __name__ == "__main__":
       
        main()


def about():

    st.title("About")

def generate_pdf(df, row,Branch_Choice,test_choice,submission_d):
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

    image_path = "/Users/darshangowda/Desktop/Header_RV.png"
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

    image_path = "/Users/darshangowda/Desktop/RV_Signature.png"
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
        df = pd.read_excel(uploaded_file)
        st.write("Generating Progress Report...")
        
        progress_bar = st.progress(0)
        
        for i in range(2,df.shape[0]):
            buffer = generate_pdf(df, i,Branch_Choice,test_choice,submission_d)
            file_name = f"{df.iloc[i, 2]}.pdf"
        
            with open(file_name, "wb") as f:
                f.write(buffer.getvalue())
            
            with open(file_name, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            
            download_link = f'<a href="data:application/zip;base64,{b64}" download="{file_name}">Download {file_name}</a>'
            st.markdown(download_link, unsafe_allow_html=True)
            
            progress_value = int((i - 1) / (df.shape[0] - 2) * 100)
            progress_bar.progress(progress_value)




def progress_report():
    users = db.fetch_all_users()
    usernames = [user["key"] for user in users]
    names = [user["name"] for user in users]
    hashed_passwords = [user["password"] for user in users]

    authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
        "sales_dashboard", "abcdef", cookie_expiry_days=30)
    name, authentication_status, username = authenticator.login("LOGIN", "main")

    if authentication_status == False:
        st.error("Username/password is incorrect")


    if authentication_status:
        authenticator.logout("Logout", "sidebar")
        progress_pdf()

with st.sidebar:
    
        
    with open('style1.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 
    selected = option_menu(
            menu_title= "MAIN MENU",
            options= ["Class Analysis","Student Analysis","Department Login","Progress Report Generation","Attendance","Submit Feedback","About"],
            icons= ["person-workspace","person","briefcase","file-earmark-break","file-bar-graph","envelope-plus","code"],
            menu_icon="list",
            default_index=0,
            orientation="horizantal",
        )
if selected == "Class Analysis":
    student_analysis()
if selected == "Student Analysis":
    USN_analysis()
if selected == "Department Login":
    st.title("DEPARTMENT LOGIN")
    department_login()
if selected == "Progress Report Generation":
    progress_report()
if selected == "Submit Feedback":
    Submit_Feedback()
if selected == "About":
    about() 
