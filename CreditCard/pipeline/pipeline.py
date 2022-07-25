from tkinter import E
from CreditCard.exception import CreditCardException
import os,sys
from CreditCard.logger import logging
from CreditCard.component.data_ingestion import DataIngestion
from CreditCard.config.configuration import Configuration
from CreditCard.entity.artifcat_entity import DataIngestionArtifact,DataValidationArtifact
from CreditCard.entity.config_entity import DataIngestionConfig
from CreditCard.component.data_validation import Datavalidation

class Pipeline:
    
    def __init__(self,config:Configuration=Configuration()) -> None:
        try:
            self.config = config

        except Exception as e:
            raise CreditCardException(e,sys) from e
    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise CreditCardException(e,sys) from e
    
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact) -> DataValidationArtifact:
        try:
            data_validation = Datavalidation(data_validation_config=self.config.get_data_validation_config(),
                                              data_ingestion_artifact=data_ingestion_artifact)
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise CreditCardException(e,sys) from e

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            logging.info("started data valiadtion")
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            logging.info("completed data valiadtion")
        except Exception as e:
            raise CreditCardException(e,sys) from e