import os
import re
import sys

import pandas as pd

from src.logger import logging
from src.exception import BookRecommendationException

from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact


class DataTransformation:

    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_transformation_config: DataTransformationConfig
    ):

        self.ingestion_artifact = data_ingestion_artifact

        self.config = data_transformation_config

    ####################################################
    # Read Data
    ####################################################

    def _load_data(self):

        logging.info("Loading merged dataset...")

        df = pd.read_csv(self.ingestion_artifact.merged_file_path)

        logging.info(f"Dataset Loaded Successfully : {df.shape}")

        return df

    ####################################################
    # Remove Missing Values
    ####################################################

    def _remove_missing_values(self, df):

        logging.info("Removing Missing Values...")

        df = df.dropna(
            subset=[
                "user_id",
                "book_id",
                "rating",
                "Title"
            ]
        )

        logging.info(f"Shape After Removing Missing Values : {df.shape}")

        return df

    ####################################################
    # Remove Duplicates
    ####################################################

    def _remove_duplicates(self, df):

        logging.info("Removing Duplicate Records...")

        before = len(df)

        df = df.drop_duplicates()

        after = len(df)

        logging.info(f"Removed {before-after} Duplicate Rows")

        return df

    ####################################################
    # Clean Book Titles
    ####################################################

    def _clean_titles(self, df):

        logging.info("Cleaning Book Titles...")

        df["Title"] = (

            df["Title"]

            .str.lower()

            .str.strip()

            .str.replace(r"[^a-zA-Z0-9 ]", "", regex=True)

        )

        return df

    ####################################################
    # Clean Publication Year
    ####################################################

    def _clean_publication_year(self, df):

        logging.info("Cleaning Publication Year...")

        df["original_publication_year"] = (

            df["Publication Year"]

            .fillna(0)

            .astype(int)

        )

        return df

    ####################################################
    # Filter Users
    ####################################################

    def _filter_users(self, df):

        logging.info("Filtering Inactive Users...")

        user_counts = df["user_id"].value_counts()

        active_users = user_counts[
            user_counts >= self.config.minimum_user_ratings
        ].index

        df = df[df["user_id"].isin(active_users)]

        logging.info(f"Shape After User Filtering : {df.shape}")

        return df

    ####################################################
    # Filter Books
    ####################################################

    def _filter_books(self, df):

        logging.info("Filtering Unpopular Books...")

        book_counts = df["book_id"].value_counts()

        popular_books = book_counts[
            book_counts >= self.config.minimum_book_ratings
        ].index

        df = df[df["book_id"].isin(popular_books)]

        logging.info(f"Shape After Book Filtering : {df.shape}")

        return df

    ####################################################
    # Save Dataset
    ####################################################

    def _save_dataset(self, df):

        logging.info("Saving Clean Dataset...")

        os.makedirs(
            self.config.data_transformation_dir,
            exist_ok=True
        )

        df.to_csv(
            self.config.transformed_file_path,
            index=False
        )

        logging.info(
            f"Dataset Saved Successfully : {self.config.transformed_file_path}"
        )

    ####################################################
    # Main Transformation Pipeline
    ####################################################

    def initiate_data_transformation(self):

        try:

            logging.info("=" * 60)
            logging.info("Data Transformation Started")
            logging.info("=" * 60)

            df = self._load_data()

            total_before = len(df)

            df = self._remove_missing_values(df)

            df = self._remove_duplicates(df)

            df = self._clean_titles(df)

            df = self._clean_publication_year(df)

            df = self._filter_users(df)

            df = self._filter_books(df)

            self._save_dataset(df)

            total_after = len(df)

            artifact = DataTransformationArtifact(

                transformed_file_path=self.config.transformed_file_path,

                total_records_before=total_before,

                total_records_after=total_after,

                removed_records=total_before-total_after,

                status=True,

                message="Data Transformation Completed Successfully"

            )

            logging.info("=" * 60)
            logging.info("Data Transformation Completed Successfully")
            logging.info("=" * 60)

            return artifact

        except Exception as e:

            raise BookRecommendationException(e, sys)