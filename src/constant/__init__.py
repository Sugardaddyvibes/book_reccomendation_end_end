import os

##########################################
# Project Information
##########################################

PROJECT_NAME = "BookRecommendation"

PIPELINE_NAME = "BookRecommendationPipeline"

ARTIFACT_DIR = "artifacts"

MODEL_DIR = "saved_models"

LOG_DIR = "logs"

CONFIG_DIR = "config"

##########################################
# Dataset
##########################################

DATA_DIR = "data"

BOOK_FILE_NAME = "Books.csv"

RATING_FILE_NAME = "Ratings.csv"

##########################################
# Data Ingestion
##########################################

DATA_INGESTION_DIR = "data_ingestion"

MERGED_DATA_NAME = "merged_books.csv"

##########################################
# Data Transformation
##########################################

DATA_TRANSFORMATION_DIR = "data_transformation"

TRANSFORMED_DATA_FILE_NAME = "clean_book_ratings.csv"

MINIMUM_USER_RATINGS = 5

MINIMUM_BOOK_RATINGS = 5

##########################################
# FEATURE ENGINEERING
##########################################

FEATURE_ENGINEERING_DIR = "feature_engineering"

USER_ITEM_MATRIX_FILE_NAME = "user_item_matrix.pkl"

BOOK_MAPPING_FILE_NAME = "book_mapping.pkl"

#############################################
# MODEL TRAINER
#############################################

MODEL_TRAINER_DIR = "model_trainer"

SIMILARITY_MATRIX_FILE_NAME = "similarity_matrix.pkl"

MODEL_FILE_NAME = "item_based_model.pkl"

##########################################
# Evaluation
##########################################

MODEL_EVALUATION_DIR = "model_evaluation"

METRIC_FILE_NAME = "metrics.json"

##########################################
# Prediction
##########################################

PREDICTION_DIR = "prediction"

TOP_K = 5