import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
from pymongo import MongoClient
from dotenv import load_dotenv
import pymongo
from networksecurity.logging.logger import logging  
from networksecurity.exception.exception import NetworkSecurityException

load_dotenv()

uri = os.getenv("MONGO_DB_URI")
ca = certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(str(e), sys)
    
    def cv_to_json(self, file_path: str) -> dict:
        try:
            logging.info(f"Converting CSV file {file_path} to JSON format.")
            df = pd.read_csv(file_path)
            df.reset_index(drop=True, inplace=True)
            records = list(json.loads(df.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(str(e), sys)
        
    
    def insert_data_to_mongodb(self,records,db,collection):
        try:
            logging.info(f"Inserting data into MongoDB collection: {collection}")
            self.database = db
            self.collection = collection
            self.records = records
            self.client = pymongo.MongoClient(uri, tlsCAFile=ca)
            self.database = self.client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            logging.info("Data inserted successfully.")
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(str(e), sys)
        

if __name__ == "__main__":
    FILE_PATH = "phisingData.csv"
    if not os.path.isfile(FILE_PATH):
        logging.error(f"File not found: {FILE_PATH}")
        raise NetworkSecurityException(f"File not found: {FILE_PATH}", sys)
    db = "network_security_db"
    collection = "NetworkData"
    try:
        networkobj = NetworkDataExtract()
        networkobj.cv_to_json(file_path=FILE_PATH)
        records = networkobj.cv_to_json(file_path=FILE_PATH)
        inserted_count = networkobj.insert_data_to_mongodb(records=records, db=db, collection=collection)
        logging.info(f"Total records inserted: {inserted_count}")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise NetworkSecurityException(str(e), sys)