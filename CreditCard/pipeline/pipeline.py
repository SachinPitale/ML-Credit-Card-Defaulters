from tkinter import E
from CreditCard.exception import CreditCardException
import os,sys
from CreditCard.logger import logging
from CreditCard.component.data_ingestion import DataIngestion
from CreditCard.config.configuration import Configuration
from CreditCard.entity.artifcat_entity import DataIngestionArtifact
from CreditCard.entity.config_entity import DataIngestionConfig


class pipeline:
    
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

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
        except Exception as e:
            raise CreditCardException(e,sys) from e