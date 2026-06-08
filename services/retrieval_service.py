import faiss
import numpy as np
#from rich.prompt import result
from documents.models import DocumentChunk
from services.embedding_service import EmbeddingService


class RetrievalService:
    @staticmethod
    def search(query,top_k=5):
        chunks = list(DocumentChunk.objects.exclude(embedding__isnull=True)) # Exclude chunks without embeddings
        if not chunks:
            return [] # Return an empty list if there are no chunks with embeddings
        
        vectors = np.array([chunk.embedding for chunk in chunks],dtype = np.float32)# Create a matrix of embeddings for the chunks

        index = faiss.IndexFlatL2(vectors.shape[1])# Create a FAISS index for efficient similarity search
        index.add(vectors) # Add the chunk embeddings to the index

        queryvector = np.array([EmbeddingService.generate_embedding(query)],
                               dtype = np.float32).reshape(1, -1) # Generate the embedding for the query and reshape it for FAISS
        
        distances, indices = index.search(queryvector, top_k) # Search for the top_k most similar chunks

        results = []
        for idx in indices[0]:# Iterate through the indices of the top_k results
            idx = int(idx)
            if idx < 0:
                continue
            if idx >= len(chunks):
                continue
            results.append(chunks[idx])# Append the index of the chunk to the results list

        for result in results:
            print(result.content[:200])
            print("-" * 50)
        return results # Return the list of indices of the most relevant chunks