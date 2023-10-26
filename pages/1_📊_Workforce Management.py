import streamlit as st
import snowflake.connector
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime
from connecttion import query, categorize_age, categorize_salary


st.set_page_config(layout="wide" )

# Convert the data into a pandas DataFrame with column headers
df= query("workforce")
df_re= query('retention_insight')
# data for age range of retention 
df['EMPLOYEE_ID'] = df['EMPLOYEE_ID'].astype('int64')
df_re['EMPLOYEE_ID'] = df_re['EMPLOYEE_ID'].astype('int64')

df['SALARY_RANGE'] = df['ANNUAL_INCOME'].apply(categorize_salary)
df_merge = pd.merge(df, df_re, on= "EMPLOYEE_ID", how='right')
#---------------Data for full time and part time structure
df['worktype']=None
df['worktype'] = df['WORKSCHEDULE_TRANSLATION'].apply(lambda x: 'Full-time' if 'Full-time' in x else ('Part-time' if 'Part-time' in x else 'Unspecified'))

df['HIREDATE'] = pd.to_datetime(df['HIREDATE'])

df['year'] = df['HIREDATE'].dt.year
currentyear= datetime.now().year
df = df[df['year'].between(currentyear-10, currentyear)]


total_counts = df['year'].value_counts()

job_counts = df.groupby('year')['worktype'].value_counts()

percentages = job_counts / total_counts * 100

percentages = percentages.reset_index()

percentages.columns = ['Year', 'worktype', 'Percentage']

pivot_df = percentages.pivot(index='Year', columns='worktype', values='Percentage')
#filter 


#-------------------------------------------------------
with st.container():
    st.header(":busts_in_silhouette: Workforce Dashboard")
    st.markdown("""
        <div style="background-color: lightblue; padding: 10px; border-radius: 5px;">
            <h2 style="color: black; text-align: center;">Workforce Dashboard</h2>
        </div>
        """, unsafe_allow_html=True)
    # Create 3 columns with different widths
    st.markdown("<br>", unsafe_allow_html=True) 
    col1, col2, col3= st.columns([0.2,0.4, 0.4])
    st.dataframe(df_merge)
    # Use the columns for displaying content
    
    with col1:
        #filter 
        selected_department = st.selectbox('Select a department',options=['all'] + list(df['DEPARTMENT'].unique())  # The options in the selectbox are 'all' and the unique values in the 'department' column
        )
        if selected_department != 'all':
            df_merge = df_merge[df_merge['DEPARTMENT'] == selected_department]
            df = df[df['DEPARTMENT'] == selected_department]
        else:
            df_merge = df_merge
            df = df
        selected_SAL = st.selectbox('Select a salary',options=['all'] + list(df['SALARY_RANGE'].unique())  # The options in the selectbox are 'all' and the unique values in the 'department' column
        )
        
        if selected_SAL  != 'all':
            df_merge = df_merge[df_merge['SALARY_RANGE'] == selected_SAL ]
            df = df[df['SALARY_RANGE'] == selected_SAL ]
        else:
            df_merge = df_merge
            df = df
        
    with col2:
        values =df.groupby('GENDER')['GENDER'].value_counts()
        layouts = go.Layout(autosize=False,  width=400, height=350)
        colors= ['#0089BA','#C4FCEF']
        fig = go.Figure(data=go.Pie(labels=['Female', "Male"], values=values, marker=dict(colors=colors)),layout=layouts)  # Use the layout defined above)
        st.subheader("Gender Ratio")
        st.plotly_chart(fig)
        df_merge['age_range']= df_merge['AGE'].apply(categorize_age)
        df_merge['percentage']= df_merge.groupby('age_range')['age_range'].transform(lambda x: len(x)/df_merge.shape[0]*100)
        
        df_merge = df_merge.sort_values('age_range')
        df_merge_NO= df_merge[(df_merge['LENGTHOFSERVICE'] >= 0) & (df_merge['LENGTHOFSERVICE'] <= 3)]
        fig = go.Figure(data=[go.Bar(
        x=df_merge_NO['age_range'].unique(), 
        y=df_merge_NO.groupby('age_range')['percentage'].first(),
        text=[f"{x:.2f}%" for x in df_merge_NO.groupby('age_range')['percentage'].first()],
        textposition='auto',)])

# Set the layout attributes
        fig.update_layout(
            
            xaxis_title='Age Range',
            yaxis_title='Percentage',
            autosize=False,
            width=500,
            height=470,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
        )
        st.subheader("Notices During First Three Year By Age Group")
        # Display the plot in Streamlit
        st.plotly_chart(fig)
    with col3:
        st.subheader("Full-time and Part-time Employees")
        st.line_chart(pivot_df)
        df_merge['Percentage'] = df_merge.groupby('LENGTHOFSERVICE')['LENGTHOFSERVICE'].transform(lambda x: len(x) / df_merge.shape[0]*100)
        df_merge = df_merge.sort_values('LENGTHOFSERVICE')
# Create an area chart with custom colors using Plotly
        layouts1 = go.Layout(autosize=True,  width=530, height=470,xaxis_title='Years')
        fig = go.Figure(layout=layouts1)
        fig.add_trace(go.Scatter(x=df_merge['LENGTHOFSERVICE'], y=df_merge['Percentage'],fill='tozeroy',mode='lines+markers',line_color='#0089BA',fillcolor='#C4FCEF'))
        fig.update_yaxes(range=[0, max(df_merge['Percentage'].max(), df_merge['Percentage'].max())*1.5])
        st.subheader("Time To Quit The Job")
        # Display the plot in Streamlit
        st.plotly_chart(fig)
        
