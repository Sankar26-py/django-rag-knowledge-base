import faiss
import pickle
import numpy as np

from documents.models import DocumentChunk
from services.embedding_service import EmbeddingService


class RetrievalService:

    INDEX_PATH = "storage/faiss/index.faiss"
    META_PATH = "storage/faiss/metadata.pkl"

    @classmethod
    def search(cls, query, top_k=5):

        index = faiss.read_index(cls.INDEX_PATH)

        with open(cls.META_PATH, "rb") as f:
            chunk_ids = pickle.load(f)

        query_vector = np.array(
            [EmbeddingService.generate_embedding(query)],
            dtype=np.float32
        )

        distances, indices = index.search(query_vector, top_k)

        results = []

        for idx in indices[0]:

            idx = int(idx)

            if idx < 0 or idx >= len(chunk_ids):
                continue

            chunk_map = {
                chunk.id: chunk
                    for chunk in DocumentChunk.objects.filter(id__in=chunk_ids)
                    }

            results.append(chunk_map[chunk_ids[idx]])

        return results