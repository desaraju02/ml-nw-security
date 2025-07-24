import pymongo
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.exception.exception import NetworkSecurityException
import os
import sys
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
import pandas as pd
import numpy as np
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split

load_dotenv()
logging.info("Data Ingestion component initialized")
MONGO_DB_URI = os.getenv("MONGO_DB_URI")
if not MONGO_DB_URI:
    raise NetworkSecurityException("MONGO_DB_URI not found in environment variables", sys)  
ca = certifi.where()

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            
        except Exception as e:
            raise NetworkSecurityException(str(e), sys)
    
    def export_collection_as_dataframe(self) -> pd.DataFrame:
        try:
           # logging.info(f"Exporting collection {collection_name} from database {database_name} to DataFrame.")
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.client = pymongo.MongoClient(MONGO_DB_URI, tlsCAFile=ca)
            collection = self.client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find({})))
            if '_id' in df.columns:
                df.drop(columns=['_id'], inplace=True)
            if df.empty:
                logging.warning(f"Collection {collection_name} is empty.")
            df.replace({'na': np.nan}, inplace=True)
            logging.info(f"Collection {collection_name} exported successfully.")
            return df
        except Exception as e:
            raise NetworkSecurityException(str(e), sys)
    
    def export_data_to_feature_store(self, df: pd.DataFrame):
        try:
            logging.info("Exporting data to feature store.")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            df.to_csv(feature_store_file_path, index=False, header=True)
            logging.info(f"Data exported to feature store at {feature_store_file_path}.")
            return df
        except Exception as e:
            raise NetworkSecurityException(str(e), sys)

    def split_data_as_train_test(self, df: pd.DataFrame):
        try:
            logging.info("Splitting data into train and test sets.")
            train_df, test_df = train_test_split(df, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42)
            logging.info(f"Train set size: {len(train_df)}, Test set size: {len(test_df)}")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            train_df.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_df.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            return train_df, test_df
        except Exception as e:
            raise NetworkSecurityException(str(e), sys)

    def initiate_data_ingestion(self):
        try:
            logging.info("Starting data ingestion process.")
            df = self.export_collection_as_dataframe()
            df = self.export_data_to_feature_store(df)
            self.split_data_as_train_test(df)
            dataingestionartifact = DataIngestionArtifact(

                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

            logging.info("Data ingestion process completed successfully.")
            return dataingestionartifact
            # Split the data into train and test sets
            train_df, test_df = train_test_split(df, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42)
            
            # Save the train and test data to CSV files
            train_df.to_csv(self.data_ingestion_config.train_file_path, index=False)
            test_df.to_csv(self.data_ingestion_config.test_file_path, index=False)
            
            logging.info(f"Data ingestion completed. Train file saved at {self.data_ingestion_config.train_file_path} and Test file saved at {self.data_ingestion_config.test_file_path}")
            
        except Exception as e:
            raise NetworkSecurityException(str(e), sys)

    