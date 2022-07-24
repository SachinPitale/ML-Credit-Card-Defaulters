from re import T
from CreditCard.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from CreditCard.constant import *
from CreditCard.exception import CreditCardException
import os, sys
from CreditCard.util.util import read_yaml_file
from CreditCard.logger import logging


class Configuration:
    def __init__(self,
        config_file_path:str = CONFIG_FILE_PATH,
        current_time_stamp:str = CURRENT_TIME_STAMP )->None:
        try:
            self.config_info=read_yaml_file(file_path=config_file_path)
            self.training_pipeline_config =  self.get_training_pipeline_config()
            self.time_stamp = current_time_stamp

        except Exception as e:
            raise CreditCardException(e,sys) from e

    def get_training_pipeline_config(self)->TrainingPipelineConfig:
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(ROOT_DIR,
                training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
                training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]
                )
            training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f"Training pipleine config: {training_pipeline_config}")
            return training_pipeline_config
        except Exception as e:
            raise CreditCardException(e,sys) from e
    
    def get_data_ingestion_config(self)-> DataIngestionConfig:
        try:
            # getting artifact directory
            artifact_dir = self.training_pipeline_config.artifact_dir

            #getting data ingestion directory inside artifact directory
            data_ingestion_artifact_dir=os.path.join(artifact_dir,
                DATA_INGESTION_ARTIFACT_DIR,
                self.time_stamp
                )
            # retrive all data ingestion info from config.yaml 
            data_ingestion_info = self.config_info[DATA_INGESTION_CONFIG_KEY]
            
            # get source data url
            dataset_download_url = data_ingestion_info[DATA_INGESTION_DOWNLOAD_URL_KEY]

            # destination location to download file
            tgz_download_dir = os.path.join(data_ingestion_artifact_dir,
                data_ingestion_info[DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY]
            )
            # main directory, when we keep our row data inside artifact
            raw_data_dir = os.path.join(data_ingestion_artifact_dir,
                data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY]
            )

            # directory inside we keep train and test data
            ingested_data_dir =  os.path.join(data_ingestion_artifact_dir,
            data_ingestion_info[DATA_INGESTION_INGESTED_DIR_NAME_KEY]
                )
            # directory for keep train data
            ingested_train_dir = os.path.join(ingested_data_dir,
            data_ingestion_info[DATA_INGESTION_TRAIN_DIR_KEY]
            )

            ingested_test_dir = os.path.join(ingested_data_dir,
            data_ingestion_info[DATA_INGESTION_TEST_DIR_KEY]
            )

            DataIngestionConfig(
            dataset_download_url=dataset_download_url,
            tgz_download_dir=tgz_download_dir,
            raw_data_dir=raw_data_dir,
            ingested_train_dir=ingested_train_dir,
            ingested_test_dir=ingested_test_dir)
        except Exception as e:
            raise CreditCardException(e,sys) from e