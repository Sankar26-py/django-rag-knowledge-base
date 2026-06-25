from django.core.management.base import BaseCommand

from services.index_service import IndexService

class Command(BaseCommand):

    help = "Build FAISS Index"

    def handle(self, *args, **kwargs):

        IndexService.build_index()

        self.stdout.write(self.style.SUCCESS("FAISS index built successfully."))