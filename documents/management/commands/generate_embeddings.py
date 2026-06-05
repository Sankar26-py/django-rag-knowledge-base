from django.core.management.base import BaseCommand
from documents.models import DocumentChunk
from services.embedding_service import EmbeddingService

class Command(BaseCommand):
    help = 'Generate embeddings for document chunks that do not have them yet'

    def handle(self,*args,**kwargs):
        chunks = DocumentChunk.objects.filter(embedding__isnull=True) # Get all chunks that do not have embeddings
        self.stdout.write(f"Found {chunks.count()} chunks")
        for chunk in chunks:
            embedding = EmbeddingService.generate_embedding(chunk.content) # Generate the embedding for the chunk content
            chunk.embedding = embedding # Assign the generated embedding to the chunk
            chunk.save(update_fields=["embedding"]) # Save the updated chunk to the database
            self.stdout.write(f"Processed {chunk.id}")
            self.stdout.write(self.style.SUCCESS(f'Generated embedding for chunk {chunk.id} of document "{chunk.document.title}"'))

        self.stdout.write(self.style.SUCCESS("Completed"))

