import os
import sys

import pandas as pd

from src.logger import logging
from src.exception import BookRecommendationException

from src.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig,FeatureEngineeringConfig, DataTransformationConfig,ModelTrainerConfig
from src.entity.artifact_entity import DataIngestionArtifact,DataTransformationArtifact,FeatureEngineeringArtifact,ModelTrainerArtifact
from  src.components.data_transformation import DataTransformation
from src.components.feature_engineering import FeatureEngineering
from src.components.model_trainer import ModelTrainer


print("Current Working Directory:", os.getcwd())


class DataIngestion:
    """
    Reads the raw datasets, merges them,
    saves the merged dataset into artifacts,
    and returns the DataIngestionArtifact.
    """

    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("=" * 60)
            logging.info("Data Ingestion Started")
            logging.info("=" * 60)

            # Create artifact directory
            os.makedirs(self.config.data_ingestion_dir, exist_ok=True)

            ###########################################
            # Read datasets
            ###########################################

            logging.info(f"Reading Books Dataset: {self.config.book_file_path}")

            books = pd.read_csv(self.config.book_file_path)

            logging.info(f"Books Loaded Successfully : {books.shape}")

            logging.info(f"Reading Ratings Dataset: {self.config.rating_file_path}")

            ratings = pd.read_csv(self.config.rating_file_path)

            logging.info(f"Ratings Loaded Successfully : {ratings.shape}")

            ###########################################
            # Keep Required Columns
            ###########################################

            books = books[
                [
                    "ISBN",
                    "book_id",
                    "Publication Year",
                    "Author",
                    "Title",
                    "AvgRating",
                    "Image-URL",
                    "Image-URL-S"
                ]
            ]

            ratings = ratings[
                [
                    "book_id",
                    "user_id",
                    "rating"
                ]

                ]

            ###########################################
            # Merge
            ###########################################

            logging.info("Merging Books and Ratings...")

            merged_df = ratings.merge(
                books,
                on="book_id",
                how="left"
            )

            logging.info(
                f"Merged Dataset Shape : {merged_df.shape}"
            )

            ###########################################
            # Save merged dataset
            ###########################################

            merged_df.to_csv(self.config.merged_file_path,index=False)

            logging.info(
                f"Merged dataset saved to : {self.config.merged_file_path}"
            )

            ###########################################
            # Create Artifact
            ###########################################

            artifact = DataIngestionArtifact(

                merged_file_path=self.config.merged_file_path,

                total_books=len(books),

                total_ratings=len(ratings),

                merged_records=len(merged_df),

                is_ingested=True,

                message="Data Ingestion Completed Successfully"

            )

            logging.info("Data Ingestion Completed Successfully")
            logging.info("=" * 60)

            return artifact

        except Exception as e:
            raise BookRecommendationException(e, sys)


if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation Completed")
        print(dataingestionartifact)
        logging.info("Starting Data Transformation")
        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)
        data_transformation = DataTransformation(dataingestionartifact,data_transformation_config)
        data_transformation_artifact = (data_transformation.initiate_data_transformation())
        print(data_transformation_artifact)
        logging.info("Starting Feature Engineering")
        feature_engineering_config = FeatureEngineeringConfig(trainingpipelineconfig)
        feature_engineering = FeatureEngineering(feature_engineering_config, data_transformation_artifact)
        feature_engineering_artifact = feature_engineering.initiate_feature_engineering()
        print(feature_engineering_artifact)
        logging.info("Starting Model Training")
        model_trainer_config = ModelTrainerConfig(trainingpipelineconfig)
        model_trainer = ModelTrainer(model_trainer_config, feature_engineering_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        print(model_trainer_artifact)
    except Exception as e:
        raise BookRecommendationException(e,sys)