import json
import boto3
import pandas as pd
from ETL.ETL import run_etl
import io
from decimal import Decimal

def import_drinks(event, context):
    filename = event['Records'][0]['s3']['object']['key']
    print("importing from filename: " + filename)

    data = get_data_from_bucket("sainos-bucket", filename)
    # Each row looks like this:
    # "2020-06-15 10:19:24.356839","Dungannon","Terry Keys"," Speciality Tea - Peppermint: 1.3, Large Flavoured latte - Vanilla: 2.85,  Smoothies - Berry Beautiful: 2.0, Regular Flavoured latte - Gingerbread: 2.55","8.70","CASH",""
    # print(f"first row: {data[0]}")
    objects = [convert_row_to_object(row) for row in data]

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('drinksTable')
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.batch_writer
    with table.batch_writer() as batch:
        for obj in objects:
            # print(f"creating record: {obj}")
            for item in create_records(obj):
                # https://www.reddit.com/r/aws/comments/6iv8cb/boto3_and_dynamo_put_item_python/
                # print(f"item: {item}")
                batch.put_item(Item=item)
    
    print("complete")

def create_records(obj):
    return [create_record(obj, basket_item, basket_index) 
            for basket_index, basket_item in enumerate(obj["basket"])]

def create_record(obj, basket_item, basket_index):
    return {
        "_id": create_partition_key(obj, basket_item),
        "_rng": create_range_key(obj, basket_item, basket_index),
        "date": obj["date"],
        "location": obj["location"],
        "customerName": obj["customerName"],
        "total": Decimal(str(obj["price"])),
        "paymentMethod": obj["paymentMethod"],
        "name": basket_item["name"],
        "price": Decimal(basket_item["price"]),
    }

def create_partition_key(obj, basket_item):
    return obj["location"]

def create_range_key(obj, basket_item, basket_index):
    return obj["date"] + "/" + basket_item["name"] + "/" + obj["location"] + "/" + str(basket_index)

# fe839b82-abd6-11ea-91b2-acde48001122, 2020-06-11, 11:30:41, 59, Susan, Rush, 690.00, Cash
def convert_row_to_object(row):
    # "2020-06-15 10:19:24.356839","Dungannon","Terry Keys","  Speciality Tea - Peppermint: 1.3, Large Flavoured latte - Vanilla: 2.85,  Smoothies - Berry Beautiful: 2.0, Regular Flavoured latte - Gingerbread: 2.55","8.70","CASH",""
    return {
        "date": row[0],
        "location": row[1],
        "customerName": row[2],
        "basket": get_basket(row[3]),
        "price": row[4],
        "paymentMethod": row[5]
    }

def get_basket(data):
    # "Speciality Tea - Peppermint: 1.3, Large Flavoured latte - Vanilla: 2.85,  Smoothies - Berry Beautiful: 2.0, Regular Flavoured latte - Gingerbread: 2.55
    return [get_drink(drink_data) for drink_data in data.split(', ')]

def get_drink(data):
    # Speciality Tea - Peppermint: 1.3
    parts = data.split(": ")
    return {
        "name": parts[0].strip(),
        "price": parts[1].strip(),
    }

def get_data_from_bucket(bucket, key):    
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key=key)
    initial_df = pd.read_csv(io.BytesIO(obj['Body'].read()))
    return initial_df.values.tolist()