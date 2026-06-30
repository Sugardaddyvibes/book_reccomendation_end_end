import os
import sys
import re
import difflib

import numpy as np
import pandas as pd

from src.logger import logging
from src.exception import BookRecommendationException
from src.utils import get_latest_artifact_paths, load_object


class PredictionPipeline:

    def __init__(self, artifacts_dir="artifacts"):
        try:
            paths = get_latest_artifact_paths(artifacts_dir)

            self.user_item_matrix = load_object(paths["user_item_matrix"])
            self.book_mapping = load_object(paths["book_mapping"])
            self.similarity_matrix = load_object(paths["similarity_matrix"])
            self.books_df = pd.read_csv(paths["clean_books"])

            self.books_df["normalized_title"] = self.books_df["Title"].astype(str).map(self._normalize_title)

            self.indexed_titles = self.user_item_matrix.index.astype(str).map(self._normalize_title)

        except Exception as e:
            raise BookRecommendationException(e, sys)

    @staticmethod
    def _normalize_title(title: str) -> str:
        normalized = str(title).lower().strip()
        normalized = normalized.replace("\n", " ").replace("\t", " ").replace("\r", " ")
        normalized = re.sub(r"[^a-z0-9 ]", "", normalized)
        normalized = re.sub(r"\s+", " ", normalized).strip()
        return normalized

    @staticmethod
    def _score_match(query: str, candidate: str) -> float:
        return difflib.SequenceMatcher(None, query, candidate).ratio()

    def _find_title(self, book_name: str) -> str:
        normalized_book_name = self._normalize_title(book_name)
        titles = self.indexed_titles.values

        if normalized_book_name in titles:
            return normalized_book_name

        query_tokens = normalized_book_name.split()

        # Prefer titles that begin with the query phrase
        startswith_matches = [title for title in titles if title.startswith(normalized_book_name)]
        if startswith_matches:
            best_match = min(startswith_matches, key=len)
            logging.info(
                f"Using startswith title match for '{book_name}': '{best_match}'"
            )
            return best_match

        # Prefer exact substring matches, with earlier position and shorter title
        substring_matches = [title for title in titles if normalized_book_name in title]
        if substring_matches:
            best_match = min(
                substring_matches,
                key=lambda title: (title.find(normalized_book_name), len(title))
            )
            logging.info(
                f"Using substring title match for '{book_name}': '{best_match}'"
            )
            return best_match

        # Next prefer titles that contain all query tokens in order
        def contains_tokens_in_order(value: str, tokens: list[str]) -> bool:
            position = 0
            for token in tokens:
                position = value.find(token, position)
                if position == -1:
                    return False
                position += len(token)
            return True

        token_matches = [
            title
            for title in titles
            if contains_tokens_in_order(title, query_tokens)
        ]
        if token_matches:
            best_match = min(token_matches, key=len)
            logging.info(
                f"Using ordered token title match for '{book_name}': '{best_match}'"
            )
            return best_match

        closest = difflib.get_close_matches(
            normalized_book_name,
            titles,
            n=1,
            cutoff=0.7
        )

        if closest:
            matched_title = closest[0]
            logging.info(
                f"Using closest title match for '{book_name}': '{matched_title}'"
            )
            return matched_title

        raise ValueError(
            f"Book '{book_name}' was not found in the known book list."
        )

    def recommend_books(self, book_name: str, top_n: int = 5):
        try:
            logging.info(f"Generating recommendations for: {book_name}")

            book_name = self._find_title(book_name)
            book_index = int(np.where(self.indexed_titles.values == book_name)[0][0])

            similarity_scores = list(enumerate(self.similarity_matrix[book_index]))
            similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
            similarity_scores = similarity_scores[1: top_n + 1]

            recommended_titles = [self.indexed_titles[i] for i, _ in similarity_scores]

            recommendations = self.books_df[
                self.books_df["normalized_title"].isin(recommended_titles)
            ].drop_duplicates(subset=["normalized_title"])

            recommendations = (
                recommendations
                .set_index("normalized_title")
                .reindex(recommended_titles)
                .reset_index(drop=True)
            )

            recommendations = recommendations.rename(
                columns={
                    "Title": "title",
                    "Author": "authors",
                    "AvgRating": "average_rating"
                }
            )

            output_columns = [
                "book_id",
                "title",
                "authors",
                "original_publication_year",
                "average_rating"
            ]

            return recommendations[output_columns]

        except Exception as e:
            raise BookRecommendationException(e, sys)
        
if __name__ == "__main__":

    predictor = PredictionPipeline()

    recommendations = predictor.recommend_books(
        "hunger games",
        top_n=5
    )

    print(recommendations)
