from django.db import models

# Create your models here.
class Document(models.Model):
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to = 'documents/')
    uploaded_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering =["-uploaded_at"]

    def __str__(self):
        return self.title
    
class DocumentChunk(models.Model):

    document = models.ForeignKey(Document,on_delete=models.CASCADE,related_name="chunks")
    content = models.TextField()
    chunk_number = models.IntegerField()
    embedding = models.JSONField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"{self.document.title}" f"-{self.chunk_number}")