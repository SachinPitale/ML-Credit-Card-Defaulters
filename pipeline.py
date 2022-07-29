import sys,os
from CreditCard.exception import CreditCardException
from CreditCard.logger import logging
from CreditCard.pipeline.pipeline import Pipeline
from CreditCard.config.configuration import Configuration
def main():
    try:
        # pipeline = Pipeline()
        # pipeline.run_pipeline()
        data_validation_config = Configuration().get_model_trainer_config()
        print(data_validation_config)
    except Exception as e:
        raise Exception(e,sys) from e


if __name__=="__main__":
    main()