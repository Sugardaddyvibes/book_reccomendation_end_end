import os
import sys
import pickle

from src.exception import BookRecommendationException
from src.logger import logging


def save_object(file_path, obj):

    try:

        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file:

            pickle.dump(obj, file)

        logging.info(f"Object saved at: {file_path}")

    except Exception as e:

        raise BookRecommendationException(e, sys)


def load_object(file_path):

    try:

        with open(file_path, "rb") as file:

            obj = pickle.load(file)

        logging.info(f"Object loaded from: {file_path}")

        return obj

    except Exception as e:

        raise BookRecommendationException(e, sys)


def get_latest_artifact_paths(base_artifacts_dir: str):

    try:

        logging.info("Scanning artifact directory for latest pipeline run...")

        # Get only folders
        folders = [
            folder
            for folder in os.listdir(base_artifacts_dir)
            if os.path.isdir(os.path.join(base_artifacts_dir, folder))
        ]

        if len(folders) == 0:
            raise Exception("No artifact folders found.")

        # Latest timestamp folder
        latest_folder = sorted(folders)[-1]

        latest_folder_path = os.path.join(
            base_artifacts_dir,
            latest_folder
        )

        logging.info(f"Latest Artifact Folder : {latest_folder_path}")

        ####################################################
        # Build Folder Paths
        ####################################################

        ingestion_dir = os.path.join(
            latest_folder_path,
            "data_ingestion"
        )

        transformation_dir = os.path.join(
            latest_folder_path,
            "data_transformation"
        )

        feature_engineering_dir = os.path.join(
            latest_folder_path,
            "feature_engineering"
        )

        model_trainer_dir = os.path.join(
            latest_folder_path,
            "model_trainer"
        )

        ####################################################
        # Validate folders
        ####################################################

        for folder in [
            ingestion_dir,
            transformation_dir,
            feature_engineering_dir,
            model_trainer_dir,
        ]:

            if not os.path.exists(folder):

                raise FileNotFoundError(
                    f"{folder} does not exist."
                )

        ####################################################
        # Return every artifact path
        ####################################################

        clean_books_file = "clean_book_ratings.csv"
        clean_books_path = os.path.join(
            transformation_dir,
            clean_books_file
        )

        if not os.path.exists(clean_books_path):
            clean_books_file = "clean_books.csv"
            clean_books_path = os.path.join(
                transformation_dir,
                clean_books_file
            )

        return {

            "latest_folder": latest_folder_path,

            # Data Ingestion
            "merged_books": os.path.join(
                ingestion_dir,
                "merged_books.csv"
            ),

            # Data Transformation
            "clean_books": clean_books_path,

            # Feature Engineering
            "user_item_matrix": os.path.join(
                feature_engineering_dir,
                "user_item_matrix.pkl"
            ),

            "book_mapping": os.path.join(
                feature_engineering_dir,
                "book_mapping.pkl"
            ),

            # Model Trainer
            "similarity_matrix": os.path.join(
                model_trainer_dir,
                "similarity_matrix.pkl"
            ),

            "model": os.path.join(
                model_trainer_dir,
                "item_based_model.pkl"
            )

        }

    except Exception as e:

        raise BookRecommendationException(e, sys)