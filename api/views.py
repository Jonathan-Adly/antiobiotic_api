import requests
import json
from django.shortcuts import render
from rest_framework import generics
from .models import Drug
from .serializers import DrugSerializer
from .forms import DrugForm, IndicationForm, FormulationForm


class DrugList(generics.ListAPIView):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer


class DrugDetail(generics.RetrieveAPIView):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer

    lookup_field = "slug"


def data_entry(request):

    return render(
        request,
        "data_entry.html",
        {"drug_form": DrugForm(), "form_2": FormulationForm, "form_3": IndicationForm},
    )


def auto_complete(request):
    if request.method == "GET":
        user_input = request.GET.get("drug_name")
        url = "https://dailymed.nlm.nih.gov/dailymed/autocomplete.cfm?key=search&returntype=json&term="
        if len(user_input) > 3:
            meds_json = requests.get(
                f"https://dailymed.nlm.nih.gov/dailymed/autocomplete.cfm?key=search&returntype=json&term={user_input}"
            ).content
            meds = json.loads(meds_json)
            medications = meds[:3]
        else:
            medications = None
    return render(
        request, "components/auto_complete.html", {"medications": medications}
    )
