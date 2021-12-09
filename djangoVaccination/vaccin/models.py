from django.db import models, connections
from django.db.models.fields import CharField

# Create your models here.
class ModelVaccin(models.Model):
    label = models.CharField(max_length=70)
    doses = models.IntegerField()

    class Meta:
        db_table = "vaccin"