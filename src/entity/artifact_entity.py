from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:

    merged_file_path: str

    total_books: int

    total_ratings: int

    merged_records: int

    is_ingested: bool

    message: str



@dataclass
class DataTransformationArtifact:

    transformed_file_path: str

    total_records_before: int

    total_records_after: int

    removed_records: int

    status: bool

    message: str
from dataclasses import dataclass


@dataclass
class FeatureEngineeringArtifact:

    user_item_matrix_path: str

    book_mapping_path: str

    total_users: int

    total_books: int

    matrix_shape: tuple

    status: bool

    message: str

from dataclasses import dataclass


@dataclass
class ModelTrainerArtifact:

    similarity_matrix_path: str

    model_path: str

    total_books: int

    status: bool

    message: str