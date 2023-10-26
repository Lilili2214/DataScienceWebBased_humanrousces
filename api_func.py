from fastapi import FastAPI, UploadFile
import numpy as np
import pandas as pd
from pydantic import BaseModel
from make_pre import make_prediction, make_prediction_retention
from train_model import make_model_save, add_to_data
import json
from connecttion import predict_promotion, query, reoder, predict_retention
from employee import Employee
app = FastAPI()
with open('encoder_feature.json', 'r') as f:
    data = json.load(f)
df_off= query("promotion")
df_off = reoder(df_off)
d_department = data['department']
d_regions = data['region']
d_recruitment_channel = data['recruitment_channel']
d_education = data['education']
df_skill= query("skill_record")
df_ole=query("ole")
df_training_record= query('training_record')
# For the other dictionaries, you can create them as before
d_kpi= {"Yes":1,"No":0} 
d_award={"Yes":1,"No":0}
d_gender= {"Female":1,"Male":0}
class Item(BaseModel):
    data: list

@app.get("/detail/{id}")
def get_employee(id: int):
    data= df_skill[df_skill['EMPLOYEE_ID']==id]
    df_grouped = df_training_record.groupby('EMPLOYEE_ID').agg(training_count=('TRAININGID', 'count'),score_mean=('SCORE', 'mean')).reset_index()   
    data_ole=df_ole.groupby('EMPLOYEE_ID').agg(absent_days=('ABSEETISM_DAYS', 'sum'),ole_mean=('OLE', 'mean')).reset_index()   
    data_ole= data_ole[data_ole['EMPLOYEE_ID']==id]
    df_grouped= df_grouped[df_grouped['EMPLOYEE_ID']==id]
    data_re= data.merge(df_grouped, on='EMPLOYEE_ID')
    data_final= data_re.merge(data_ole, on='EMPLOYEE_ID')
    dict_= data_final.to_dict()
    return dict_


@app.get("/{gender}/{no_of_trainings}/{age}/{performance_rating}/{length_of_service}/{kpi_met}/{award}/{avg_training_score}/{recruitment}/{region}/{department}/{education}")
async def get_pred(gender: str, no_of_trainings: int, age: int, performance_rating: int, length_of_service: int, kpi_met: str, award: str, avg_training_score: int, recruitment: str, region: str, department: str, education: str):
    dataa= {'department': department,'region':region,'education': education,'gender':d_gender[gender],'recruitment_channel':recruitment,'no_of_trainings': no_of_trainings,'age': age,'previous_year_rating': performance_rating,'length_of_service': length_of_service,'KPIs_met >80%': d_kpi[kpi_met],'awards_won?': d_award[award],'avg_training_score': avg_training_score}
    X= predict_promotion(dataa)
    dict_out = make_prediction(X)
    return dict_out

@app.post("/predict")
async def predict(file: UploadFile):
    
    df = pd.read_csv(file.file)
    X= predict_promotion(df)
    
    dict_out = make_prediction(X)
    dict_out= dict_out.to_dict()

    return dict_out

@app.get("/predict_df/individual/{item}")
async def predict_df(item: int):
    df=df_off[df_off["employee_id"]==item]
    X= predict_promotion(df)
    dict_out = make_prediction(X)
    print(type(dict_out))
    return dict_out

@app.get("/predict_df/department/{item}")
async def predict_df(item: str):
    if item==-1:
        df = df_off.copy()
    else:
        df=df_off[df_off["department"]==item]
    X= predict_promotion(df)
    dict_out = make_prediction(X)
    if isinstance(dict_out, pd.DataFrame):
        dict_out= dict_out.to_dict()
    return dict_out

@app.post("/predict_re")
async def predict_re(item: Item):
    data = item.data
    data=pd.DataFrame(data)
    if len(data)==0:
        return "cannot find data"
    else:
        print(data)
        data = predict_retention(data)
        dict_= make_prediction_retention(data)
        print(dict_)
        dict_ = dict_.to_dict()
        print(dict_)
        return dict_
    
@app.get("/train_model")
def train_model():
    make_model_save()
    return {"Response": "Training completed."}

@app.get("/add/{gender}/{no_of_trainings}/{age}/{performance_rating}/{length_of_service}/{kpi_met}/{award}/{avg_training_score}/{recruitment}/{region}/{department}/{education}/{is_promoted}")
def add(gender: str, no_of_trainings: int, age: int, performance_rating: int, length_of_service: int, kpi_met: str, award: str, avg_training_score: int, recruitment: str, region: str, department: str, education: str,is_promoted:str):
    add_to_data(department, region, education,d_gender[gender], recruitment, no_of_trainings, age, performance_rating, length_of_service, d_kpi[kpi_met], d_award[award], avg_training_score, is_promoted)
    return {"Response": "New row has been added to training dataset!"}
