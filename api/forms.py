from django import forms

from .models import Drug, Formulation, Indication
from django.urls import reverse_lazy


class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = [
            "drug_name",
            "brand_name",
            "is_sulfa",
            "is_penicillin",
            "is_cephalosporin",
            "is_combo",
            "hepatic_adjustment",
            "renal_adjustment",
            "is_generic",
            "hepatic_comments",
            "renal_comments",
        ]

        labels = {
            "drug_name": "",
            "brand_name": "",
            "is_sulfa": "",
            "is_penicillin": "",
            "is_cephalosporin": "",
            "is_combo": "",
            "hepatic_adjustment": "",
            "renal_adjustment": "",
            "is_generic": "",
            "hepatic_comments": "",
            "renal_comments": "",
        }

        widgets = {
            "drug_name": forms.TextInput(
                attrs={
                    "placeholder": "Amoxicillin",
                    "class": "form-control",
                    "id": "drug_name",
                    "hx-get": reverse_lazy("auto_complete"),
                    "hx-target": "#autoComplete",
                    "hx-swap": "outerHTML",
                    "hx-trigger": "keyup changed delay:500ms",
                    "required": "required",
                }
            ),
            "brand_name": forms.TextInput(
                attrs={
                    "placeholder": "Amox",
                    "class": "form-control",
                    "id": "brand_name",
                }
            ),
            "is_generic": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "type": "checkbox",
                    "id": "is_generic",
                }
            ),
            "is_penicillin": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "type": "checkbox",
                    "id": "is_penicillin",
                }
            ),
            "is_sulfa": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "type": "checkbox",
                    "id": "is_sulfa",
                }
            ),
            "is_cephalosporin": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "type": "checkbox",
                    "id": "is_cephalosporin",
                }
            ),
            "hepatic_adjustment": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "type": "checkbox",
                    "id": "hepatic_adjustment",
                    "_": "on change toggle .d-none on #hepatic_box",
                }
            ),
            "renal_adjustment": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "type": "checkbox",
                    "id": "renal_adjustment",
                    "_": "on change toggle .d-none on #renal_box",
                }
            ),
            "is_combo": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "type": "checkbox",
                    "id": "is_combo",
                }
            ),
            "hepatic_comments": forms.Textarea(
                attrs={"class": "form-control d-none", "id": "hepatic_comments"}
            ),
        }


class FormulationForm(forms.ModelForm):
    class Meta:
        model = Formulation
        fields = "__all__"


class IndicationForm(forms.ModelForm):
    class Meta:
        model = Indication
        fields = "__all__"
