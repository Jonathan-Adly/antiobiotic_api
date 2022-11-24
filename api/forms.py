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
                attrs={"class": "form-control", "id": "hepatic_comments", "rows": 3}
            ),
            "renal_comments": forms.Textarea(
                attrs={"class": "form-control", "id": "renal_comments", "rows": 3}
            ),
        }


class FormulationForm(forms.ModelForm):
    class Meta:
        model = Formulation
        fields = ["route", "label", "dosage_form", "value"]
        widgets = {
            "route": forms.Select(attrs={"class": "form-select"}),
            "label": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "amoxicillin 250mg/5mL"}
            ),
            "dosage_form": forms.Select(attrs={"class": "form-select"}),
            "value": forms.NumberInput(attrs={"class": "form-control"}),
        }


class IndicationForm(forms.Form):

    #INDICATION_CHOICES = list(
        #Indication.objects.all().values_list(
        #    "pk",
        #    "name",
        #)
    #) + [(0, "Not in this list")]
    INDICATION_CHOICES = [(0, "dasda")]
    DISEASE_CHOICES = [
        ("neuro", "Neuro"),
        ("heent", "HEENT"),
        ("ocular", "Ocular"),
        ("respiratory", "Respiratory"),
        ("gi", "GI"),
        ("genital", "Genital"),
        ("urinary", "Urinary"),
        ("skin/soft tissue", "Skin/Soft Tissue"),
        ("msk", "MSK"),
        ("viral", "Viral"),
        ("sepsis", "Sepsis"),
        ("febrile neutropenia", "Febrile Neutropenia"),
    ]

    indication = forms.ChoiceField(
        choices=INDICATION_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "_": """on change if my.options.selectedIndex is my.options.length-1 
                        remove [@disabled] from #id_indication_name else 
                        add [@disabled] to #id_indication_name""",
            }
        ),
    )

    indication_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "disabled": "true",
            }
        )
    )
    disease_system = forms.ChoiceField(
        choices=DISEASE_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check-input", "type": "radio"}),
    )
    comments = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3})
    )
