import os
import faiss
import pickle
import numpy as np

from documents.models import DocumentChunk


class IndexService:

    INDEX_DIR = "storage/faiss"
    INDEX_PATH = os.path.join(INDEX_DIR, "index.faiss")
    META_PATH = os.path.join(INDEX_DIR, "metadata.pkl")

    @classmethod
    def build_index(cls):

        # Create directory if it doesn't exist
        os.makedirs(cls.INDEX_DIR, exist_ok=True)

        chunks = list(DocumentChunk.objects.exclude(embedding__isnull=True))

        if not chunks:
            print("No embeddings found.")
            return

        vectors = np.array(
            [chunk.embedding for chunk in chunks],
            dtype=np.float32
        )

        index = faiss.IndexFlatL2(vectors.shape[1])
        index.add(vectors)

        faiss.write_index(index, cls.INDEX_PATH)

        with open(cls.META_PATH, "wb") as f:
            pickle.dump([chunk.id for chunk in chunks], f)

        print(f"Indexed {len(chunks)} chunks successfully.")