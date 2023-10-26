import streamlit as st
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import plotly.express as px
import requests
from connecttion import filter_by_salary,categorize_salary,reoder, query, search,predict_promotion,get_feature
import numpy as np
import plotly.graph_objects as go
from employee import Employee
from train_model import get_feature_retention
from sklearn.decomposition import PCA
import random
import json
import plotly.figure_factory as ff
from sklearn.preprocessing import LabelEncoder

# Assume df is your DataFrame
le = LabelEncoder()


st.set_page_config(page_title="Prediction",layout="wide")
with open('./file.json', 'r') as f:
    data_img = json.load(f)
df_img = pd.DataFrame(list(data_img.items()), columns=['Index', 'Image_Path'])

df_em= query("dim_employees")
df_reten= query("retention_meta")
dataset = df_reten.to_dict(orient='records')
response= requests.post(f'http://localhost:8000/predict_re', json={"data": dataset})
df = pd.DataFrame.from_dict(response.json())
df= pd.concat([df_reten[[i for i in df_reten.columns if i !='ATTRITION']], df.reset_index()], axis=1)
df_workforce= query("workforce")


# Load and preprocess the data
employee_dff = pd.read_csv("./employee_data.csv")
employee_dff['Attrition'] = employee_dff['Attrition'].apply(lambda x: 1 if x == 'Yes' else 0)
employee_dff['OverTime'] = employee_dff['OverTime'].apply(lambda x: 1 if x == 'Yes' else 0)
employee_dff['Over18'] = employee_dff['Over18'].apply(lambda x: 1 if x == 'Y' else 0)
employee_df=employee_dff.drop(['EmployeeCount', 'StandardHours', 'Over18', 'EmployeeNumber'], axis=1)
columns_to_encode = ['Attrition', 'BusinessTravel', 'Department', 'EducationField', 'Gender', 'JobRole', 'MaritalStatus', 'OverTime']

for column in columns_to_encode:
    employee_df[column] = le.fit_transform(employee_df[column])


correlations = employee_df.corr()




heatmap = go.Heatmap(z=correlations.values,
                     x=list(correlations.columns),
                     y=list(correlations.index),
                     colorscale='rdgy',  # use the 'Viridis' color scale
                     zmin=-1, zmax=1)

layout = go.Layout(title='Correlation Heatmap',
                   width=800, height=800,
                   xaxis=dict(ticks='', nticks=36),
                   yaxis=dict(ticks=''),
                   plot_bgcolor='rgba(0,0,0,0)')

fig = go.Figure(data=[heatmap], layout=layout)
fig.update_layout(width=1200, height=1200)

# Display the plot in Streamlit
st.plotly_chart(fig)
st.write("""
- Job level is strongly correlated with total working hours
- Monthly income is strongly correlated with Job level
- Monthly income is strongly correlated with total working hours
- Age is stongly correlated with monthly income
""")

st.header("Employees Who Likely to Leave")


mean_PERFORMANCERATING = df_reten['PERFORMANCERATING'].mean()
mean_WORKLIFEBALANCE = df_reten['WORKLIFEBALANCE'].mean()
mean_RELATIONSHIPSATISFACTION = df_reten['RELATIONSHIPSATISFACTION'].mean()
mean_JOBSATISFACTION = df_reten['JOBSATISFACTION'].mean()
mean_JOBINVOLVEMENT = df_reten['JOBINVOLVEMENT'].mean()
mean_ENVIRONMENTSATISFACTION = df_reten['ENVIRONMENTSATISFACTION'].mean()
mean_MONTHLYINCOME= df_reten['MONTHLYINCOME'].mean()

  
response= requests.post(f'http://localhost:8000/predict_re', json={"data": dataset})
df = pd.DataFrame.from_dict(response.json())
df= pd.concat([df_reten[[i for i in df_reten.columns if i !='ATTRITION']], df.reset_index()], axis=1)
df['salary_category'] = df['MONTHLYINCOME'].apply(categorize_salary)

col1, col2= st.columns([0.4,0.6])

departments = df_reten['DEPARTMENT'].unique().tolist()
departments.insert(0, "All")
selected_department = st.sidebar.selectbox('Select a department', departments)

if selected_department != "All":    
    df_filter= df[df['DEPARTMENT']==selected_department]
    
else:
    df_filter = df
    

df_filter=df_filter[df_filter['Predicted Status']==1]

salary_ranges = ['All','<$40000', '$40000-$59999', '$60000-$79999', '$80000-$99999', '$100000-$119999', '$120000-$139999', '$140000-$159999', '$160000-$179999', '$180000-$199999', '>= $200000']
selected_range = st.sidebar.selectbox('Select a salary range:', salary_ranges)
joblevel= df_reten['JOBLEVEL'].unique().tolist()
joblevel.insert(0, "All")

selected_joblv= st.sidebar.selectbox("Choose Job Level",joblevel)
if selected_range=="All" and selected_joblv=="All":
    filtered_df=df_filter.copy()
elif selected_joblv=="All" :
    filtered_df = filter_by_salary(df_filter, selected_range)
elif selected_range=="All":
    filtered_df= df_filter[df_filter['JOBLEVEL']==selected_joblv]
else:
    filtered_df = filter_by_salary(df_filter, selected_range)
    filtered_df= df_filter[df_filter['JOBLEVEL']==selected_joblv]


st.subheader("List of all Employees have predicted result as likely to quit ")
st.write(filtered_df[[i for i in filtered_df.columns if i!='Predicted Status']])

filtered_df['EMPLOYEENUMBER'] = filtered_df['EMPLOYEENUMBER'].astype(str)

# Convert the 'EMPLOYEE_ID' column to string
df_workforce['EMPLOYEE_ID'] = df_workforce['EMPLOYEE_ID'].astype(str)

# Now you can merge
df_expan = pd.merge(filtered_df, df_workforce, left_on='EMPLOYEENUMBER', right_on='EMPLOYEE_ID')
df_expan= pd.merge(filtered_df,df_workforce,left_on='EMPLOYEENUMBER', right_on= "EMPLOYEE_ID")
df_expan.columns= df_expan.columns.astype(str)
df_expan= df_expan.sort_values('1', ascending=False)
df_expander = df_expan[df_expan['1'] > 0.85]
st.subheader(f"Found {len(df_expander)} employees likely to quit with probability of more than 85%")
for index, row in df_expander.iterrows():
    with st.expander(f"{index}"):
        col1, col2 = st.columns([0.4, 0.6])
        with col1:
            st.image(df_img.iloc[random.randint(0,len(df_img)-1)]['Image_Path'], width=200)
            st.metric(label=f"Job Role-Level: {row['JOBLEVEL']}", value=row['JOBROLE_x'])   
        with col2:
            st.subheader(row['NAME'])
            col3, col4= st.columns(2)
            
            with col3:
                st.metric(label="Probability to quit (%)",value=round(row["1"]*100,2))
                st.metric(label="Monthly Income ($)",value=row['MONTHLYINCOME'])
            with col4:
                st.metric(label="Age",value=row['AGE_x'])
                st.metric(label="Total working years",value=row['TOTALWORKINGYEARS'])
        col5, col6= st.columns(2)
        with col5:
            fig = go.Figure(data=[
                    go.Bar(name='Mean', x=['RELATIONSHIPSATISFACTION', 'JOBSATISFACTION', 'JOBINVOLVEMENT', 'ENVIRONMENTSATISFACTION', 'PERFORMANCERATING', 'WORKLIFEBALANCE'], y=[mean_RELATIONSHIPSATISFACTION, mean_JOBSATISFACTION, mean_JOBINVOLVEMENT, mean_ENVIRONMENTSATISFACTION, mean_PERFORMANCERATING, mean_WORKLIFEBALANCE]),
                    go.Scatter(name='Row Value', x=['RELATIONSHIPSATISFACTION', 'JOBSATISFACTION', 'JOBINVOLVEMENT', 'ENVIRONMENTSATISFACTION', 'PERFORMANCERATING', 'WORKLIFEBALANCE'], y=[row['RELATIONSHIPSATISFACTION'], row['JOBSATISFACTION'], row['JOBINVOLVEMENT'], row['ENVIRONMENTSATISFACTION'], row['PERFORMANCERATING'], row['WORKLIFEBALANCE']], mode='lines+markers')
                ])

            fig.update_layout(barmode='group', autosize=False, width=500, height=400)

            st.plotly_chart(fig)   
        with col6:
            categories = ['Employee Salary', 'Average Salary']
            values = [row['MONTHLYINCOME'], mean_MONTHLYINCOME]

            fig = go.Figure(data=[
                go.Bar(x=categories, y=values)
            ])

            fig.update_layout(title_text='Salary Comparison',autosize=False, width=500, height=400)

            st.plotly_chart(fig)

                                
        


