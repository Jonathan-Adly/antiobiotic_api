from django.urls import path
from .views import DrugList, DrugDetail, data_entry, auto_complete, handle_drug_form


urlpatterns = [
    path("", data_entry, name="data_entry"),
    path("drug-form", handle_drug_form, name="drug_form"),
    path("autocomplete/", auto_complete, name="auto_complete"),
    path("drug/<slug:slug>/", DrugDetail.as_view()),
    path("drug-list/", DrugList.as_view()),
]
