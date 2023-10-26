import snowflake.connector
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import streamlit as st
from sklearn.preprocessing import OneHotEncoder
import numpy as np
def query(table):
    con = snowflake.connector.connect(
    user='lizz2214',
    password='Ly0923316675',
    account='ss98730.ap-southeast-2',
    warehouse='hr_management',
    database='hr_management',
    schema='dbt_nly'
)
    table = table.upper()
    # Create a cursor object
    cur = con.cursor()

    query = f"SELECT * FROM {table}"
    cur.execute(query)

    # Fetch all rows from the result of the query
    rows = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    # Close the cursor and connection
    cur.close()
    con.close()

    # Convert the data into a pandas DataFrame with column headers
    df = pd.DataFrame(rows, columns=column_names)
    
    return df



def categorize_age(age):
    if age<=25:
        return '<26'
    elif 26 <= age < 35:
        return '26-35'
    elif 35 <= age < 45:
        return '35-45'
    elif 45 <= age < 55:
        return '45-55'
    else:
        return '>55' 
def categorize_salary(salary):
    salary=salary*12
    if salary < 40000:
        return '<$40000'
    elif 40000 <= salary < 60000:
        return '$40000-$59999'
    elif 60000 <= salary < 80000:
        return '$60000-$79999'
    elif 80000 <= salary < 100000:
        return '$80000-$99999'
    elif 100000 <= salary < 120000:
        return '$100000-$119999'
    elif 120000 <= salary < 140000:
        return '$120000-$139999'
    elif 140000 <= salary < 160000:
        return '$140000-$159999'
    elif 160000 <= salary < 180000:
        return '$160000-$179999'
    elif 180000 <= salary < 200000:
        return '$180000-$199999'
    else:
        return '>=$200000'
    
def filter_by_salary(df, salary_range):
    return df[df['salary_category'] == salary_range]
def reoder(df):
    df= df.dropna()
    df = df.rename(columns={
    'EMPLOYEE_ID': 'employee_id',
    'DEPARTMENT': 'department',
    'AGE': 'age',
    'REGION': 'region',
    'GENDER_': 'gender',
    'RECRUITMENT_CHANNEL': 'recruitment_channel',
    'EDUCATION': 'education',
    'AWARDS_WON': 'awards_won?',
    'KPI_MET': 'KPIs_met >80%',
    'LENGTH_OF_SERVICE': 'length_of_service',
    'NO_OF_TRAINING': 'no_of_trainings',
    'AVG_TRAINNING_SCORE': 'avg_training_score',
    'PERFORMANCE_RATING': 'previous_year_rating'
    })
    # Assuming df is your DataFrame
    df['employee_id'] = df['employee_id'].astype('int64')
    df['no_of_trainings'] = df['no_of_trainings'].astype('float64')
    df['previous_year_rating'] = df['previous_year_rating'].astype('float64')
    df['avg_training_score'] = df['avg_training_score'].astype('float64')
    df['awards_won?'] = df['awards_won?'].astype('int64')

    # Assuming 'df' is your DataFrame
    column_order = ['employee_id','department', 'region', 'education', 'gender', 'recruitment_channel', 'no_of_trainings', 'age', 'previous_year_rating', 'length_of_service', 'KPIs_met >80%', 'awards_won?', 'avg_training_score']
    # Assuming 'df' is your DataFrame
    df = df[column_order]
    
    return df

def predict_promotion(test):
    x= get_feature(test)
    print(x)
    Predictors=['department', 'region', 'education','gender', 'no_of_trainings', 'age', 'previous_year_rating', 'length_of_service', 'KPIs_met >80%', 'awards_won?', 'avg_training_score', 'recruitment_channel_referred', 'recruitment_channel_sourcing']
    X=x[Predictors].values
    PredictorScaler=MinMaxScaler()
    PredictorScalerFit=PredictorScaler.fit(X)
    X=PredictorScalerFit.transform(X)
    return X

def predict_retention(employee_df):
    
    employee_df['OVERTIME'] = employee_df['OVERTIME'].apply(lambda x: 1 if x == 'Yes' else 0)
    employee_df['OVER18'] = employee_df['OVER18'].apply(lambda x: 1 if x == 'Y' else 0)
    employee_df=employee_df.drop([ 'STANDARDHOURS', 'OVER18', 'EMPLOYEENUMBER'], axis=1)
    print(employee_df)
    
    X_cat = employee_df[["BUSINESSTRAVEL", "DEPARTMENT", "EDUCATIONFIELD", "GENDER", "JOBROLE", "MARITALSTATUS"]]
    print(X_cat)
    onehotencoder = OneHotEncoder()
    X_cat = onehotencoder.fit_transform(X_cat).toarray()  # Convert sparse matrix to numpy array
    X_cat = pd.DataFrame(X_cat)
    # Get feature names from onehotencoder and convert them to a list
    
    X_numerical = employee_df[["AGE", "DAILYRATE", "DISTANCEFROMHOME", "EDUCATION", "ENVIRONMENTSATISFACTION", "HOURLYRATE", "JOBINVOLVEMENT", "JOBLEVEL", "JOBSATISFACTION", "MONTHLYINCOME", "MONTHLYRATE", "NUMCOMPANIESWORKED", "OVERTIME", "PERCENTSALARYHIKE", "PERFORMANCERATING", "RELATIONSHIPSATISFACTION", "STOCKOPTIONLEVEL", "TOTALWORKINGYEARS", "TRAININGTIMESLASTYEAR", "WORKLIFEBALANCE", "YEARSATCOMPANY","YEARSINCURRENTROLE", "YEARSSINCELASTPROMOTION", "YEARSWITHCURRMANAGER"]]
    print(X_cat)
    X_all = pd.concat([X_cat, X_numerical], axis=1)
    print(X_all.columns)
    scaler = MinMaxScaler()
    X_all.columns = X_all.columns.astype(str)
    
    X = scaler.fit_transform(X_all)
    print(X)
    
    return X


def get_feature(test):
    if isinstance(test,dict):
        test = pd.DataFrame(test, index=[0])
    ordinal_labels=['Legal', 'HR', 'Sales & Marketing', 'R&D', 'Finance', 'Operations',
       'Analytics', 'Procurement', 'Technology']
    # One-hot encode 'gender' and 'recruitment_channel' columns
    ordinal_labels2={k:i for i,k in enumerate(ordinal_labels,0)}
    
    test['department']=test['department'].map(ordinal_labels2)
    #Count Or Frequency Encoding for region
    region_map=test['region'].value_counts().to_dict()
    test['region']=test['region'].map(region_map)
    #Education Encoding
    test['education']=test['education'].replace({"Doctor":5,"Master":4,"Bachelor":3,"College":2,'Below College':1})
    #Avoidng Dumy Trap for applying Drop First
    if len(test) == 1: 
        # Check if 'recruitment_channel' is 'sourcing'
        if test['recruitment_channel'].iloc[0] == 'sourcing':
            test['recruitment_channel_referred'] = 0
            test['recruitment_channel_sourcing'] = 1
        # Check if 'recruitment_channel' is 'referred'
        elif test['recruitment_channel'].iloc[0] == 'referred':
            test['recruitment_channel_referred'] = 1
            test['recruitment_channel_sourcing'] = 0
        # If 'recruitment_channel' is neither 'sourcing' nor 'referred'
        else:
            test['recruitment_channel_referred'] = 0
            test['recruitment_channel_sourcing'] = 0
    else: 
        test = pd.get_dummies(test, columns=['recruitment_channel'], drop_first=True)
    # Ensure all necessary columns exist in the DataFrame
    return test
    
    


def search(df_name):
    selected_names= st.multiselect("Select employess", df_name['employeename'].unique())
    filter_df= df_name[df_name['employeename'].isin(selected_names)]
    return filter_df