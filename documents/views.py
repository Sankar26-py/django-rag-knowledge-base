from django.shortcuts import render
from .models import Document,DocumentChunk
from .serializers import DocumentSerializer,DocumentChunkSerializer,QuerySerializer
from rest_framework import generics

from rest_framework.views import APIView
from rest_framework.response import Response
from services.retrieval_service import RetrievalService
from services.llm_service import LLMService

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

class QueryView(APIView):
    def post(self,request):
        serializer = QuerySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            question = serializer.validated_data['question']
            results = RetrievalService.search(question)
            context = "\n\n".join(chunk.content for chunk in results)
            answer = LLMService.generate_answer(question,context)
            return Response({
                "question": question,
                "answer": answer,
                "sources": [
                    chunk.id
                    for chunk in results
                ]
            })