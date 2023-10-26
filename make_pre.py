import json
from xgboost import XGBClassifier
import pickle
import pandas as pd
from sklearn.linear_model import LogisticRegression



def make_prediction(x):
    loaded_model = XGBClassifier()
    loaded_model.load_model("main_model.model")
    predictions_out = loaded_model.predict(x)
    print(predictions_out)
    if (len(predictions_out)!=1):
        PredictedStatus=pd.DataFrame(predictions_out, columns=['Predicted Status'])
        print(PredictedStatus)
        print("ok")
        return PredictedStatus
    else:
        predictions_out[0]=predictions_out[0].astype(str)
        dict_={}
        if predictions_out[0]==1:
            dict_["1"]='is_promoted'
        elif predictions_out[0]==0:
            dict_["0"]="not_promoted"
        print(dict_)
        return dict_


def make_prediction_retention(x):
    try:
        with open('FinalLRModel1.pkl', 'rb') as fileReadStream:
            LR_model = pickle.load(fileReadStream)
    except FileNotFoundError:
        print("Could not find 'FinalLRModel1.pkl'.")
        return
    except Exception as e:
        print(f"An error occurred while loading the model: {e}")
        return

    try:
        predictions_out = LR_model.predict(x)
        probabilities = LR_model.predict_proba(x)
    except Exception as e:
        print(f"An error occurred while making predictions: {e}")
        return

    if len(predictions_out) != 1:
        PredictedStatus = pd.DataFrame(predictions_out, columns=['Predicted Status'])
        probabilities=pd.DataFrame(probabilities)
        df_return = pd.concat([PredictedStatus,probabilities], axis=1)
        print(df_return)
        return df_return
    else:
        data = {"Yes":1,"No":0}
        
        return data[str(int(predictions_out[0]))]