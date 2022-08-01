# Defaults the credit card payment

## Problem Statement
To build a classification methodology to determine whether a person defaults the credit card payment for the next month.

### Features
-  LIMIT_BAL: continuous.Credit Limit of the person
-  SEX:  1 = male; 2 = female
-  EDUCATION: 1 = BE; 2 = MTech 3 = Phd
-  MARRIAGE: 1 = single; 2 = married; 
-  AGE: person ages
- PAY_0 to PAY_6: History of past payment. We tracked the past monthly payment records (from April to September, 2005)
- BILL_AMT1 to BILL_AMT6: Amount of bill statements.
- PAY_AMT1 to PAY_AMT6: Amount of previous payments.

### Target Label
- default payment = Yes = 1, No = 0.

### Traning Pipeline
![image](images\model_train_arch.PNG)

### Stages
#### Data Ingestion 
- Download data from source location and save it to raw directory.
- split data into train and test dataset. 

#### Data Valiatiton
- Validate raw data set file exist or not
- Validate all the column names.
- validate missing values in whole column
- Validate total number of columns

#### Data Transformation
- type cast all the feature column as per shema file
- apply onehot encording for nan values.
- apply StandardScaler to data set.
- save all the ndarray data in  npz file format.
- Create pickle module of data transformation for feature predication dataset to perform transformation.

#### Model Tranining
- train the model with differents ml algorithm and find out best model out of all train models.

#### Model Evaluation
- evaluate the latest train model accuracy with already deployed model.

#### Model Push
- Push model to artifact repository


## Model Deployment link.
[Model Access URL](https://ml-classification-model.herokuapp.com/)

### predication
![image](images\predication.PNG)
### Result
![image](images\predication_result.PNG)













  
  