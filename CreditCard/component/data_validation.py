from CreditCard.entity.config_entity import DataIngestionConfig,DataValidationConfig
from CreditCard.entity.artifcat_entity import DataValidationArtifact,DataIngestionArtifact
from CreditCard.logger import logging
from CreditCard.exception import CreditCardException
import sys, os
import pandas as pd
import numpy as np
import json
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab


class Datavalidation:
    def __init__(self, data_validation_config:DataValidationConfig,
        data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info("started data test set")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            logging.info("end data test set")
        except Exception as e:
            raise CreditCardException(e,sys) from e
    



    def is_train_test_file_exists(self)->bool:
        try:
            logging.info("Checking if training and test file is available")
            is_train_file_exist = False
            is_test_file_exist = False


            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            is_train_file_exist = os.path.exists(train_file_path)
            is_test_file_exist = os.path.exists(test_file_path)

            is_available = is_train_file_exist and is_test_file_exist

            if not is_available:
                training_file = self.data_ingestion_artifact.train_file_path
                testing_file = self.data_ingestion_artifact.test_file_path
                message=f"Training file: {training_file} or Testing file: {testing_file}" \
                    "is not present"
                raise Exception(message)
            
            logging.info(f"Is train and test file exists?-> {is_available}")
            return is_available
        except Exception as e:
            raise CreditCardException(e,sys) from e
    def is_schema_file_exists(self) -> bool:
        try:
            """
                          Method Name: is_schema_file_exists
                          Description: This function validates the schema file exist or not
                          On Failure: Exception
            """
            is_schema_file = False
            schema_file_path=self.data_validation_config.schema_file_path
            is_schema_file = os.path.exists(schema_file_path)
            is_exist = is_schema_file

            if not is_exist:
                schema_file_path=self.data_validation_config.schema_file_path
                message=f"Schema file: {schema_file_path}" \
                    "is not present"
                raise Exception(message)
            return is_schema_file

        except Exception as e:
            raise CreditCardException(e,sys) from e


    def validate_column_length(self) -> bool:
        try:
            """
                          Method Name: validate_column_length
                          Description: This function validates the number of columns in the csv files.
                                       It is should be same as given in the schema file.
                          Output: None
                          On Failure: Exception
            """
            schema_file_path=self.data_validation_config.schema_file_path
            Number_of_Columns=self.data_validation_config.number_of_Columns
            train_df,test_df =  self.get_train_and_test_df()
            if train_df.shape[1] != Number_of_Columns:                
                message=f"train csv : {train_df}" \
                    "doesn't have all the columns"
                raise Exception(message)
            
            if test_df.shape[1] != Number_of_Columns:                
                message=f"test csv : {test_df}" \
                    "doesn't have all the columns"
                raise Exception(message)


        except Exception as e:
            raise CreditCardException(e,sys) from e
    
    def validateMissingValuesInWholeColumn(self):
        try:
            """
            Method Name: validateMissingValuesInWholeColumn
            Description: This function validates if any column in the csv file has all values missing.
            
            """
            train_df,test_df =  self.get_train_and_test_df()
            for columns in train_df:
                if (len(train_df[columns]) - train_df[columns].count()) == len(train_df[columns]):
                    message=f"Invalid Column for the file!! : {columns}"
                    raise Exception(message)
            

            for columns in test_df:
                if (len(test_df[columns]) - test_df[columns].count()) == len(test_df[columns]):
                    message=f"Invalid Column for the file!! : {columns}"
                    raise Exception(message) 
        except Exception as e:
            raise CreditCardException(e,sys) from e
    def validate_columns_names(self):
        try:
            Columns_Names=self.data_validation_config.ColNames
            logging.info(f"all columns names are {Columns_Names}")
            train_df,test_df =  self.get_train_and_test_df()
            for colName in Columns_Names:
                if colName not in train_df.columns:
                    message=f"Column Column doesn't find in file!! : {colName}"
                    logging.ERROR(message)
                    raise Exception(message)

                if colName not in test_df.columns:
                    message=f"Column Column doesn't find in file!! : {colName}"
                    logging.ERROR(message)
                    raise Exception(message) 
        except Exception as e:
            raise CreditCardException(e,sys) from e

    def validate_dataset_schema(self)->bool:
        try:
            validation_status = False
            #1. Number of Column
            #2. Check column names

            validation_status = True
            return validation_status 
        except Exception as e:
            raise CreditCardException(e,sys) from e
    
    def get_train_and_test_df(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df,test_df
        except Exception as e:
            raise CreditCardException(e,sys) from e

    def get_and_save_data_drift_report(self):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])
            train_df,test_df =  self.get_train_and_test_df()
            
            # It will calculate stats between train and test dataset
            profile.calculate(train_df,test_df)
            # it will save output to json file
            report = json.loads(profile.json())

            report_file_path = self.data_validation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            with open(report_file_path,"w") as report_file:
                json.dump(report,report_file,indent=6)
            
            return report

        except Exception as e:
            raise CreditCardException(e,sys) from e
    
    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df,test_df = self.get_train_and_test_df()
            dashboard.calculate(train_df,test_df)
            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir,exist_ok=True)

            dashboard.save(report_page_file_path)

        except Exception as e:
            raise CreditCardException(e,sys) from e
    
    def is_data_drift_found(self)-> bool:
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True
        except Exception as e:
            raise CreditCardException(e,sys) from e
    

    def initiate_data_validation(self)-> DataValidationArtifact:
        try:

            self.is_train_test_file_exists()
            self.is_schema_file_exists()
            self.validate_column_length()
            self.validate_columns_names()
            self.validateMissingValuesInWholeColumn()
            self.validate_dataset_schema()
            self.is_data_drift_found()

            data_validation_artifact = DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                report_file_path=self.data_validation_config.report_file_path,
                report_page_file_path=self.data_validation_config.report_page_file_path,
                is_validated=True,
                message="Data Validation performed successully."
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise CreditCardException(e,sys) from e


    def __del__(self):
        logging.info(f"{'='*20}Data Valdaition log completed.{'='*20} \n\n")

        

        
