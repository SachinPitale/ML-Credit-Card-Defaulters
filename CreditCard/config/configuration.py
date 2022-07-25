from re import T
from CreditCard.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig
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
            #dataset_download_url = data_ingestion_info[DATA_INGESTION_DOWNLOAD_URL_KEY]

            dataset_file_path = os.path.join(ROOT_DIR,
                data_ingestion_info[DATA_INGESTION_DATA_DIR_KEY],
                data_ingestion_info[DATA_INGESTION_DATA_FILE_NAME_KEY]
                )

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

            data_ingestion_config= DataIngestionConfig(
            #dataset_download_url=dataset_download_url,
            dataset_file_path= dataset_file_path,
            tgz_download_dir=tgz_download_dir,
            raw_data_dir=raw_data_dir,
            ingested_train_dir=ingested_train_dir,
            ingested_test_dir=ingested_test_dir)
            logging.info(f"Data Ingestion config: {data_ingestion_config}")
            return data_ingestion_config
        except Exception as e:
            raise CreditCardException(e,sys) from e
    def get_data_validation_config(self) -> DataValidationConfig:
        try:
            # Get main artifact directory
            artifact_dir =  self.training_pipeline_config.artifact_dir

            # find path of validation directory inside artifact
            data_validation_artifact_dir=os.path.join(
                artifact_dir,
                DATA_VALIDATION_ARTIFACT_DIR_NAME,
                self.time_stamp
            )

            # Get data validation keys
            data_validation_config = self.config_info[DATA_VALIDATION_CONFIG_KEY]

            # Get schema file name
            schema_file_path = os.path.join(ROOT_DIR,
            data_validation_config[DATA_VALIDATION_SCHEMA_DIR_KEY],
            data_validation_config[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY]
            )

            # GET report file directory path
            report_file_path = os.path.join(data_validation_artifact_dir,
            data_validation_config[DATA_VALIDATION_REPORT_FILE_NAME_KEY]
            )
            # GET report file path
            report_page_file_path = os.path.join(data_validation_artifact_dir,
            data_validation_config[DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY]
            )

            data_validation_config = DataValidationConfig(
                schema_file_path=schema_file_path,
                report_file_path=report_file_path,
                report_page_file_path=report_page_file_path,
            )
            return data_validation_config

        except Exception as e:
            raise CreditCardException(e,sys) from e