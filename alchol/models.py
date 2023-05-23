from django.db import models


class Alchol(models.Model):
    class Meta:
        db_table = "alchol"
        
    name = models.CharField(max_length=10)
    sorts = [
        ('소주', '소주'),
        ('탁주', '탁주'),
        ('청주', '청주'),
        ('과실주', '과실주'),
        ('증류주', '증류주'),
    ]
    sort = models.CharField(choices=sorts, max_length=3)
    beverage = models.FloatField()
    tastes = [
        ('깔끔한', '깔끔한'),
        ('가벼운', '가벼운'),
        ('향긋한', '향긋한'),
        ('풍부한', '풍부한'),
        ('상큼한', '상큼한'),
        ('달콤한', '달콤한'),
        ('부드러운', '부드러운'),
    ]
    taste = models.CharField(choices=tastes, max_length=4)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.name)