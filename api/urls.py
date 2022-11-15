from django.urls import path
from .views import DrugList, DrugDetail, data_entry, auto_complete


urlpatterns = [
    path("", data_entry, name="data_entry"),
    path("autocomplete/", auto_complete, name="auto_complete"),
    path("drug/<slug:slug>/", DrugDetail.as_view()),
    path("drug-list/", DrugList.as_view()),
]
