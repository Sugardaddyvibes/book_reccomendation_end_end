import os
import sys
import pickle

import pandas as pd

from src.logger import logging
from src.exception import BookRecommendationException

from src.entity.config_entity import FeatureEngineeringConfig
from src.entity.artifact_entity import (
    FeatureEngineeringArtifact,
    DataTransformationArtifact
)


class FeatureEngineering:

    def __init__(
        self,
        config: FeatureEngineeringConfig,
        transformation_artifact: DataTransformationArtifact
    ):

        self.config = config

        self.transformation_artifact = transformation_artifact

    ########################################################

    def _load_data(self):

        logging.info("Loading Clean Dataset...")

        df = pd.read_csv(
            self.transformation_artifact.transformed_file_path
        )

        return df

    ########################################################

    def _create_user_item_matrix(self, df):

        logging.info("Creating User-Item Matrix...")

        matrix = df.pivot_table(

            index="Title",

            columns="user_id",

            values="rating",

            fill_value=0

        )

        logging.info(f"Matrix Shape : {matrix.shape}")

        return matrix

    ########################################################

    def _create_book_mapping(self, matrix):

        logging.info("Creating Book Mapping...")

        mapping = {

            idx: Title

            for idx, Title in enumerate(matrix.index)

        }

        return mapping

    ########################################################

    def _save_artifacts(self, matrix, mapping):

        os.makedirs(
            self.config.feature_engineering_dir,
            exist_ok=True
        )

        with open(
            self.config.user_item_matrix_path,
            "wb"
        ) as file:

            pickle.dump(matrix, file)

        with open(
            self.config.book_mapping_path,
            "wb"
        ) as file:

            pickle.dump(mapping, file)

    ########################################################

    def initiate_feature_engineering(self):

        try:

            logging.info("=" * 60)

            logging.info("Feature Engineering Started")

            logging.info("=" * 60)

            df = self._load_data()

            matrix = self._create_user_item_matrix(df)

            mapping = self._create_book_mapping(matrix)

            self._save_artifacts(
                matrix,
                mapping
            )

            artifact = FeatureEngineeringArtifact(

                user_item_matrix_path=self.config.user_item_matrix_path,

                book_mapping_path=self.config.book_mapping_path,

                total_users=matrix.shape[1],

                total_books=matrix.shape[0],

                matrix_shape=matrix.shape,

                status=True,

                message="Feature Engineering Completed Successfully"

            )

            logging.info("Feature Engineering Completed")

            return artifact

        except Exception as e:

            raise BookRecommendationException(e, sys)