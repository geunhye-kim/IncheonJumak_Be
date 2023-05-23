from django.db import models
from alchol.models import Alchol


class Event(models.Model):
    class Meta:
        db_table = "event"

    alchol = models.ForeignKey(Alchol, on_delete=models.DO_NOTHING)
    eventname = models.CharField(max_length=30)
    region = models.CharField(max_length=10)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()

    def __str__(self):
        return str(self.eventname)