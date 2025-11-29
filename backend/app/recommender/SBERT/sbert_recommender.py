import numpy as np
import torch
from sqlalchemy.orm import Session
from app.recommender.SBERT import sbert_service
from app.schemas import PlantRecommendation, UserFreeTextSubmission
from app.services import recommender_placeholder_service
from sentence_transformers import SentenceTransformer, SimilarityFunction


""" -----------------------------------------------------------------------------------------------
 SBERT Recommender https://www.kaggle.com/refs/hf-model/sentence-transformers/all-MiniLM-L6-v2
 Calculation of similarities oriented on the documentation at 
 https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html
----------------------------------------------------------------------------------------------- """
class SBertRecommender:
    def __init__(self, db: Session):
        self.db = db
        self.sbert = self._create_sbert_model()
        self.dataset_text_representation = self._create_dataset_text_representation()
        self.dataset_embeddings = self._create_dataset_embeddings()


    @staticmethod
    def _create_sbert_model():
        return SentenceTransformer(
            'sentence-transformers/all-MiniLM-L6-v2',
            similarity_fn_name=SimilarityFunction.COSINE)


    def _create_dataset_text_representation(self):
        return sbert_service.create_text_representation_plants(db=self.db)


    def _create_dataset_embeddings(self):
        plants_text_tuples = sbert_service.create_text_representation_plants(db=self.db)
        plant_sentences = [text for id, text in plants_text_tuples]
        return self.sbert.encode(plant_sentences)


    def recommend(self, user_free_text: UserFreeTextSubmission, num_perfect: int, num_good: int, num_bad: int):

        # Dataset embeddings are already created in constructor. Now building text embeddings for user input
        user_query_text = sbert_service.create_text_representation_user_query(user_query=user_free_text)
        user_query_embeddings = self.sbert.encode(user_query_text)

        # Calculate cosine similarity
        similarities = self.sbert.similarity(self.dataset_embeddings, user_query_embeddings)

        # Make list out of matrix, all rows, first column
        scores = similarities.flatten()
        top_scores, top_indices = torch.topk(scores, k=num_perfect)

        # Extract the top plant tuples
        top_plants = [self.dataset_text_representation[i-1] for i in top_indices]
        plant_sentences = [text for id, text in self.dataset_text_representation]

        # top_plants now contains [(id, text), ...] in descending similarity order
        print(f"top indices{top_indices}, top_scores{top_scores}")
        for plant_id, plant_text in top_plants:
            print(f"Plant ID: {plant_id}, Text: {plant_text}")
        print("Original plant text:", plant_sentences[top_indices[0]-1])
        print("Original plant text:", plant_sentences[top_indices[1]-1])
        print("Original plant text:", plant_sentences[top_indices[2]-1])


        plant_list = recommender_placeholder_service.fetch_plant_recommendations_randomly(num_plants=num_perfect, db=self.db)

        return [PlantRecommendation(label="SBERT_perfect", recommendation=plant_list),
                PlantRecommendation(label="SBERT_good", recommendation=plant_list),
                PlantRecommendation(label="SBERT_mismatch", recommendation=plant_list)]


