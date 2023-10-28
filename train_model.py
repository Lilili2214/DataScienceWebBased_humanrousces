import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from xgboost import XGBClassifier
import csv
import json
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import xgboost
import random
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle
def make_model_save():
    data = pd.read_csv("./train_data.csv")
    
    data= data.dropna()
    data = data.drop(["Unnamed: 0","employee_id"], axis=1)
    data_off= data.copy()

    label_encoder = LabelEncoder()

   
    region_map=data['region'].value_counts().to_dict()
    data_off['region']=data_off['region'].map(region_map)
    ordinal_labels=data_off.groupby(['department'])['is_promoted'].mean().sort_values().index
    ordinal_labels2={k:i for i, k in enumerate(ordinal_labels, 0)}
    data_off['department'] = data_off['department'].map(ordinal_labels2)
    print(data_off)
    data_off['education']=data_off['education'].replace({"Doctor":5,"Master":4,"Bachelor":3,"College":2,'Below College':1})
    data_off= pd.get_dummies(data_off, drop_first=True)
   
    print(data_off)

    
    
    dict_encoder = {"1": "is_promo", "0": "not_promo"}
    with open("encoder.json", "w") as write_file:
        json.dump(dict_encoder, write_file, indent=4)
    targetvariable='is_promoted'
    predictors = [i for i in data_off.columns if i not in targetvariable]
    print(predictors)
    X=data_off[predictors].values 
    y=data_off[targetvariable].values
    
    PredictorScaler=MinMaxScaler()

    
    PredictorScalerFit=PredictorScaler.fit(X)


    X=PredictorScalerFit.transform(X)
    
    classifier=xgboost.XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
       colsample_bytree=0.7, gamma=0.3, learning_rate=0.1,
       max_delta_step=0, max_depth=10, min_child_weight=5, missing=np.nan,
       n_estimators=200, n_jobs=1, nthread=None,
       objective='binary:logistic', random_state=0, reg_alpha=0,
       reg_lambda=1, scale_pos_weight=1, seed=None, silent=True,
       subsample=1)


    FinalXGBModel=classifier.fit(X,y)

    FinalXGBModel.save_model("main_model.model")
    print(X)
   
    

def add_to_data(department, region, education, gender, recruitment_channel, no_of_trainings, age, previous_year_rating, length_of_service, KPIs_met, awards_won, avg_training_score, is_promoted):
    new_row = [random.randint(0,1000), department, region, education, gender, recruitment_channel, int(no_of_trainings), int(age), float(previous_year_rating), int(length_of_service), KPIs_met, awards_won, int(avg_training_score), is_promoted]

    with open("./train_data.csv", "a", newline='') as csv_file:
        writer_object = csv.writer(csv_file)
        writer_object.writerow(new_row)
    

def add_to_data(dataset):
    with open("./train_data.csv", "a", newline='') as csv_file:
        writer_object = csv.writer(csv_file)
        for data in dataset:
            department, region, education, gender, recruitment_channel, no_of_trainings, age, previous_year_rating, length_of_service, KPIs_met, awards_won, avg_training_score, is_promoted = data
            new_row = [random.randint(0,1000), department, region, education, gender, recruitment_channel, int(no_of_trainings), int(age), float(previous_year_rating), int(length_of_service), KPIs_met, awards_won, int(avg_training_score), is_promoted]
            writer_object.writerow(new_row)




    

def make_model_retention():
    employee_dff = pd.read_csv("./employee_data.csv")
    employee_dff['Attrition'] = employee_df['Attrition'].apply(lambda x: 1 if x == 'Yes' else 0)
    employee_dff['OverTime'] = employee_df['OverTime'].apply(lambda x: 1 if x == 'Yes' else 0)
    employee_dff['Over18'] = employee_df['Over18'].apply(lambda x: 1 if x == 'Y' else 0)
    employee_df=employee_dff.drop(['EmployeeCount', 'StandardHours', 'Over18', 'EmployeeNumber'], axis=1)
    
    
    X_cat = employee_df[['BusinessTravel', 'Department', 'EducationField', 'Gender', 'JobRole', 'MaritalStatus']]
    onehotencoder = OneHotEncoder()
    X_cat = onehotencoder.fit_transform(X_cat).toarray() 
    X_cat = pd.DataFrame(X_cat)
   
    
    X_numerical = employee_df[['Age', 'DailyRate', 'DistanceFromHome', 'Education', 'EnvironmentSatisfaction', 'HourlyRate', 'JobInvolvement', 'JobLevel', 'JobSatisfaction', 'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked', 'OverTime', 'PercentSalaryHike', 'PerformanceRating', 'RelationshipSatisfaction', 'StockOptionLevel', 'TotalWorkingYears', 'TrainingTimesLastYear', 'WorkLifeBalance', 'YearsAtCompany','YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager']]

    X_all = pd.concat([X_cat, X_numerical], axis=1)
    scaler = MinMaxScaler()
    X_all.columns = X_all.columns.astype(str)
    print(X_all.columns)
    X = scaler.fit_transform(X_all)
    y = employee_df['Attrition']
    X_y= pd.concat([X,y], axis =1)
    X_y.to_csv("X_y.csv")
    model = LogisticRegression()
    model= model.fit(X, y)
    
    with open('FinalLRModel1.pkl', 'wb') as fileWriteStream:
        pickle.dump(model, fileWriteStream)
       
        fileWriteStream.close()


def get_feature_retention():
    employee_dff = pd.read_csv("./employee_data.csv")
    employee_dff['OverTime'] = employee_dff['OverTime'].apply(lambda x: 1 if x == 'Yes' else 0)
    employee_dff['Over18'] = employee_dff['Over18'].apply(lambda x: 1 if x == 'Y' else 0)
    employee_df=employee_dff.drop(['EmployeeCount', 'StandardHours', 'Over18', 'EmployeeNumber'], axis=1)
    
    
    X_cat = employee_df[['BusinessTravel', 'Department', 'EducationField', 'Gender', 'JobRole', 'MaritalStatus']]
    onehotencoder = OneHotEncoder()
    X_cat = onehotencoder.fit_transform(X_cat).toarray() 
    X_cat = pd.DataFrame(X_cat)
   
    
    X_numerical = employee_df[['Age', 'DailyRate', 'DistanceFromHome', 'Education', 'EnvironmentSatisfaction', 'HourlyRate', 'JobInvolvement', 'JobLevel', 'JobSatisfaction', 'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked', 'OverTime', 'PercentSalaryHike', 'PerformanceRating', 'RelationshipSatisfaction', 'StockOptionLevel', 'TotalWorkingYears', 'TrainingTimesLastYear', 'WorkLifeBalance', 'YearsAtCompany','YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager']]

    X_all = pd.concat([X_cat, X_numerical], axis=1)
    scaler = MinMaxScaler()
    X_all.columns = X_all.columns.astype(str)
    print(X_all.columns)
    X = scaler.fit_transform(X_all)
    return X