import numpy as np
import torch
from sqlalchemy.orm import Session
from app.recommender.SBERT import sbert_service
from app.schemas import PlantRecommendation, UserFreeTextSubmission
from sentence_transformers import SentenceTransformer, SimilarityFunction

PADDING = 10

""" -----------------------------------------------------------------------------------------------
Class that represents a sentence transformer model (SBERT), namely MiniLM-L6-v2, see
https://www.kaggle.com/refs/hf-model/sentence-transformers/all-MiniLM-L6-v2. 
It maps sentences and paragraphs into a 384 dimensional vector space and can then be used for 
clusterings or semantic search. After initialization of this pre-trained model, a text-representation
and embeddings of the dataset and the user query (free text) is being done. 
By finding the cosine similarities (of different percentiles) different recommendations are returned.

Calculation of similarities oriented on the documentation at 
https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html
----------------------------------------------------------------------------------------------- """
class SBertRecommender:
    def __init__(self, db: Session):
        self.db = db
        self.sbert = self._create_sbert_model()
        self.dataset_text_representation = self._create_dataset_text_representation()
        self.dataset_embeddings = self._create_dataset_embeddings()

    # Initialization of the model
    @staticmethod
    def _create_sbert_model():
        return SentenceTransformer(
            'sentence-transformers/all-MiniLM-L6-v2',
            similarity_fn_name=SimilarityFunction.COSINE)

    # Text representation creation of database entries - is a preprocessing step
    def _create_dataset_text_representation(self):
        return sbert_service.create_text_representation_plants(db=self.db)

    # Dataset embeddings are created from the database entries
    def _create_dataset_embeddings(self):
        plants_text_tuples = sbert_service.create_text_representation_plants(db=self.db)
        plant_sentences = [text for id, text in plants_text_tuples]
        return self.sbert.encode(plant_sentences)


    # The recommendation step itself
    def recommend(self, user_free_text: UserFreeTextSubmission, num_perfect: int, num_good: int, num_bad: int):

        # Dataset embeddings are already created in constructor. Now building text embeddings from user input
        user_query_text = sbert_service.create_text_representation_user_query(user_query=user_free_text)
        user_query_embeddings = self.sbert.encode(user_query_text)

        # Calculate cosine similarity
        similarities = self.sbert.similarity(self.dataset_embeddings, user_query_embeddings)
        scores = similarities.flatten()

        # Fancy retrieve top n matches. Applied Padding to be able to prioritize plants with existing image url
        top_scores, top_indices = torch.topk(scores, k=num_perfect + PADDING)



        # Retrieve plants from db, but also prioritize those with image url
        perfect_plants = sbert_service.get_plant_data_from_score_indices(db=self.db,
                                                                         indices=top_indices.tolist(),
                                                                         scores=top_scores.tolist(),
                                                                         num=num_perfect)

        # sbert_service.print_infos(perfect_plants, "PERFECT")


        # Get percentiles to find good and bad matches too
        percentiles = torch.quantile(scores, torch.tensor([0.25, 0.75]))
        p25, p75 = percentiles.tolist()

        # Get good matches above 75 percentile, elegantly with the torch library
        good_matches_indices = torch.where(scores >= p75)[0]
        good_matches_indices = good_matches_indices[:num_good + PADDING].tolist()
        good_match_scores = [float(scores[i]) for i in good_matches_indices]


        # Retrieve plants from db, but also prioritize those with image url
        good_plants = sbert_service.get_plant_data_from_score_indices(db=self.db,
                                                                      indices=good_matches_indices,
                                                                      scores=good_match_scores,
                                                                      num=num_good)

        # sbert_service.print_infos(good_plants, "GOOD")

        # Get mismatches under 25th percentile
        bad_indices = torch.where(scores <= p25)[0]
        bad_indices = bad_indices[:num_bad + PADDING].tolist()
        bad_match_scores = [float(scores[i]) for i in bad_indices]


        bad_plants = sbert_service.get_plant_data_from_score_indices(db=self.db,
                                                                     indices=bad_indices,
                                                                     scores=bad_match_scores,
                                                                     num=num_bad)
        # sbert_service.print_infos(bad_plants, "BAD")



        return [PlantRecommendation(label="SBERT_perfect", recommendation=perfect_plants),
                PlantRecommendation(label="SBERT_good", recommendation=good_plants),
                PlantRecommendation(label="SBERT_mismatch", recommendation=bad_plants)]


