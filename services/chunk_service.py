class ChunkService:
    @staticmethod
    def chunk_text(text,chunk_size =1000,overlap = 100):
        chunks = []
        start = 0
        while start < len(text):

            end = start + chunk_size
            chunk = text[start:end]#0:1000,1000:2000,2000:3000
            chunks.append(chunk)
            start += chunk_size - overlap #1000-100=900,2000-100=1900,3000-100=2900

        return chunks