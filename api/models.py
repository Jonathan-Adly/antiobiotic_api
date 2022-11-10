import itertools
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.template.defaultfilters import slugify
from django.db.models import Q

ORAL = "po"
INTRAVENOUS = "iv"
SUBLINGUAL = "sl"
RECTAL = "pr"
INTRAMUSCULAR = "im"
SUBCUTANEOUS = "sc"
INTRANASAL = "n"
INHALED = "in"
VAGINAL = "pv"
SUSPENSION = "suspension/liquid"
TABLET = "tablet"
CAPSULE = "capsule"
CHEWABLE = "chewable"
SUPPOSITORY = "suppository"


ROUTE_CHOICES = [
    (ORAL, "Oral"),
    (INTRAVENOUS, "IV"),
    (SUBLINGUAL, "Sublingual"),
    (RECTAL, "rectal"),
    (INTRAMUSCULAR, "IM"),
    (SUBCUTANEOUS, "SC"),
    (INTRANASAL, "Intranasal"),
    (INHALED, "Inhaled"),
    (VAGINAL, "Vaginal"),
]
DOSAGE_FORM_CHOICES = [
    (SUSPENSION, "Liquid/Powder for Suspension"),
    (TABLET, "Tablet"),
    (CAPSULE, "Capsule"),
    (CHEWABLE, "Chewable"),
    (SUPPOSITORY, "Suppository"),
    (INTRAVENOUS, "IV"),
    (SUBLINGUAL, "Sublingual"),
    (INTRAMUSCULAR, "IM"),
    (SUBCUTANEOUS, "SC"),
    (INTRANASAL, "Intranasal"),
    (INHALED, "Inhaled"),
    (VAGINAL, "Vaginal"),
]


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    `created_at` and `updated_at` fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Drug(TimeStampedModel):
    drug_name = models.CharField(max_length=100)
    brand_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    is_sulfa = models.BooleanField(default=False)
    is_penicillin = models.BooleanField(default=False)
    is_cephalosporin = models.BooleanField(default=False)
    similar_terms = ArrayField(
        base_field=models.CharField(max_length=100), blank=True, null=True
    )
    is_combo = models.BooleanField(default=False)
    hepatic_adjustment = models.BooleanField(default=False)
    hepatic_comments = models.TextField(blank=True)
    renal_adjustment = models.BooleanField(default=False)
    is_generic = models.BooleanField(default=False)

    @property
    def routes(self):
        f = Formulation.objects.filter(drug=self).values_list("route").distinct()
        return list(itertools.chain.from_iterable(f))

    @property
    def formulationsPO(self):
        f = (
            Formulation.objects.filter(drug=self)
            .filter(Q(route=ORAL) | Q(route=SUBLINGUAL))
            .values("value", "label", "dosage_form")
        )
        return f

    @property
    def formulationsIV(self):
        f = (
            Formulation.objects.filter(drug=self)
            .filter(route=INTRAVENOUS)
            .values("value", "label", "dosage_form")
        )
        return f

    @property
    def formulationsOther(self):
        f = (
            Formulation.objects.filter(drug=self)
            .exclude(Q(route=ORAL) | Q(route=SUBLINGUAL) | Q(route=INTRAVENOUS))
            .values("value", "label", "dosage_form")
        )
        return f

    @property
    def get_indications(self):
        return Indication.objects.filter(drug=self).values(
            "name",
            "disease_system",
            "similar_terms",
            "comments",
            "virus",
            "dosages__route",
            "dosages__weight_based_per_dose",
            "dosages__weight_based_freq",
            "dosages__weight_based_dosing_unit",
            "dosages__duration",
            "dosages__duration_unit",
            "dosages__adult_per_dose",
            "dosages__adult_freq",
            "dosages__adult_dose_unit",
        )

    @property
    def get_renal_dose(self):
        if self.renal_adjustment:
            dosages = RenalDose.objects.filter(indication__drug=self).values(
                "indication__name",
                "crcl_min",
                "crcl_max",
                "route",
                "weight_based_per_dose",
                "weight_based_freq",
                "weight_based_dosing_unit",
                "duration",
                "duration_unit",
                "adult_per_dose",
                "adult_freq",
                "adult_dose_unit",
            )
            return dosages
        else:
            return []

    @property
    def get_bacteria(self):
        return Bacteria.objects.filter(possible_drugs=self).values(
            "possible_indications__name", "name", "group"
        )

    def __str__(self):
        return self.drug_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.drug_name)
        return super().save(*args, **kwargs)


class Formulation(TimeStampedModel):
    drug = models.ForeignKey(
        Drug, related_name="formulations", on_delete=models.CASCADE
    )
    route = models.CharField(max_length=2, choices=ROUTE_CHOICES)
    label = models.CharField(max_length=250)
    dosage_form = models.CharField(max_length=20, choices=DOSAGE_FORM_CHOICES)
    is_pill = models.BooleanField()
    value = models.IntegerField(
        help_text="amount of milligrams per mL for non-pill, or amount of milligrams per pill"
    )

    def __str__(self):
        return f"{self.drug}: {self.label}"


class Indication(TimeStampedModel):
    name = models.CharField(max_length=250)
    drug = models.ForeignKey(Drug, related_name="indications", on_delete=models.CASCADE)
    disease_system = models.CharField(max_length=150)
    similar_terms = ArrayField(
        base_field=models.CharField(max_length=100), blank=True, null=True
    )
    comments = models.TextField(blank=True)
    virus = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.drug} for {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Dosage(TimeStampedModel):
    indication = models.ForeignKey(
        Indication, related_name="dosages", on_delete=models.CASCADE
    )
    route = models.CharField(max_length=2, choices=ROUTE_CHOICES)
    weight_based_per_dose = models.FloatField()  # 25
    weight_based_freq = models.IntegerField(help_text="per day")  # 3
    weight_based_dosing_unit = models.CharField(max_length=50)  # mg/kg
    duration = models.IntegerField()  # 7
    duration_unit = models.CharField(max_length=20)  # days
    adult_per_dose = models.FloatField()  # 500
    adult_freq = models.IntegerField(help_text="per day")  # 3
    adult_dose_unit = models.CharField(max_length=20)  # mg

    def __str__(self):
        # Otitis Media - PO : 25mg/kg 3 times a day for 7 days
        return f"""
        {self.indication} - {self.route}: 
        {self.weight_based_per_dose}{self.weight_based_dosing_unit} {self.weight_based_freq} time/s a day for 
        {self.duration}{self.duration_unit} 
        """


class RenalDose(TimeStampedModel):
    indication = models.ForeignKey(
        Indication, related_name="renal_dosages", on_delete=models.CASCADE
    )
    crcl_min = models.IntegerField()
    crcl_max = models.IntegerField()
    route = models.CharField(max_length=2, choices=ROUTE_CHOICES)
    weight_based_per_dose = models.FloatField()  # 25
    weight_based_freq = models.IntegerField(help_text="per day")  # 3
    weight_based_dosing_unit = models.CharField(max_length=50)  # mg/kg
    duration = models.IntegerField()  # 7
    duration_unit = models.CharField(max_length=20)  # days
    adult_per_dose = models.FloatField()  # 500
    adult_freq = models.IntegerField(help_text="per day")  # 3
    adult_dose_unit = models.CharField(max_length=20)  # mg

    def __str__(self):
        # Otitis Media - PO : 25mg/kg 3 times a day for 7 days
        return f"""
        {self.indication} - {self.route}: 
        {self.weight_based_per_dose}{self.weight_based_dosing_unit} {self.weight_based_freq} time/s a day for 
        {self.duration}{self.duration_unit} 
        """


class Bacteria(TimeStampedModel):
    GRAM_POS = "gram+"
    GRAM_NEG = "gram-"
    ANAEROBIC = "anaerobic"
    GROUP_CHOICE = [
        (GRAM_POS, "gram-positive"),
        (GRAM_NEG, "gram-negative"),
        (ANAEROBIC, "anaerobic"),
    ]

    name = models.CharField(max_length=250, blank=True)
    possible_drugs = models.ManyToManyField(Drug, related_name=("bacteria"))
    possible_indications = models.ManyToManyField(Indication, related_name=("bacteria"))
    group = models.CharField(choices=GROUP_CHOICE, max_length=10)
