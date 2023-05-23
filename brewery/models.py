from django.db import models
from alchol.models import Alchol


class Brewery(models.Model):
    class Meta:
        db_table = "brewery"

    alchol = models.ForeignKey(Alchol, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=20)
    region = models.CharField(max_length=10)
    restaurant = models.BooleanField()
    business_hour = models.TimeField(null=True, blank=True)
    experience = models.BooleanField()
    experience_hour = models.TimeField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.name)