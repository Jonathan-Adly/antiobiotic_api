import requests
import json
from django.shortcuts import render
from rest_framework import generics, permissions
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Drug
from .serializers import DrugSerializer
from .forms import DrugForm, IndicationForm, FormulationForm


class DrugList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer


class DrugDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer

    lookup_field = "slug"


@login_required
def data_entry(request):

    return render(
        request,
        "data_entry.html",
        {
            "drug_form": DrugForm(),
            "formulation_form": FormulationForm(),
            "indication_form": IndicationForm(),
        },
    )


@require_POST
@login_required
def handle_drug_form(request):
    pass
    # form = DrugForm(request.POST)
    # if form.is_valid():
    # form


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
