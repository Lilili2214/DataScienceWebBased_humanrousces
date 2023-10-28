import streamlit as st
import snowflake.connector
import pandas as pd
import plotly.graph_objects as go

from connecttion import query, categorize_age, categorize_salary
import plotly.express as px

import numpy as np
st.set_page_config(layout="wide" )

df= query("workforce")
df_re= query('retention_insight')
df_re_= query("retention_")
df['EMPLOYEE_ID'] = df['EMPLOYEE_ID'].astype('int64')
df_re['EMPLOYEE_ID'] = df_re['EMPLOYEE_ID'].astype('int64')
df_per= query("performance")
df_monthly= df['ANNUAL_INCOME']/12
st.header("TALENT MANAGEMENT")
df_merge= pd.merge(df, df_re,on="EMPLOYEE_ID")
st.write(df_re_)
df_len= df_re_[df_re_["YEARSATCOMPANY"].isin([0,1,2,3,5])]
df_re_pe= df_per.merge(df_len, right_on="EMPLOYEENUMBER", left_on='EMPLOYEE_ID')
df_re_pe= df_re_pe[['EMPLOYEE_ID','TYPE','RATING','YEARSATCOMPANY','ENVIRONMENTSATISFACTION','RELATIONSHIPSATISFACTION','JOBINVOLVEMENT']]
st.write(df_re_pe)


values = [1, 2, 3, 4]
ratios = [0.3, 0.12, 0.45, 0.13]


random_values = np.random.choice(values, size=len(df_re_pe), p=ratios)


df_re_pe['new_rating'] = random_values

df_re_pe['RATING'] = df_re_pe['new_rating']
df_re_pe.drop(columns=['new_rating'], inplace=True)
st.markdown("<h2 style='text-align: left; color: black;'>TALENT MANAGEMENT</h2>", unsafe_allow_html=True)
col0_0, col0_1= st.columns(2)
with col0_0:
    col3, col4, col5= st.columns([0.3, 0.4, 0.3])
    with col3:
        df_1= df[df['STATUS']==1]
        st.metric(label="EMPLOYEES", value=len(df_1))
    with col4:
        st.metric(label="MONTHLY SALARY", value=f"${int(df_monthly.sum())}")
    with col5:
        st.metric(label="JOB ROLE", value= len(df['JOBROLE'].unique()))
            

col1, col2=st.columns(2)
with col1:
    
    grouped = df_merge.groupby(['DEPARTMENT', 'TYPE']).size().reset_index(name='counts')

   
    total_counts = grouped['counts'].sum()

    
    grouped['Percentage'] = grouped['counts'] / total_counts * 100

    
    grouped['Percentage_Text'] = grouped['Percentage'].apply(lambda x: f'{x:.0f}%')

    fig = px.bar(grouped, x='DEPARTMENT', y='Percentage', color='TYPE', text='Percentage_Text', barmode='group',color_discrete_sequence=['#63B1C5', '#AA467E'])


    fig.update_traces(texttemplate='%{text}', textposition='outside')
    st.markdown("<h2 style='text-align: center; color: black;'>TALENT TURNOVER RATE</h2>", unsafe_allow_html=True)
    

    st.plotly_chart(fig)
    st.markdown("<h2 style='text-align: center; color: black;'></h2>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: black;'></h2>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: black;'></h2>", unsafe_allow_html=True)
    grouped = df_merge[(df_merge['TYPE'] == 'Terminated for Cause') & (df_merge['LENGTHOFSERVICE'] != 3)].groupby(['LENGTHOFSERVICE']).size().reset_index(name='counts')
    total_counts = grouped['counts'].sum()
    grouped['Percentage'] = grouped['counts'] / total_counts * 100
    grouped= grouped[grouped['Percentage']>5]
    grouped['Percentage_Text'] = grouped['Percentage'].apply(lambda x: f'{x:.0f}%' if x > 5 else '')
    fig = px.bar(grouped, x='LENGTHOFSERVICE', y='Percentage', text='Percentage_Text', barmode='group', color_discrete_sequence=['#63B1C5'])
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    st.markdown("<h2 style='text-align: center; color: black;'>FIRED TALENTS</h2>", unsafe_allow_html=True)
    st.plotly_chart(fig)


with col2:
    
    st.markdown("<h2 style='text-align: center; color: black;'>TALENT SATISFACTION</h2>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: black;'></h2>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: black;'></h2>", unsafe_allow_html=True)
    
    temp = df_re_.groupby("YEARSATCOMPANY").size()
    col3, col4, col5= st.columns([0.6, 0.1,0.3])
    with col3:
        df_re_pe['average']= (df_re_pe['ENVIRONMENTSATISFACTION']+df_re_pe['JOBINVOLVEMENT']+df_re_pe['RELATIONSHIPSATISFACTION'])/3
        df_use= df_re_pe[df_re_pe['YEARSATCOMPANY']==0]
       


        percentage = (len(df_use[df_use['average'] > 2]) / len(df_use)) * 100

        
        fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=percentage,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "(%) OF SCORE WITH 'GOOD' OR 'VERY GOOD'"},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "#AA467E"}, 
            'steps': [
                {'range': [0, 100], 'color': "#63B1C5"},
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': percentage}
                }
            ))
        fig.update_layout(autosize=False,width=450,height=465)
        st.plotly_chart(fig)
    with col5:
        st.metric(label="", value="")
        st.metric(label="", value="")
        df_use= df_re_pe[df_re_pe['YEARSATCOMPANY']==1]
        percentage = (len(df_use[df_use['average'] > 2]) / len(df_use)) * 100

        st.metric(label="1 YEAR", value=round(percentage,1))
        df_use= df_re_pe[df_re_pe['YEARSATCOMPANY']==2]
        percentage = (len(df_use[df_use['average'] > 2]) / len(df_use)) * 100

        st.metric(label="2 YEAR", value=round(percentage,1))
        df_use= df_re_pe[df_re_pe['YEARSATCOMPANY']==5]
        percentage = (len(df_use[df_use['average'] > 2]) / len(df_use)) * 100

        st.metric(label="5 YEAR", value=round(percentage,1))
    
    st.markdown("<h2 style='text-align: center; color: black;'>TALENT RATING</h2>", unsafe_allow_html=True)
    
    cola, colb, colc= st.columns([0.65,0.01,0.34])
    with cola:
        df_use= df_re_pe[df_re_pe['YEARSATCOMPANY']==0]
        df_use= df_use.groupby('TYPE')['RATING'].mean().reset_index()
        
        categories = df_use['TYPE'].tolist()
        values = df_use['RATING'].tolist()

        fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself'
        ))

        fig.update_layout(autosize=False,width=400,height=400,title_text='6 MONTH',
        polar=dict(
            radialaxis=dict(
            visible=True,
            range=[0, 5]  
            )),
        showlegend=False
        )

        st.plotly_chart(fig)
    
    with colc:
        st.metric(label="", value="")
        st.metric(label="", value="")
        df_use= df_re_pe[df_re_pe['YEARSATCOMPANY']==1]
        df_use= df_use.groupby('TYPE')['RATING'].mean().reset_index()
        
        categories = df_use['TYPE'].tolist()
        values = df_use['RATING'].tolist()

        fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself'
        ))

        fig.update_layout(autosize=False,width=300,height=300,title_text='YEAR 1',
        polar=dict(
            radialaxis=dict(
            visible=True,
            range=[0, 5]  
            )),
        showlegend=False
        )

        st.plotly_chart(fig)
    
    
        
    col6, col7, col8= st.columns([0.45, 0.1, 0.45])
    with col6:
        
        df_use= df_re_pe[df_re_pe['YEARSATCOMPANY']==2]
        df_use= df_use.groupby('TYPE')['RATING'].mean().reset_index()
        
        categories = df_use['TYPE'].tolist()
        values = df_use['RATING'].tolist()

        fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself'
        ))

        fig.update_layout(autosize=False,width=300,height=300,title_text='YEAR 2',
        polar=dict(
            radialaxis=dict(
            visible=True,
            range=[0, 5]  
            )),
        showlegend=False
        )
        
        st.plotly_chart(fig)
    with col8:
        df_use= df_re_pe[df_re_pe['YEARSATCOMPANY']==5]
        df_use= df_use.groupby('TYPE')['RATING'].mean().reset_index()
        
        categories = df_use['TYPE'].tolist()
        values = df_use['RATING'].tolist()

        fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself'
        ))

        fig.update_layout(autosize=False,width=300,height=300,title_text='YEAR 5',
        polar=dict(
            radialaxis=dict(
            visible=True,
            range=[0, 5] 
            )),
        showlegend=False
        )
        
        st.plotly_chart(fig)



