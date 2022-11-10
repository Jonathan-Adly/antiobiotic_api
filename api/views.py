from rest_framework import generics
from .models import Drug
from .serializers import DrugSerializer


class DrugList(generics.ListAPIView):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer


class DrugDetail(generics.RetrieveAPIView):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer

    lookup_field = "slug"
