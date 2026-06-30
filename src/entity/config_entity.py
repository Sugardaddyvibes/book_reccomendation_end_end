from datetime import datetime
import os

from src.constant import *

ROOT_DIR = os.getcwd()


class TrainingPipelineConfig:

    def __init__(self):

        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.pipeline_name = PIPELINE_NAME

        self.artifact_dir = os.path.join(
            ARTIFACT_DIR,
            self.timestamp
        )

        self.model_dir = MODEL_DIR
class DataIngestionConfig:

    def __init__(self, training_pipeline_config):

        self.data_ingestion_dir = os.path.join(
            training_pipeline_config.artifact_dir,
            DATA_INGESTION_DIR
        )

        self.book_file_path = os.path.join(
            DATA_DIR,
            BOOK_FILE_NAME
        )

        self.rating_file_path = os.path.join(
            DATA_DIR,
            RATING_FILE_NAME
        )

        self.merged_file_path = os.path.join(
            self.data_ingestion_dir,
            MERGED_DATA_NAME
        )


class DataTransformationConfig:

    def __init__(self,
                 training_pipeline_config):

        self.data_transformation_dir = os.path.join(
            training_pipeline_config.artifact_dir,
            DATA_TRANSFORMATION_DIR
        )

        self.transformed_file_path = os.path.join(
            self.data_transformation_dir,
            TRANSFORMED_DATA_FILE_NAME
        )

        self.minimum_user_ratings = MINIMUM_USER_RATINGS

        self.minimum_book_ratings = MINIMUM_BOOK_RATINGS


class FeatureEngineeringConfig:

    def __init__(self, training_pipeline_config):

        self.feature_engineering_dir = os.path.join(
            training_pipeline_config.artifact_dir,
            FEATURE_ENGINEERING_DIR
        )

        self.user_item_matrix_path = os.path.join(
            self.feature_engineering_dir,
            USER_ITEM_MATRIX_FILE_NAME
        )

        self.book_mapping_path = os.path.join(
            self.feature_engineering_dir,
            BOOK_MAPPING_FILE_NAME
        )



class ModelTrainerConfig:

    def __init__(self, training_pipeline_config):

        self.model_trainer_dir = os.path.join(
            training_pipeline_config.artifact_dir,
            MODEL_TRAINER_DIR
        )

        self.similarity_matrix_path = os.path.join(
            self.model_trainer_dir,
            SIMILARITY_MATRIX_FILE_NAME
        )

        self.model_path = os.path.join(
            self.model_trainer_dir,
            MODEL_FILE_NAME
        )