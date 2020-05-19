import pymysql
from os import environ
import time
from extract import Extract
from transform import Transform

if __name__ == "__main__":
    start = time.time()
    app = Extract()
    app.load_data()
    end_extract = time.time()
    print(f"Extract time:")
    print(round(end_extract - start, 4))
    app = Transform()
    raw_data = app.get_raw_data()
    app.transform(raw_data)

    end_transform = time.time()
    print(f"Transform time:")
    print(round(end_transform - end_extract, 4))
    # insert load call
    end_load = time.time()
    print(f"Load time:")
    print(round(end_load - end_transform, 4))