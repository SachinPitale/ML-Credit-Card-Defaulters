from CreditCard.entity.config_entity import DataIngestionConfig
from CreditCard.exception import CreditCardException
import os, sys
from CreditCard.logger import logging
from CreditCard.entity.artifcat_entity import DataIngestionArtifact
import tarfile
from six.moves import urllib
import numpy as np
import pandas as pd
import shutil
from sklearn.model_selection import train_test_split

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'='*20} Data ingestion log started {'='*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CreditCardException(e,sys) from e
    
    def download_housing_data(self,) -> str:
        try:
            #extraction remote url to download dataset
            download_url = self.data_ingestion_config.dataset_download_url

            #folder location to download file
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir
            
            if os.path.exists(tgz_download_dir):
                os.remove(tgz_download_dir)

            os.makedirs(tgz_download_dir,exist_ok=True)

            housing_file_name = os.path.basename(download_url)

            tgz_file_path = os.path.join(tgz_download_dir, housing_file_name)

            logging.info(f"Downloading file from :[{download_url}] into :[{tgz_file_path}]")
            urllib.request.urlretrieve(download_url, tgz_file_path)
            logging.info(f"File :[{tgz_file_path}] has been downloaded successfully.")
            return tgz_file_path

        except Exception as e:
            raise CreditCardException(e,sys) from e
    #def extract_tgz_file(self,tgz_file_path:str):
    def extract_tgz_file(self):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir,exist_ok=True)

            # logging.info(f"Extracting tgz file: [{tgz_file_path}] into dir: [{raw_data_dir}]")
            # with tarfile.open(tgz_file_path) as housing_tgz_file_obj:
            #     housing_tgz_file_obj.extractall(path=raw_data_dir)
            # logging.info(f"Extraction completed")

            dataset_file_path = self.data_ingestion_config.dataset_file_path
            shutil.copy(dataset_file_path, raw_data_dir)


        except Exception as e:
            raise CreditCardException(e,sys) from e
    
    def split_data_as_train_test(self) -> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]

            credit_card_file_path = os.path.join(raw_data_dir,file_name)


            logging.info(f"Reading csv file: [{credit_card_file_path}]")
            credit_card_data_frame = pd.read_csv(credit_card_file_path)
            y=credit_card_data_frame['default payment next month']
            X=credit_card_data_frame.drop(columns=['default payment next month'])

    

            

            logging.info(f"Splitting data into train and test")
            train_set = None
            test_set = None

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            train_set = pd.concat([X_train, y_train], axis=1, join='inner')
            test_set = pd.concat([X_test, y_test], axis=1, join='inner')

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,
                                            file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,
                                        file_name)
            
            if train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting training datset to file: [{train_file_path}]")
                train_set.to_csv(train_file_path,index=False)

            if test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok= True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                test_set.to_csv(test_file_path,index=False)
            

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                test_file_path=test_file_path,
                                is_ingested=True,
                                message=f"Data ingestion completed successfully."
                                )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact

        except Exception as e:
            raise CreditCardException(e,sys) from e
    
    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            #tgz_file_path =  self.download_housing_data()
            #return self.extract_tgz_file(tgz_file_path=tgz_file_path)
            self.extract_tgz_file()
            return self.split_data_as_train_test()
        except Exception as e:
            raise CreditCardException(e,sys) from e
    
    def __del__(self):
        logging.info(f"{'='*20}Data Ingestion log completed.{'='*20} \n\n")

