import random
from django.db import models


class Field(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def years(self):
        return self.analysis.order_by('-year').values_list('year', flat=True)


class FieldAnalysis(models.Model):
    SOIL_TYPE_CHOICES = (
        (1, 'Loamy'),
        (2, 'Peaty'),
        (3, 'Chalky'),
        (4, 'Clay'),
        (5, 'Silty'),
        (6, 'Sandy')
    )

    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='analysis')
    year = models.IntegerField()

    hectars = models.IntegerField()
    nitrogen = models.IntegerField()
    moisture = models.FloatField()
    soil_type = models.IntegerField(choices=SOIL_TYPE_CHOICES)
    daily_sunlight = models.FloatField()
    avg_temperature = models.FloatField()

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.field.name} - {self.year}'

    def get_results(self):
        res = self.result_set.first()
        if not res is None:
            return res

        rand_pk = random.choice(Crop.objects.values_list('pk', flat=True))
        res = Result.objects.create(
            crop=Crop.objects.get(pk=rand_pk),
            analysis=self,
            income=random.randint(50000, 500000),
            total_yield=random.random() * 100 + 10
        )
        return res



class Crop(models.Model):
    crop_type = models.CharField(max_length=200)
    img = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.crop_type


class Result(models.Model):
    finished = models.BooleanField(default=True)
    crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True)
    income = models.IntegerField()
    total_yield = models.FloatField()
    analysis = models.ForeignKey(FieldAnalysis, on_delete=models.CASCADE)

    @property
    def year(self):
        return self.analysis.year

    @property
    def field(self):
        return self.analysis.field

    def __str__(self):
        return f'Result for {self.field} ({self.year})'


class Monitoring(models.Model):
    NUTRIENT_TYPE_CHOICES = (
        (1, 'Nitrogen'),
        (2, 'Phosphorus'),
        (3, 'Magnesium'),
    )

    REGISTRATION_CHOICES = (
        (1, 'Automatic'),
        (2, 'Manual'),
    )

    nutrient_type = models.IntegerField(
        choices=NUTRIENT_TYPE_CHOICES,
        default=1
    )
    registration_type = models.IntegerField(
        choices=REGISTRATION_CHOICES,
        default=1
    )
    value = models.FloatField()
    date = models.DateTimeField()
    analysis = models.ForeignKey(
        FieldAnalysis,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f'{self.nutrient_type} measurement for {self.analysis.field}'
