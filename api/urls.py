from django.urls import path
from .views import DrugList, DrugDetail


urlpatterns = [
    path("<slug:slug>/", DrugDetail.as_view()),
    path("", DrugList.as_view()),
]
