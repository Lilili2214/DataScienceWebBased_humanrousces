import streamlit as st
import json
import pandas as pd
import plotly.express as px
import requests
from connecttion import reoder, query, search,predict_promotion,get_feature
from xgboost import XGBClassifier
import random
import plotly.graph_objects as go
from employee import Employee
import matplotlib.pyplot as plt
st.set_page_config(page_title="Prediction")
st.header("Prediction - Potential Employee for Promotion")
st.markdown("Using XGBoost, make predictions for which employees have potential to consider for promotion or praising them for their hard work")
st.sidebar.header("Make Prediction")
with open('encoder_feature.json', 'r') as f:
    data = json.load(f)
with open('./file.json', 'r') as f:
    data_img = json.load(f)
df_img = pd.DataFrame(list(data_img.items()), columns=['Index', 'Image_Path'])
df= query("promotion")
tab1, tab2, tab3, tab4 = st.tabs(["Try Prediction", "Search for Employee", "Recommend by Department","About the model"])
df_name= query("dim_employees")
df_name.columns = df_name.columns.str.lower()
df_name= df_name.drop("num", axis=1)
df_per= query("performance")
Predictors=['department', 'region', 'education','gender', 'no_of_trainings', 'age', 'previous_year_rating', 'length_of_service', 'KPIs_met >80%', 'awards_won?', 'avg_training_score', 'recruitment_channel_referred', 'recruitment_channel_sourcing']
df_kpi= query("employeekpi")   
df_work= query("workforce")


with tab1:
    if st.checkbox("Upload Your Dataset"):
        st.write("We prepare a file test.csv in folder. Please use it")
        uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
        if uploaded_file is not None:
           
            file_bytes = uploaded_file.getvalue()
            temp= pd.read_csv(uploaded_file)
            st.write(temp.shape)
            st.write(temp.dtypes)
            response = requests.post('http://localhost:8000/predict', files={'file': file_bytes})
            
            if st.button('Predict', key=1):
                if response.status_code == 200:
                    st.success("Request successful!")
                    data = response.json()

                    df_re = pd.DataFrame(data, columns=['Predicted Status'])
                    temp=get_feature(temp)
                    temp["status"]=df_re['Predicted Status'].values
                    show_result = temp[temp['status']==1]
                    show_result= show_result[[i for i in Predictors if i not in ['recruitment_channel_referred', 'recruitment_channel_sourcing']]]
                    st.write(show_result)
                else:
                    st.error("Request failed with status code {}".format(response.status_code))
    
                
        
    else:
        
        d_department = data['department']
        d_regions = data['region']
        d_recruitment_channel = data['recruitment_channel']

        d_education = data['education']


        d_kpi= {"Yes":1,"No":0} 
        d_award={"Yes":1,"No":0}
        d_gender= {"Female":1,"Male":0}
        region=st.selectbox("Region",tuple(d_regions.keys()))
        department=st.selectbox("Department",tuple(d_department.keys()))
        education=st.selectbox("Your highest Education",tuple(d_education.keys()))
        gender= st.radio("Gender",tuple(d_gender.keys()))
        performance_rating= st.selectbox("Performance Rating",['1','2','3','4','5'])
        kpi_met= st.radio("KPI met > 80%",tuple(d_kpi.keys()))
        award= st.radio("Award",tuple(d_award.keys()))
        recruitment= st.radio("Recruitment Channel",tuple(d_recruitment_channel.keys()))
        age= st.slider("Select Age",17,65)
        avg_training_score= st.slider("Average Training Score",0,100)
        no_of_trainings=  st.number_input(label="Number of trainings",step=1.,format="%.2f")
        length_of_service=  st.number_input(label="Lenght of Service",step=1.,format="%.2f")


    
        p1 = ["", "", "", "", "", "", "", "", "", "", ""]

        if st.button('Predict',key=2):
        
            response = requests.get(f'http://localhost:8000/{gender}/{no_of_trainings}/{age}/{performance_rating}/{length_of_service}/{kpi_met}/{award}/{avg_training_score}/{recruitment}/{region}/{department}/{education}')
            species_pred = response.json()
            if response.status_code == 200:
                st.success("Request successful!")
                if species_pred=="not_promo":
                        st.subheader(f"Predicted Status: This Employee needs more time to gain performance")
                else:
                    st.subheader(f"Predicted Status: Well performance! Recommend to consider!")
            else:
                st.error("Request failed with status code {}".format(response.status_code))
            
        if st.checkbox("Add to trainining dataset"):
            d_promo=data['promo']
            is_promoted= st.radio("Promo?",tuple(d_promo.keys()))
            is_promoted=d_promo[is_promoted]
            if st.button('Wanna add new row',key=3):
                response = requests.get(f'http://localhost:8000/add/{gender}/{no_of_trainings}/{age}/{performance_rating}/{length_of_service}/{kpi_met}/{award}/{avg_training_score}/{recruitment}/{region}/{department}/{education}/{is_promoted}')
                if response.status_code == 200:
                    st.success(response.json()["Response"])
                else:
                    st.error("Failed to get a response from the server.")


with tab2:
    loaded_model = XGBClassifier()
    loaded_model.load_model("main_model.model")
   
    st.header("Search by Name")
    filter_df= search(df_name)
    st.write(filter_df)
    for number,name in filter_df.iterrows():
        with st.expander(name['employeename'].upper()):
            performance= df_per[df_per["EMPLOYEE_ID"]==int(name['employeenumber'])]
            kpi= df_kpi[df_kpi["EMPLOYEENUMBER"]==int(name['employeenumber'])]
            st.subheader("Performance Rating from Manager")
            fig = px.bar(performance, x='TYPE', y='RATING')
            fig.update_layout(
            yaxis=dict(range=[0, 2*performance['RATING'].max()]),  
            )
            st.plotly_chart(fig)
            df_grouped = df_kpi.groupby('MONTH_')['KPI'].mean().reset_index()
            df_grouped = df_grouped.sort_values('MONTH_')
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_grouped['MONTH_'], y=df_grouped['KPI'], fill='tozeroy', name='Average KPI'))
            fig.update_layout(
            yaxis=dict(range=[0, 2*df_grouped['KPI'].max()]),  
            )
            fig.add_trace(go.Scatter(x=kpi['MONTH_'], y=kpi['KPI'], mode='lines', name='Employee KPI'))
            promo= df[df["EMPLOYEE_ID"]==(name['employeenumber'])]
            promo = reoder(promo)
            st.write(promo)
            gender=promo['gender'].apply(lambda x: 'Male' if x == 1 else 'Female')
            length_of_service=promo['length_of_service']
            performance_rating=promo['previous_year_rating']
            age=promo['age']
            item= int(name['employeenumber'])
            st.subheader("KPI in 2023 by Month compare with the average")
            st.plotly_chart(fig)
            if st.button('Predict', key=f'{item}'):
                response = requests.get(f'http://localhost:8000/predict_df/individual/{item}')
                species_pred = response.json()
                
                if response.status_code == 200:
                    st.success("Request successful!")
                    if species_pred['0']=="not_promoted":
                        st.subheader(f"Predicted Status: This Employee needs more time to gain performance")
                    else:
                        st.subheader(f"Predicted Status: Well performance! Recommend to consider!")
                else:
                    st.error("Request failed with status code {}".format(response.status_code))
                                

with tab3:
    st.header("Potential Employees")
    
    departments = df['DEPARTMENT'].unique()
    selected_department = st.selectbox('Select a department', departments)
    dataset = df[df['DEPARTMENT']==selected_department]
    dataset=reoder(dataset)
    dataset= get_feature(dataset)
    if st.button("Predict"):
        item= selected_department
        response = requests.get(f'http://localhost:8000/predict_df/department/{item}')
        data = response.json()
        if response.status_code == 200:
                st.success("Request successful!")
        else:
            st.error("Request failed with status code {}".format(response.status_code))
        df_re = pd.DataFrame(data, columns=['Predicted Status'])
        dataset['status']=df_re['Predicted Status'].values
        st.write(dataset)
        dataset=dataset[dataset['status']==1]
        

                    
        if len(dataset)==0:
            st.write("Cannot find any potential employee.")
        else:
            if len(dataset)>5:
                dataset = dataset.sort_values(by='avg_training_score', ascending=False).head(5)
            st.write(f"Find {len(dataset)} potential employees")
            num_images = len(dataset)


        
        for i,name in dataset.iterrows():
            with st.expander(str(name['employee_id'])):
                
                col1, col2 = st.columns([0.4, 0.6])
                with col1:
                    st.image(df_img.iloc[random.randint(0,len(df_img)-1)]['Image_Path'], width=200)
                with col2:
                    employee= df_work[df_work['EMPLOYEE_ID']==str(name['employee_id'])]
                    em= Employee(employee)
                    id=em.get_employee_id()

                    response = requests.get(f"http://localhost:8000/detail/{id}")
                    if response.status_code == 200:
                        st.success("Request successful!")
                    else:
                        st.error("Request failed with status code {}".format(response.status_code))
                    st.subheader(f'{em.get_name()}')
                    st.write("Postion:",em.get_job_role())
                    st.write("Age", em.get_age())
                    st.write("Education:",em.get_education())
                    data= response.json()
                    df_detail = pd.DataFrame(data)
                    
                    df_detail = df_detail.dropna(axis=1, how='all')
                    
                col1, col2, col0=st.columns([0.5,0.25,0.25])
                with col1:
                    
                    st.metric(label="OLE Yearly Average %", value=round(df_detail['ole_mean']*100))
                with col2:
                    st.metric(label="Number of Trainings", value=df_detail['training_count'])
                with col0:
                    st.metric(label="Previous Year Rating", value=name['previous_year_rating'])
                col3,col4,col5=st.columns([0.5,0.25,0.25])
                with col3:
                    st.metric(label="Salary Range", value=em.get_salary_range())
                    
                with col4:
                    st.metric(label="Average Training Score", value=round(df_detail['score_mean'],2))
                with col5:
                    
                    st.metric(label="Absenteeism in days", value=df_detail['absent_days'])
                st.write("Skills")
                st.write(df_detail[[i for i in df_detail.columns if i != 'EMPLOYEE_ID']])

with tab4:
    st.subheader("General Structure of Dataset")
    train= pd.read_csv("./train_data.csv")
    st.write(train)
    if st.button("Retrain Model"):
        response= requests.get(f"http://localhost:8000/train_model")
        if response.status_code == 200:
                        st.success("Request successful!")
        else:
            st.error("Request failed with status code {}".format(response.status_code))
    st.write("The bar charts you’re creating show the distribution of promoted and not promoted employees across different categories within each feature.")
    catcol=['department', 'region', 'education', 'gender', 'recruitment_channel',
        'no_of_trainings', 'previous_year_rating', 'length_of_service']

    for categoricalcol in catcol:
        crosstabresult=pd.crosstab(index=train[categoricalcol], columns=train['is_promoted'])
        fig, ax = plt.subplots()
        crosstabresult.plot.bar(color=['red','green'], ax=ax, title =categoricalcol+' Vs'+' is_promoted')
        st.pyplot(fig)
        

        classification_report = {
            '0': {'precision': 0.98, 'recall': 0.86, 'f1-score': 0.91, 'support': 15127},
            '1': {'precision': 0.87, 'recall': 0.98, 'f1-score': 0.92, 'support': 14957},
            'accuracy': 0.92,
            'macro avg': {'precision': 0.92, 'recall': 0.92, 'f1-score': 0.92, 'support': 30084},
            'weighted avg': {'precision': 0.92, 'recall': 0.92, 'f1-score': 0.92, 'support': 30084}
        }

        
        report_df = pd.DataFrame(classification_report).transpose()

      
    st.title('Model Evaluation')
    st.write('The table below presents the evaluation of the model performance. The metrics calculated are precision, recall and F1-score for each class (promoted and not promoted), as well as the overall accuracy of the model.')
    st.dataframe(report_df)
    st.write('From the table, we can see that the model performs well with an accuracy of over 90%. Both classes are well represented in the precision, recall and F1-score metrics.')

    


                       
        
