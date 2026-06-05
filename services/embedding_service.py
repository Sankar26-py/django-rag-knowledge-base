from sentence_transformers import SentenceTransformer

class EmbeddingService:

    model = model = SentenceTransformer("all-MiniLM-L6-v2")# Load the pre-trained model for generating embeddings

    @classmethod
    def generate_embedding(cls,text):
        embedding = cls.model.encode(text) # Generate the embedding
        return embedding.tolist()# Convert the embedding to a list for storage in the database
    