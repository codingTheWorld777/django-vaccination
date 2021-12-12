from django.db import connection
from django.db import models
from django.db.models.fields import CharField

# Create your models here.


class ModelVaccin(models.Model):
    label = models.CharField(max_length=70)
    doses = models.IntegerField()

    @staticmethod
    def getOne(label):
        sql_command = "SELECT * FROM vaccin WHERE label=%s;"
        vaccin_rows = ModelVaccin.objects.raw(sql_command, [label])
        return vaccin_rows

    @staticmethod
    def getAll():
        sql_command = "SELECT * FROM vaccin"
        vaccin_rows = ModelVaccin.objects.raw(sql_command)
        return vaccin_rows

    @staticmethod
    def getAllLabel():
        sql_command = "SELECT label from vaccin"
        with connection.cursor() as cursor:
            cursor.execute(sql_command)
            label_list = cursor.fetchall()


    @staticmethod
    def insert(label, doses):
        sql_idMax = "SELECT MAX(id) FROM vaccin"
        with connection.cursor() as cursor:
            cursor.execute(sql_idMax)
            idMax = int(cursor.fetchone()[0]) + 1

        with connection.cursor() as cursor:
            sql_command = "INSERT INTO vaccin VALUE (%s, %s, %s);"
            cursor.execute(sql_command, [idMax, label, doses])

        # vaccin_inserted = ModelVaccin.objects.raw(sql_command, [idMax, label, doses])
        return idMax

    @staticmethod
    def deleteLabel(vaccin_label):
        sql_command = "DELETE FROM vaccin WHERE label=%s"
        with connection.cursor() as cursor:
            cursor.execute(sql_command, [vaccin_label])
        
        # Update list of vaccins
        sql_command = "SELECT * FROM vaccin"
        with connection.cursor() as cursor:
            cursor.execute(sql_command)
            vaccin_info = cursor.fetchall()
            print(vaccin_info)
            return vaccin_info

    @staticmethod
    def updateDose(vaccin_label, quantite):
        sql_command = "SELECT doses FROM vaccin WHERE label=%s"
        with connection.cursor() as cursor:
            cursor.execute(sql_command, [vaccin_label])
            result = cursor.fetchone()[0]
            doses = int(quantite) + int(result)
            print("doses", doses)

        sql_command = "UPDATE vaccin SET doses=%s WHERE label=%s"
        with connection.cursor() as cursor:
            cursor.execute(sql_command, [doses, vaccin_label])

    class Meta:
        db_table = "vaccin"