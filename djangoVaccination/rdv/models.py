from django.db import connection
from django.db import models

# Create your models here.


class ModelRdv(models.Model):
    # Prendre la liste des rendez-vous
    def getAll():
        try:
            sql_command = "SELECT patient.nom, patient.prenom, centre.label as centre_label, centre.adresse as centre_adresse, rendezvous.injection as injection, vaccin.label as vaccin_label FROM patient JOIN rendezvous ON patient.id = rendezvous.patient_id JOIN centre ON centre.id = rendezvous.centre_id JOIN vaccin ON vaccin.id = rendezvous.vaccin_id ORDER BY rendezvous.patient_id"
            with connection.cursor() as cursor:
                cursor.execute(sql_command)
                results = cursor.fetchall()

                return results
        except Exception:
            print("ERROR")
            return 0


    # Prendre l'injection du patient
    def getInjection(patient_id):
        try:
            sql_command = "SELECT rendezvous.injection as injection FROM rendezvous WHERE rendezvous.patient_id=%s"
            with connection.cursor() as cursor:
                cursor.execute(sql_command, [patient_id])
                results = cursor.fetchall()
                results = results[len(results) - 1][0]
                return results
        except Exception:
            print("ERROR")
            return 0


    # Prendre les infos de patients
    def getPatient():
        try:
            sql_command = "SELECT id, nom, prenom, adresse FROM patient"
            with connection.cursor() as cursor:
                cursor.execute(sql_command)
                results = cursor.fetchall()

                return results
        except Exception:
            print("ERROR")
            return None


    # Proposer le vaccin pour les patients
    def getRdv(patient_id):
        try:
            sql_command = "SELECT patient.nom, patient.prenom, centre.label as centre_label, centre.adresse as centre_adresse, rendezvous.injection as injection, vaccin.label as vaccin_label FROM patient JOIN rendezvous ON patient.id = rendezvous.patient_id JOIN centre ON centre.id = rendezvous.centre_id JOIN vaccin ON vaccin.id = rendezvous.vaccin_id WHERE rendezvous.patient_id=%s ORDER BY rendezvous.injection"
            with connection.cursor() as cursor:
                cursor.execute(sql_command, [patient_id])
                results = cursor.fetchall()

                return results
        except Exception:
            print("ERROR")
            return None


    # Obtenir le nombre des doses d'un type du vaccin
    def getDoseNumberOfVaccin(vaccin_label):
        try:
            sql_command = "SELECT vaccin.doses as doses FROM vaccin WHERE vaccin.label=%s"
            with connection.cursor() as cursor:
                cursor.execute(sql_command, [vaccin_label])
                results = cursor.fetchall()[0][0]

            return results
        except Exception:
            print("ERROR")
            return None


    # Trouver les centres où ils ont au moins une dose de vaccin
    def getActiveDoseFromCenter():
        try:
            sql_command = "SELECT DISTINCT centre.id as centre_id, centre.label as centre_label, centre.adresse as centre_adresse, SUM(stock.quantite) as quantite FROM centre JOIN stock ON centre.id = stock.centre_id GROUP BY centre_id HAVING SUM(stock.quantite) > 0"
            with connection.cursor() as cursor:
                cursor.execute(sql_command)
                activeCenter = cursor.fetchall()

                return activeCenter
        except Exception:
            print("ERROR")
            return None


    # Utilisation: Trouver les centres de vaccination qui ont le vaccine que le patient a été vacciné
    def getCenterByVaccin(vaccin_label):
        try:
            sql_command = "SELECT DISTINCT centre.id as centre_id, centre.label as centre_label, centre.adresse as centre_adresse, SUM(stock.quantite) as quantite FROM centre JOIN stock ON centre.id = stock.centre_id JOIN vaccin ON vaccin.id = stock.vaccin_id WHERE vaccin.label=%s GROUP BY centre_id HAVING SUM(stock.quantite) > 0"
            with connection.cursor() as cursor:
                cursor.execute(sql_command, [vaccin_label])
                activeCenter = cursor.fetchall()

                return activeCenter
        except Exception:
            print("ERROR")
            return None


    # Définir un rendez-vous pour le patient
    def setRdv(centre_id, centre_label, patient_id, injection):
        if len(centre_id) > 0 and len(centre_label) > 0 and len(patient_id) > 0:
            try:
                # 1) Choisir un vaccin dans le centre choisi dont le vaccin de ce type a le nombre des doses le plus grand
                # On l'appelle 'VACCIN_G"
                sql_command = "SELECT MAX(stock.quantite) as quantite FROM stock WHERE stock.centre_id=%s"
                with connection.cursor() as cursor:
                    cursor.execute(sql_command, [centre_id])
                    maxDose = cursor.fetchall()[0][0]

                # 2) On prend les infos du 'VACCIN_G' au centre choisi comme vaccin(id, lour le proposer au patient
                    # 2.1) Si ce patient a déjà un rendez-vous au centre de vaccination, on va trouver le nom du vaccin dans sa première dose
                    # 2.2) Au contraire, on va trouver les centres qui ont le vaccin avec le nombre des doses positif pour ce patient
                    # et on choisi le centre qui a le nombre des doses le plus grand.
                sql_command = "SELECT rendezvous.vaccin_id as vaccin_id FROM rendezvous WHERE rendezvous.patient_id=%s"
                with connection.cursor() as cursor:
                    cursor.execute(sql_command, [patient_id])
                    vaccin_id = cursor.fetchall()

                # **** 2.1) Il y a pas de rendez-vous ****
                vaccinInfo = ''
                if len(vaccin_id) == 0:
                    sql_command = "SELECT vaccin.id as vaccin_id, vaccin.label as vaccin_label, stock.quantite as quantite FROM vaccin JOIN stock ON vaccin.id = stock.vaccin_id WHERE stock.centre_id=%s AND stock.quantite=%s"
                    with connection.cursor() as cursor:
                        cursor.execute(sql_command, [centre_id, maxDose])
                        vaccinInfo = cursor.fetchall()[0]
                        vaccin_id = vaccinInfo[0]
                        print("vaccin_id in stock", vaccin_id)

                # **** 2.2) Au contraire...: ***
                else:
                    vaccin_id = vaccin_id[0][0]

                    sql_command = "SELECT vaccin.id as vaccin_id, vaccin.label as vaccin_label, stock.quantite as quantite FROM vaccin JOIN stock ON vaccin.id = stock.vaccin_id WHERE stock.centre_id=%s AND vaccin.id=%s"
                    with connection.cursor() as cursor:
                        cursor.execute(sql_command, [centre_id, vaccin_id])
                        vaccinInfo = cursor.fetchall()[0]

                # pour savoir le nombre des doses resté d'un vaccin dans un centre
                # s'il y as plus de doses d'un vaccin dans un centre, on va notifier au patient
                # sinon, on va ajouter un rendez-vous pour ce patient et on met à jour le stock
                quantite = int(vaccinInfo[2]) - 1

                # 3) On va ajouter un rendez-vous pour ce e patient est vacciné le vaccin choisi par le système
                # -> le nombre de doses de ce vaccin au centre choisi par le patient est donc le plus grand nombre
                if (quantite >= 0):
                    # sql_command = "INSERT INTO rendezvous values (:centre_id, :patient_id, :injection, :vaccin_id)"
                    sql_command = "INSERT INTO rendezvous values (%s, %s, %s, %s)"
                    with connection.cursor() as cursor:
                        cursor.execute(sql_command, [centre_id, patient_id, injection, vaccin_id])  
                else: 
                    return -1

                # 4) On mis à jour le stock (en decrémentant la quantité des doses de ce 'VACCIN_G'
                sql_command = "UPDATE stock SET stock.quantite=%s WHERE stock.centre_id=%s AND stock.vaccin_id=%s"
                with connection.cursor() as cursor:
                    cursor.execute(sql_command, [quantite, centre_id, vaccin_id])

                results = [centre_label, vaccinInfo[1]]
                return results
            except Exception:
                print("ERROR")
                return None
        else: return None

    # Ajouter vaccins aux centres pour le stock
    def attributeVaccin():
        try:
            results = dict()

            sql_command = "SELECT distinct centre.label as centre_label FROM centre JOIN stock ON centre.id = stock.centre_id"
            with connection.cursor() as cursor:
                cursor.execute(sql_command)
                results['centre'] = cursor.fetchall()

            sql_command = "SELECT distinct vaccin.label as vaccin_label FROM vaccin JOIN stock ON vaccin.id = stock.vaccin_id"
            with connection.cursor() as cursor:
                cursor.execute(sql_command)
                results['vaccin'] = cursor.fetchall()

            return results
        except Exception:
            print("ERROR")
            return None

    class Meta:
        db_table = "rendezvous"
