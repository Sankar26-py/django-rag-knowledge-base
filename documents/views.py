from django.shortcuts import render
from .models import Document,DocumentChunk
from .serializers import DocumentSerializer,DocumentChunkSerializer
from rest_framework import generics

# Create your views here.
class DocumentUploadView(generics.CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class DocumentListView(generics.ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class DocumentDetailView(generics.RetrieveAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer