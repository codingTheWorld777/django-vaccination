from django.db import connection
from django.db import models

# Create your models here.
class ModelCentre(models.Model):
    label = models.CharField(max_length=70)
    adresse = models.CharField(max_length=70)

    @staticmethod
    def getAll():
        sql_command = "SELECT * FROM centre"
        centre_rows = ModelCentre.objects.raw(sql_command)
        return centre_rows

    class Meta:
        db_table = "centre"

