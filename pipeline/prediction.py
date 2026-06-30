import argparse
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from src.pipeline.prediction_pipeline import PredictionPipeline
from src.exception import BookRecommendationException


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate book recommendations from a saved item-based model."
    )
    parser.add_argument(
        "--book",
        required=True,
        help="The book title to use as the recommendation query."
    )
    parser.add_argument(
        "--top_n",
        type=int,
        default=5,
        help="Number of book recommendations to return."
    )
    parser.add_argument(
        "--artifacts_dir",
        default=str(project_root / "artifacts"),
        help="Path to the artifacts directory containing saved pipeline outputs."
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        pipeline = PredictionPipeline(artifacts_dir=args.artifacts_dir)
        recommendations = pipeline.recommend_books(args.book, top_n=args.top_n)

        if recommendations.empty:
            print("No recommendations were found for the given book title.")
            return

        print("Recommendations for:", args.book)
        print(recommendations.to_string(index=False))

    except BookRecommendationException as exc:
        print("Prediction failed:", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
