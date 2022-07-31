from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
from CreditCard.entity.creditcard_predictor import CreditCardData,CreditPredictor
from CreditCard.constant import CONFIG_DIR
import os
import pickle
import numpy as np

ROOT_DIR = os.getcwd()
LOG_FOLDER_NAME = "logs"
PIPELINE_FOLDER_NAME = "housing"
SAVED_MODELS_DIR_NAME = "model_artifacts"
MODEL_CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, "model.yaml")
LOG_DIR = os.path.join(ROOT_DIR, LOG_FOLDER_NAME)
PIPELINE_DIR = os.path.join(ROOT_DIR, PIPELINE_FOLDER_NAME)
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)
app=Flask(__name__)


@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict',methods=['POST','GET'])
def index():

    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            LIMIT_BAL=int(float(request.form['limit_bal']))
            is_sex= request.form['sex']
            if(is_sex=='male'):
                SEX=1
            else:
                SEX=2
            is_education= request.form['education']
            if(is_education=='BE'):
                EDUCATION=int(float(1))
            elif(is_education=='MTech'):
                EDUCATION=2
            elif(is_education=='PhD'):
                EDUCATION=3
            is_marrige= request.form['marriage']
            if(is_marrige=='single'):
                MARRIAGE=1
            else:
                MARRIAGE=2
            AGE = int(float(request.form['age']))
            PAY_0 = int(float(request.form['pay_0']))
            PAY_2 = int(float(request.form['pay_2']))
            PAY_3 = int(float(request.form['pay_3']))
            PAY_4 = int(float(request.form['pay_4']))
            PAY_5 = int(float(request.form['pay_5']))
            PAY_6 = int(float(request.form['pay_6']))

            BILL_AMT1 = int(float(request.form['bill_amt1']))
            BILL_AMT2 = int(float(request.form['bill_amt2']))
            BILL_AMT3 = int(float(request.form['bill_amt3']))
            BILL_AMT4 = int(float(request.form['bill_amt4']))
            BILL_AMT5 = int(float(request.form['bill_amt5']))
            BILL_AMT6 = int(float(request.form['bill_amt6']))

            PAY_AMT1 = int(float(request.form['pay_amt1']))
            PAY_AMT2 = int(float(request.form['pay_amt2']))
            PAY_AMT3 = int(float(request.form['pay_amt3']))
            PAY_AMT4 = int(float(request.form['pay_amt4']))
            PAY_AMT5 = int(float(request.form['pay_amt5']))
            PAY_AMT6 = int(float(request.form['pay_amt6']))

            CreditCard_Data = CreditCardData(LIMIT_BAL=LIMIT_BAL,
                                   SEX=SEX,
                                   EDUCATION=EDUCATION,
                                   MARRIAGE=MARRIAGE,
                                   AGE=AGE,
                                   PAY_0=PAY_0,
                                   PAY_2=PAY_2,
                                   PAY_3=PAY_3,
                                   PAY_4=PAY_4,
                                   PAY_5=PAY_5,
                                   PAY_6=PAY_6,
                                   BILL_AMT1=BILL_AMT1,
                                   BILL_AMT2=BILL_AMT2,
                                   BILL_AMT3=BILL_AMT3,
                                   BILL_AMT4=BILL_AMT4,
                                   BILL_AMT5=BILL_AMT5,
                                   BILL_AMT6=BILL_AMT6,
                                   PAY_AMT1=PAY_AMT1,
                                   PAY_AMT2=PAY_AMT2,
                                   PAY_AMT3=PAY_AMT3,
                                   PAY_AMT4=PAY_AMT4,
                                   PAY_AMT5=PAY_AMT5,
                                   PAY_AMT6=PAY_AMT6,
                                   )
            credit_df = CreditCard_Data.get_credit_input_data_frame()
            credit_predictor = CreditPredictor(model_dir=MODEL_DIR)
            default_payment_next_month = credit_predictor.predict(X=credit_df)
            default_payment_next_month=default_payment_next_month.astype(int)
            if default_payment_next_month == [0]:
                prediction = "No"
            elif default_payment_next_month == [1]:
                prediction = "Yes"
            print(prediction)
            return render_template('results.html',prediction=prediction)
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)




    