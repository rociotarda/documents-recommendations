import numpy as np
import tensorflow_hub as hub

WEIGHT = 0.2

class RecommendationByKeywordsNumberSimilarities:
    def initialize(self, documents):
        self.documents = documents
        self.embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
        self.weight = WEIGHT

    def prepare_data(self, new_keywords):
        keywords_by_document = self.documents.get_keywords_by_document()
        # Calculate the similarities between the new keywords and the keywords in each document
        # To calculate this similarity, count the keywords that each document has in common with the entered document, and divide that
        # number of similarities times the total number of keywords per document (#words_in_common / #words_in_that_document)
        # And then I normalize all the results so that they are between [0, 1]

        similarities = []
        for document_keywords in keywords_by_document.values():
            num_common_words = sum(1 for word in document_keywords if word in new_keywords)
            similarity = num_common_words / len(document_keywords) if len(document_keywords) > 0 else 0
            similarities.append(similarity)
        
        return np.array(similarities)

    def get_recommendations(self, document_to_recommend):
        similarities = self.prepare_data(document_to_recommend.keywords)

        # Normalize similarities
        max_similarity = np.max(similarities)
        if max_similarity == 0:
            print("No matches found.")
            return {}

        normalized_similarities = (similarities / max_similarity) * self.weight

        # Map probabilities to document IDs
        probs_by_doc_dict = {doc_id: prob for doc_id, prob in zip(self.documents.get_documents().keys(), normalized_similarities)}

        return probs_by_doc_dict
