# Extract
import pymysql
from os import environ
import time
from ETL.log import logger
import boto3
import pandas as pd
import io

class Extract():
    
    def get_data_from_bucket(self, filename):
        
        s3 = boto3.client('s3')
        key = f"{filename}"
        obj = s3.get_object(Bucket= "sainos-bucket", Key= key)
        initial_df = pd.read_csv(io.BytesIO(obj['Body'].read()))
        data_list = initial_df.values.tolist()
        print(f"imagine the csv of name {key} in the s3 has been deleted ¯\_(ツ)_/¯")
        # try:
        #     s3.delete_object(Bucket= "sainos-bucket", Key= key) # test this!
        #     print(f"file: {file} has been deleted my guy!")
        # except:
        #     print(f"file deletion failed lol")
        return data_list

