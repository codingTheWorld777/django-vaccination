from django.db import connection
from django.db import models

# Create your models here.

class ModelStock(models.Model):

    @staticmethod
    def getDosesByVaccinByCenter():
        try:
            sql_command = "SELECT vaccin.label as vaccin_label, centre.label as centre_label, centre.adresse as centre_adresse, stock.quantite as doses FROM vaccin JOIN stock ON vaccin.id = stock.vaccin_id JOIN centre ON centre.id = stock.centre_id"
            with connection.cursor() as cursor:
                cursor.execute(sql_command)
                results = cursor.fetchall()

            return results
        except Exception:
            print("ERROR")
            return None

    @staticmethod
    def getStockCentre():
        try:
            sql_command = "SELECT DISTINCT centre.label, centre.adresse FROM centre JOIN stock ON centre.id = stock.centre_id"
            with connection.cursor() as cursor:
                cursor.execute(sql_command)
                results = cursor.fetchall()

                return results
        except Exception:
            print("ERROR")
            return None
        
    @staticmethod
    def getCenterAndDose():
        try: 
            stockCenters = ModelStock.getStockCentre()
            numberOfDosesByCenter = []
            results = dict()
            
            for centre in stockCenters:
                label = centre[0]
                adresse = centre[1]
                
                sql_command = "SELECT SUM(stock.quantite) as quantite FROM centre JOIN stock ON centre.id = stock.centre_id WHERE centre.label=%s AND centre.adresse=%s"
                with connection.cursor() as cursor:
                    cursor.execute(sql_command, [label, adresse])
                    rows = cursor.fetchall()

                quantity = rows[0][0]
                numberOfDosesByCenter.append(quantity)
                results[quantity] = centre

            return {'results': results, "numberOfDosesByCenter": numberOfDosesByCenter}
        except Exception:
            print("ERROR")
            return {'results': None, "numberOfDosesByCenter": None}


    @staticmethod
    def attributeVaccin():
        try:
            results = dict()
            
            sql_command = "SELECT centre.label as centre_label, centre.adresse as centre_adresse FROM centre"
            with connection.cursor() as cursor:
                cursor.execute(sql_command)
                results['centre'] = cursor.fetchall()
            
            sql_command = "SELECT vaccin.label as vaccin_label FROM vaccin"
            with connection.cursor() as cursor:
                cursor.execute(sql_command)
                results['vaccin'] = cursor.fetchall()
            
            print("result", results)
            return results
        except Exception:
            print("ERROR")
            return None


    @staticmethod
    def addVaccin(centre_label, centre_adresse, vaccin_label, vaccin_add):
        try:
            # On a besoin de centre_id et de vaccin_id pour pouvoir modifier la table 'stock'
            # 1) Si le centre ou le vaccin n'est pas dans le stock, il faut insérer un nouveau stock 
            # avec centre_id = max(centre_id) + 1, le même pour vaccin_id
            # 2) Sinon, on a le centre_id et le vaccin_id dans le stock pour le modifier...
            
            # -> check 'centre_id'
            sql_command = "SELECT DISTINCT stock.centre_id FROM centre JOIN stock ON centre.id = stock.centre_id WHERE centre.label=%s AND centre.adresse=%s"
            with connection.cursor() as cursor:
                cursor.execute(sql_command, [centre_label, centre_adresse])
                centre_id = cursor.fetchall()
            if len(centre_id) > 0:
                centre_id = centre_id[0][0]
                print(centre_id, "HERE")
            else:
                sql_command = "SELECT centre.id as centre_id from centre WHERE centre.label=%s AND centre.adresse=%s"
                with connection.cursor() as cursor:
                    cursor.execute(sql_command, [centre_label, centre_adresse])
                    centre_id = cursor.fetchall()[0][0]
            print("centre_id :", centre_id)

            # -> check 'vaccin_id'
            sql_command = "SELECT DISTINCT stock.vaccin_id FROM vaccin JOIN stock ON vaccin.id = stock.vaccin_id WHERE vaccin.label=%s"
            with connection.cursor() as cursor:
                cursor.execute(sql_command, [vaccin_label])
                vaccin_id = cursor.fetchall()
                print(len(vaccin_id), "len(vaccin_id) IS HERE")
            if len(vaccin_id) > 0:
                vaccin_id = vaccin_id[0][0]
                print("THERE", vaccin_id)
            else:
                sql_command = "SELECT vaccin.id as vaccin_id from vaccin WHERE vaccin.label=%s"
                with connection.cursor() as cursor:
                    cursor.execute(sql_command, [vaccin_label])
                    vaccin_id = cursor.fetchall()[0][0]
                    print("OUI", vaccin_id)
            print("vaccin_id :", vaccin_id)
            
            # Après avoir pris le centre_id et le vaccin_id, on veut prendre la quantité des doses d'un vaccin dans le stock
            # 1) Si le centre_id ou le vaccin_id (ou les deux) n'est pas dans le stock, on met stock.quantite = 0
            # 2) Sinon, on ajoute le vaccin_add dans le stock(centre_id, vaccin_id) et on met à jour le stock
            sql_command = "SELECT stock.quantite as quantite FROM stock WHERE stock.centre_id=%s AND stock.vaccin_id=%s"
            with connection.cursor() as cursor:
                cursor.execute(sql_command, [centre_id, vaccin_id])
                quantite = cursor.fetchall()
            # 1)
            if len(quantite) > 0:
                quantite = quantite[0][0]
                quantite = int(quantite) + int(vaccin_add)
                print("quantite", quantite)
                # sql_command = "UPDATE stock SET stock.quantite = 'quantite' WHERE stock.centre_id = 'centre_id' AND stock.vaccin_id = 'vaccin_id'"
                sql_command = "UPDATE stock SET stock.quantite=%s WHERE stock.centre_id=%s AND stock.vaccin_id=%s"
                with connection.cursor() as cursor:
                    cursor.execute(sql_command, [quantite, centre_id, vaccin_id])
                    print("UPDATE")
            # 2)
            else:
                quantite = vaccin_add
                sql_command = "INSERT INTO stock VALUES (%s, %s, %s)"
                with connection.cursor() as cursor:
                    cursor.execute(sql_command, [centre_id, vaccin_id, quantite])
                    print("INSERT")
            
            return {"centre_label" : centre_label, "centre_adresse" : centre_adresse, "vaccin_label" : vaccin_label, 
                        "vaccin_add" : vaccin_add, "quantite" : quantite} 
        except Exception:
            print("ERROR")
            return -1

    @staticmethod
    def getCentreId(centre_label, centre_adresse):
        try:
            sql_command = "SELECT id FROM centre WHERE label=%s AND adresse=%s"
            with connection.cursor() as cursor:
                cursor.execute(sql_command, [centre_label, centre_adresse])
                results = cursor.fetchall()[0][0]

                return results
        except Exception:
            print("ERROR")
            return None

    @staticmethod
    def getVaccinId(vaccin_label):
        try:
            sql_command = "SELECT id FROM vaccin WHERE label=%s"
            with connection.cursor() as cursor:
                cursor.execute(sql_command, [vaccin_label])
                results = cursor.fetchall()[0][0]

            return results
        except Exception:
            print("ERROR")
            return None

    
    @staticmethod
    def deleteStock(centre_id, vaccin_id):
        try:
            sql_command = "DELETE FROM rendezvous WHERE rendezvous.centre_id=%s AND rendezvous.vaccin_id=%s"
            with connection.cursor() as cursor:
                cursor.execute(sql_command, [centre_id, vaccin_id])
            
            sql_command = "DELETE FROM stock WHERE stock.centre_id=%s AND stock.vaccin_id=%s"
            with connection.cursor() as cursor:
                cursor.execute(sql_command, [centre_id, vaccin_id])

            return True
        except Exception:
            print("ERROR")
            return None

    class Meta:
        db_table = "stock"
