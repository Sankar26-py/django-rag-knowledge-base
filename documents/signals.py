from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Document,DocumentChunk
from services.pdf_service import PDFService
from services.chunk_service import ChunkService

@receiver(post_save,sender = Document)

def process_document(sender,instance,created,**kwargs):

    if not created:
        return

    # Extract text from the PDF
    text = PDFService.extract_text(instance.pdf_file.path)
    # Chunk the extracted text
    chunks = ChunkService.chunk_text(text)

    chunk_objects = []

    for index, chunk in enumerate(chunks):

        chunk_objects.append(
            DocumentChunk(
                document=instance,
                chunk_number=index,
                content=chunk
            )
        )

    # Save the chunks to the database
    DocumentChunk.objects.bulk_create(chunk_objects)
