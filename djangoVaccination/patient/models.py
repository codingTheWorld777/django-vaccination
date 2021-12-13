from django.db import connection
from django.db import models

# Create your models here.
class ModelPatient(models.Model):
    nom = models.CharField(max_length=40)
    prenom = models.CharField(max_length=40)
    adresse = models.CharField(max_length=80)

    @staticmethod
    def getAll():
        sql_command = "SELECT * FROM patient"
        patient_rows = ModelPatient.objects.raw(sql_command)
        return patient_rows

    @staticmethod
    def getAllId():
        try:
            sql_command = "SELECT * FROM patient ORDER BY id"
            patient_rows = ModelPatient.objects.raw(sql_command)
            return patient_rows
        except Exception:
            return None

    @staticmethod
    def getOne(patient_id):
        try:
            sql_command = "SELECT * FROM patient WHERE id=%s"
            patient_rows = ModelPatient.objects.raw(sql_command, [patient_id])
            return patient_rows
        except Exception:
            return None

    @staticmethod
    def insert(patient_nom, patient_prenom, patient_adresse):
        sql_idMax = "SELECT MAX(id) FROM patient"
        with connection.cursor() as cursor:
            cursor.execute(sql_idMax)
            idMax = int(cursor.fetchone()[0]) + 1

        with connection.cursor() as cursor:
            sql_command = "INSERT INTO patient VALUE (%s, %s, %s, %s);"
            cursor.execute(sql_command, [idMax, patient_nom, patient_prenom, patient_adresse])

        # vaccin_inserted = ModelVaccin.objects.raw(sql_command, [idMax, label, doses])
        return idMax

    @staticmethod
    def patientReadDistinct():
        try:
            sql_commande = "SELECT DISTINCT adresse FROM patient"
            with connection.cursor() as cursor:
                cursor.execute(sql_commande)
                patient_rows = cursor.fetchall()
                return patient_rows
        except Exception:
            return None

    @staticmethod
    def getPatientQuantityByAddress():
        try:
            distinct_adresses = ModelPatient.patientReadDistinct()
            quantity_by_adresse = []
            result = []

            for adresse in distinct_adresses:
                sql_command = "SELECT COUNT(adresse) AS quantite FROM patient WHERE adresse=%s"
                with connection.cursor() as cursor:
                    cursor.execute(sql_command, [adresse])
                    quantity = cursor.fetchall()[0][0]
                    quantity_by_adresse.append(quantity)
                    result.append({'adresse': adresse, 'quantity': quantity})

            return {"adresse_info": result, "quantity": quantity_by_adresse}
        except Exception:
            return None

    @staticmethod
    def deleteId(patient_id):
        try:
            # Supprimer un patient dans la table rendezvous (s'il y existe)
            sql_command = "DELETE FROM rendezvous WHERE patient_id = %s"
            with connection.cursor() as cursor:
                cursor.execute(sql_command, [patient_id])
            
            # Supprimer un patient dans la table patient 
            sql_command = "DELETE FROM patient WHERE id = %s"
            with connection.cursor() as cursor:
                cursor.execute(sql_command, [patient_id])
            
            return patient_id;
        except Exception:
            print("ERROR")
            return None;
        

    class Meta:
        db_table = "patient"
