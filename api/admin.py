from django.contrib import admin
from . import models
from nested_inline.admin import NestedStackedInline, NestedModelAdmin


class FormulationInline(NestedStackedInline):
    model = models.Formulation
    extra = 1


class DosageInline(NestedStackedInline):  # level two
    model = models.Dosage
    fk_name = "indication"
    extra = 1


class IndicationInline(NestedStackedInline):  # level one
    model = models.Indication
    extra = 1
    fk_name = "drug"
    inlines = [DosageInline]


class DrugAdmin(NestedModelAdmin):  # top level
    prepopulated_fields = {"slug": ("drug_name",)}
    inlines = [FormulationInline, IndicationInline]


admin.site.register(models.Drug, DrugAdmin)
admin.site.register(models.Formulation)
admin.site.register(models.Indication)
admin.site.register(models.Dosage)

admin.site.register(models.Bacteria)
