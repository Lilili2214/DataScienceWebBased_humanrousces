import streamlit as st
import streamlit as st
from PIL import Image
st.set_page_config(layout="wide",
    page_title="Talent Tracker",
    page_icon= 	":busts_in_silhouette:",
)






st.sidebar.success("Select a page above")

 

st.title("Welcome to our Real-Time Talent Tracker System")


st.write("""
This system is designed to help you manage your workforce and evaluate their performance in real-time. 
It consists of several pages, each with a specific purpose:
""")

st.header("Workforce Management")
st.markdown("<a href='http://localhost:8501/Workforce_Management' target='_blank'>Workforce Management</a>", unsafe_allow_html=True)

st.write("""
On the Workforce Management page, you can view and manage information about your workforce. 
You can see various metrics related to employee performance and make informed decisions about workforce management.
""")


st.header("Performance")
st.markdown("<a href='http://localhost:8501/Performance' target='_blank'>Performance</a>", unsafe_allow_html=True)

st.write("""
The Performance page provides insights into the performance of your employees. 
You can view individual performance metrics, team performance metrics, and more.
""")


st.header("Prediction")
st.markdown("<a href='http://localhost:8501/Prediction' target='_blank'>Prediction</a>", unsafe_allow_html=True)

st.write("""
The Prediction page is divided into three tabs:
""")


st.subheader("Free Prediction")
st.write("""
In this tab, you can try out the prediction metrics and make predictions freely based on the input data.
""")

st.subheader("Employee Search")
st.write("""
This tab allows you to search for an employee by name and see insights related to their performance and potential.
""")

st.subheader("Promotion Potential")
st.write("""
In the Promotion Potential tab, you can see a group of employees who have the potential to be considered for promotion. 
You have two options in this tab:
1. Upload a CSV file with employee data.
2. Choose a department to view its employees.
""")


st.write("""
Feel free to explore each page and make full use of the features provided. Enjoy!
""")
