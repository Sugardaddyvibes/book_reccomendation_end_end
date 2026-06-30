import os
import sys
import pickle

from sklearn.metrics.pairwise import cosine_similarity

from src.logger import logging
from src.exception import BookRecommendationException

from src.entity.config_entity import ModelTrainerConfig

from src.entity.artifact_entity import (
    FeatureEngineeringArtifact,
    ModelTrainerArtifact
)


class ModelTrainer:

    def __init__(
        self,
        config: ModelTrainerConfig,
        feature_engineering_artifact: FeatureEngineeringArtifact
    ):

        self.config = config

        self.feature_artifact = feature_engineering_artifact

    ###########################################################

    def _load_user_item_matrix(self):

        logging.info("Loading User-Item Matrix...")

        with open(
            self.feature_artifact.user_item_matrix_path,
            "rb"
        ) as file:

            matrix = pickle.load(file)

        logging.info(f"Matrix Shape : {matrix.shape}")

        return matrix

    ###########################################################

    def _train_model(self, matrix):

        logging.info("Computing Cosine Similarity Matrix...")

        similarity_matrix = cosine_similarity(matrix)

        logging.info(
            f"Similarity Matrix Shape : {similarity_matrix.shape}"
        )

        return similarity_matrix

    ###########################################################

    def _save_model(self, similarity_matrix):

        os.makedirs(
            self.config.model_trainer_dir,
            exist_ok=True
        )

        with open(
            self.config.similarity_matrix_path,
            "wb"
        ) as file:

            pickle.dump(
                similarity_matrix,
                file
            )

        # Optional: save everything together
        model = {
            "similarity_matrix": similarity_matrix
        }

        with open(
            self.config.model_path,
            "wb"
        ) as file:

            pickle.dump(
                model,
                file
            )

        logging.info("Model Saved Successfully.")

    ###########################################################

    def initiate_model_trainer(self):

        try:

            logging.info("=" * 60)
            logging.info("Model Training Started")
            logging.info("=" * 60)

            matrix = self._load_user_item_matrix()

            similarity_matrix = self._train_model(matrix)

            self._save_model(similarity_matrix)

            artifact = ModelTrainerArtifact(

                similarity_matrix_path=self.config.similarity_matrix_path,

                model_path=self.config.model_path,

                total_books=matrix.shape[0],

                status=True,

                message="Item-Based Model Training Completed Successfully"

            )

            logging.info("=" * 60)
            logging.info("Model Training Completed")
            logging.info("=" * 60)

            return artifact

        except Exception as e:

            raise BookRecommendationException(e, sys)