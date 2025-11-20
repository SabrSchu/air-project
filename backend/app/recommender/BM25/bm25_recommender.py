from sqlalchemy.orm import Session
from app.schemas import UserAnswerSubmission, PlantRecommendation
from app.recommender.BM25 import bm25_service
from rank_bm25 import BM25Okapi

PADDING = 10

""" -----------------------------------------------------------------------------------------------
 Class that represents the recommender algorithm BM25. The Implementation is based on the library
 documentation https://pypi.org/project/rank-bm25/. 
 Upon initialization, the preprocessing part of the BM25 algorithm is executed. A document corpus
 is created based on the plant entries in the database and an instance of the algorithm is created.
 
 BM25 is implementing lexical search, where a query is compared against a document (in our case, 
 the plants in the database. Each row is one document). 
 For more information, see https://huggingface.co/blog/xhluca/bm25s.
----------------------------------------------------------------------------------------------- """
class BM25Recommender:
    def __init__(self, db: Session):
        self.db = db
        self.corpus = self._create_plant_corpus()
        self.tokenized_corpus = self._tokenize_corpus()
        self.bm25 = self._create_bm25_instance()

    # make corpus based on dataset
    def _create_plant_corpus(self):
        return bm25_service.create_plant_corpus(db=self.db)

    # tokenizing the corpus
    def _tokenize_corpus(self):
        return [doc.split(" ") for doc in self.corpus]

    # we use the imported BM25 algorithm
    def _create_bm25_instance(self):
        return BM25Okapi(self.tokenized_corpus)

    def recommend(self, user_answers: UserAnswerSubmission, num_perfect: int, num_good: int, num_bad: int):

        # creating user query based on user questionnaire
        user_query = bm25_service.create_query(db=self.db, user_answers=user_answers)
        tokenized_query = user_query.split(" ")

        # retrieving scores, each entry in the corpus corresponds to a score
        doc_scores = self.bm25.get_scores(tokenized_query)

        # extract top n perfect fits (plus some extra values to be able to prioritize results with image url)
        perfect_fits = self.bm25.get_top_n(tokenized_query, self.corpus, n=num_perfect + PADDING)

        plants_results = bm25_service.get_plant_based_on_bm25_document(db=self.db,
                                                                       results=perfect_fits,
                                                                       max_results=num_perfect)

        # extract top n good fits (70-90 percentile)
        good_fits = bm25_service.get_fits_in_percentile(scores=doc_scores,
                                                        dataset_corpus=self.corpus,
                                                        n=num_good + PADDING,
                                                        min_p=70,
                                                        max_p=90)

        good_results = bm25_service.get_plant_based_on_bm25_document(db=self.db, results=good_fits, max_results=num_good)

        # extract top n bad fits (5-20 percentile)
        bad_fits = bm25_service.get_fits_in_percentile(scores=doc_scores,
                                                       dataset_corpus=self.corpus,
                                                       n=num_bad + PADDING,
                                                       min_p=5,
                                                       max_p=20)

        bad_results = bm25_service.get_plant_based_on_bm25_document(db=self.db, results=bad_fits, max_results=num_bad)

        return [ PlantRecommendation(label="BM25_perfect", recommendation=plants_results),
                 PlantRecommendation(label="BM25_good", recommendation=good_results),
                 PlantRecommendation(label="BM25_mismatch", recommendation=bad_results)]


