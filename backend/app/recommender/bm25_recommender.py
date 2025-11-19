from sqlalchemy.orm import Session
from ..schemas import UserAnswerSubmission, PlantRecommendation, UserFreeTextSubmission
from ..services import bm25_service
from rank_bm25 import BM25Okapi



# Implementation oriented on example in documentation https://pypi.org/project/rank-bm25/
def get_recommendations(num_perfect: int, num_good: int, num_bad: int, user_answers: UserAnswerSubmission, db: Session):

    print(user_answers)


    # make corpus based on dataset
    dataset_corpus = bm25_service.create_plant_corpus(db=db)

    tokenized_corpus = [doc.split(" ") for doc in dataset_corpus]
    bm25 = BM25Okapi(tokenized_corpus)

    # create user query based on user questionnaire
    user_query = bm25_service.create_query(db=db, user_answers=user_answers)
    tokenized_query = user_query.split(" ")

    doc_scores = bm25.get_scores(tokenized_query)
    print(doc_scores)
    #todo best scores is top_n method, others I have to retrieve manually

    # extract top n perfect fits
    perfect_fits = bm25.get_top_n(tokenized_query, dataset_corpus, n=num_perfect)

    # extract top n good fits

    # extract top n bad fits


    plants_results = bm25_service.get_plant_based_on_bm25_document(db=db, results=perfect_fits)


    return PlantRecommendation(
        label="BM25_perfect_fit",
        recommendation=plants_results
    )


