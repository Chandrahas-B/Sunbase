import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
import lightgbm as lgbm
import tensorflow as tf
import joblib


class ChurnPredictor:
    
    def __init__(self):
        self.df = None
        df = pd.read_excel('data/customer_churn_large_dataset.xlsx')
        self.columns = df.columns
    
    def create_df(self, age, gender, location, subscription, 
                monthlyBill, totalGB):
        df = pd.DataFrame(
            data = [[age, gender, location, subscription, monthlyBill, totalGB, 0.0]],
            columns= self.columns[2:])
        self.df = df

    def transformation(self):
        transformer = joblib.load('./models/column_transformer.pkl')
        self.df = pd.DataFrame(data = transformer.transform(self.df))
        self.df = self.df.iloc[:,:-1]
    
    def ensemble(self):
        predictions = []
        pkl_models = ['RandomForest.pkl', 'lightGBM.pkl']
        model_path = './models/'
        for model_name in pkl_models:
            model = joblib.load(model_path+ model_name)
            prediction = model.predict(self.df)
            predictions.append(prediction[0])
        
        # nn_models = ['nn.h5']
        # for model_name in nn_models:
        #     model = tf.keras.models.load_model(model_path+ model_name)
        #     prediction = model.predict([self.df], verbose = 0)
        #     predictions.append(prediction[0])
        
        ensemble_prediction = sum(predictions)/len(predictions)
        final_prediction = 1 if ensemble_prediction >= 0.5 else 0
        return final_prediction