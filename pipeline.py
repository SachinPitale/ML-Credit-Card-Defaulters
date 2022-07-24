import sys,os
from CreditCard.exception import CreditCardException
from CreditCard.logger import logging
from CreditCard.pipeline.pipeline import Pipeline
def main():
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()
    except Exception as e:
        raise Exception(e,sys) from e


if __name__=="__main__":
    main()