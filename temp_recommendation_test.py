from src.pipeline.prediction_pipeline import PredictionPipeline

p = PredictionPipeline()
queries = ['hunger games', 'the hunger games', 'harry potter', 'gone girl', '1984', 'twilight', 'the fault in our stars']
for q in queries:
    try:
        matched = p._find_title(q)
        recs = p.recommend_books(q, top_n=5)['title'].tolist()
        print('QUERY:', q)
        print('MATCHED:', matched)
        print('RECOMMENDED:', recs)
        print('---')
    except Exception as e:
        print('ERROR', q, e)
