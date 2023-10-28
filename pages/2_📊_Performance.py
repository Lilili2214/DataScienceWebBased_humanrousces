import streamlit as st
import snowflake.connector
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt


 
st.set_page_config(layout="wide" )

con = snowflake.connector.connect(
    user='lizz2214',
    password='Ly0923316675',
    account='ss98730.ap-southeast-2',
    warehouse='hr_management',
    database='hr_management',
    schema='dbt_nly'
)


cur = con.cursor()

cur.execute("SELECT * FROM OLE")

rows = cur.fetchall()
column_names = [desc[0] for desc in cur.description]
cur.execute("SELECT * FROM ABSEETISM")

rows1 = cur.fetchall()
column_names1 = [desc[0] for desc in cur.description]



cur.close()
con.close()


df_OLE = pd.DataFrame(rows, columns=column_names)
df_abs=  pd.DataFrame(rows1, columns=column_names1)

df_2023= df_abs[df_abs['YEAR_'] == 2023]


#---------------------------------------------
st.title("ABSENTEEISM")
with st.container():
    
    df_yearly = df_2023.groupby('EMPLOYEE_ID')['ABSEETISM_DAYS'].sum()
    average_absenteeism = df_yearly.mean()
    df_yearlyR = df_2023.groupby('EMPLOYEE_ID')['ABSEETISM_RATE'].sum()/12
    average_absenteeismR = df_yearlyR.mean()
    col1, col_gap,col2= st.columns([0.3, 0.1,0.6])
    with col1:
        st.info("Avg Yearly Absenteeism", icon =None)
        st.markdown(f"""
            <div style="text-align: center"> 
                <h1>{round(average_absenteeism,2)} Days</h1>
            </div>
        """, unsafe_allow_html=True)
        st.info("Avg Yearly Absenteeism Rate in % (Target <5%)", icon =None)

        average_absenteeismR*=100
        fig = go.Figure(go.Indicator(mode="gauge+number",value=average_absenteeismR,domain={'x': [0, 1], 'y': [0, 1]},gauge={'axis': {'range': [0, 100]},'steps': [{'range': [0, 1], 'color': "lightgray"},{'range': [1, 100], 'color': "gray"}],'threshold': {'line': {'color': "red", 'width': 4},'thickness': 0.75,'value': average_absenteeismR},'bar': {'color': "red"}},))
        fig.update_layout(autosize=False,width=400,height=400, margin=dict(l=50,r=50,  b=100,t=100,))  
    
        st.plotly_chart(fig)
        
        
    with col2:
        st.markdown(f"""
            <div style="text-align: center"> 
                <h3>Absenteeism Over The last 12 Months</h3>
            </div>
        """, unsafe_allow_html=True)
       
        month_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 
                    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

        df_2023['Month'] = df_2023['MONTH_'].map(month_dict)

        df_monthly = df_2023.groupby('Month')[['ABSEETISM_DAYS', 'ABSEETISM_RATE']].mean()
        df_monthly.reset_index(inplace=True)


        df_monthly.rename(columns={'index': 'Month'}, inplace=True)
        months_ordered = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        df_monthly['Month'] = pd.Categorical(df_monthly['Month'], categories=months_ordered, ordered=True)

        df_monthly.sort_values(by='Month', inplace=True)
        df_monthly['ABSEETISM_RATE']=df_monthly['ABSEETISM_RATE']*100
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_monthly['Month'], y=df_monthly['ABSEETISM_RATE'], fill='tozeroy', name='Absenteeism Rate'))
        fig.add_trace(go.Scatter(x=df_monthly['Month'], y=df_monthly['ABSEETISM_DAYS'], mode='lines', name='Absenteeism in Days',line=dict(color='red')))
        fig.update_yaxes(range=[0, max(df_monthly['ABSEETISM_RATE'].max(), df_monthly['ABSEETISM_RATE'].max())*1.5])
        for i, rate in enumerate(df_monthly['ABSEETISM_RATE']):
            fig.add_annotation(x=df_monthly['Month'][i], y=rate,text=f"{round(rate,2)}%",showarrow=False,font=dict(size=10))
            fig.update_layout( autosize=False, width=800,  height=500,  )

        st.plotly_chart(fig)

st.title("Overall Labor Effectiveness (OLE)")

col1, col_gap,col2= st.columns([0.45, 0.1,0.45])

with col1: 
    df_OLE['Month'] = df_OLE['MONTH_'].map(month_dict)

   
    df_monthly = df_OLE.groupby('Month')[['OLE']].mean()
    df_monthly.reset_index(inplace=True)


    df_monthly.rename(columns={'index': 'Month'}, inplace=True)
    months_ordered = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    df_monthly['Month'] = pd.Categorical(df_monthly['Month'], categories=months_ordered, ordered=True)

    df_monthly.sort_values(by='Month', inplace=True)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_monthly['Month'],
        y=df_monthly['OLE']*100,
        mode='lines',
        line=dict(color='red'),
    ))

   
    fig.update_layout(
        title='OLE Over The Past Year',
        xaxis_title='Month',
        yaxis_title='Percentage (%)',
        autosize=True, width=650,  height=500,
    )

   
    st.plotly_chart(fig)
with col2: 
    
    df_depart = df_OLE.groupby('DEPARTMENT')[['OLE']].mean()
    df_depart.reset_index(inplace=True)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_depart['DEPARTMENT'],
        y=df_depart['OLE'],
        text=[f'{val*100:.2f}%' for val in df_depart['OLE']],
        textposition='outside',
        marker_color='rgba(255, 0, 0, 0.4)'
    ))

    fig.update_layout(
        title='Bar Chart',
        xaxis_title='Department',
        yaxis_title='Percentage (%)',
        yaxis=dict(
            tickformat=',.0%',
        ),
        autosize=True, width=650,  height=500,
    )
    fig.update_yaxes(range=[0, max(df_depart['OLE'].max(), df_depart['OLE'].max())*1.5])
   
    st.plotly_chart(fig)   
st.write(df_2023)
st.write(df_OLE)    
            
       

        
        
