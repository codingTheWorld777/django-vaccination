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

    @staticmethod
    def getOne(centre_id):
        sql_command = "SELECT * FROM centre WHERE id=%s"
        # with connection.cursor() as cursor:
        #     cursor.execute(sql_command, [centre_label, centre_adresse])
        #     centre_info = cursor.fetchall()
        #     print(centre_info)
        #     return centre_info
        centre_info = ModelCentre.objects.raw(sql_command, [centre_id])
        print(centre_info)
        return centre_info

        
    @staticmethod
    def insert(centre_label, centre_adresse):
        sql_idMax = "SELECT MAX(id) FROM centre"
        with connection.cursor() as cursor:
            cursor.execute(sql_idMax)
            idMax = int(cursor.fetchone()[0]) + 1

        with connection.cursor() as cursor:
            sql_command = "INSERT INTO centre VALUE (%s, %s, %s);"
            cursor.execute(sql_command, [idMax, centre_label, centre_adresse])

        return idMax

    @staticmethod
    def deleteId(id):
        # Suppression d'un centre dans la table stock quand on supprime d'un vaccin
        # throw une erreur s'il y aucun centre avec ce centre_id dans le stock...
        sql_command = "DELETE FROM stock WHERE stock.centre_id=%s";
        with connection.cursor() as cursor:
            cursor.execute(sql_command, [id])
        
        # la même erreur qu'avant (dans la table rendezvous)
        sql_command = "DELETE FROM rendezvous WHERE rendezvous.centre_id=%s";
        with connection.cursor() as cursor:
            cursor.execute(sql_command, [id])
        
        sql_command = "DELETE FROM centre WHERE id=%s";
        with connection.cursor() as cursor:
            cursor.execute(sql_command, [id])
  
        return id;


    class Meta:
        db_table = "centre"

