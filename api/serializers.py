from rest_framework import serializers
from .models import Drug, Dosage, Formulation, Bacteria, Indication


class DrugSerializer(serializers.ModelSerializer):

    routes = serializers.ReadOnlyField()
    formulationsPO = serializers.ReadOnlyField()
    formulationsIV = serializers.ReadOnlyField()
    formulationsOther = serializers.ReadOnlyField()
    indications = serializers.ReadOnlyField(source="get_indications")
    bacteria = serializers.ReadOnlyField(source="get_bacteria")

    class Meta:
        model = Drug
        exclude = ["created_at"]
        lookup_field = "slug"
