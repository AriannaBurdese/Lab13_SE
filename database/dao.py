from database.DB_connect import DBConnect
from model import cromosoma
from model.cromosoma import Cromosoma
from model.gene import Gene
from model.interazione import Interazione


class DAO:

    #@staticmethod
    """def query_esempio():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = SELECT * FROM esempio

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result"""
    @staticmethod
    def get_geni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None
        cursor = cnx.cursor(dictionary=True)
        query = ("""SELECT *
                    FROM gene g 
                    WHERE g.cromosoma != 0""")
        try:
            cursor.execute(query)
            for row in cursor:
                cromosoma = Gene(**row)
                result.append(cromosoma)

        except Exception as e:
            print(f"Errore durante la query: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result
    @staticmethod
    def get_cromosomi(): #sono i miei nodi
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None
        cursor = cnx.cursor(dictionary=True)
        query = ("""SELECT DISTINCT cromosoma
                    FROM gene g 
                    WHERE g.cromosoma > 0""")
        try:
            cursor.execute(query)
            for row in cursor:
                result.append(row['cromosoma'])

        except Exception as e:
            print(f"Errore durante la query: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_geni_connessi(): #prendo tutti i collegamenti dei geni e la correlazione
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None
        cursor = cnx.cursor(dictionary=True)
        query = ("""SELECT g1.id AS gene1, g2.id AS gene2, i.correlazione 
                    FROM  gene g1, gene g2,  interazione i
                    WHERE i.id_gene1 = g1.id AND i.id_gene2 = g2.id  
                        AND g1.cromosoma != g2.cromosoma  
                        AND g1.cromosoma > 0 AND g2.cromosoma > 0
                    GROUP BY g1.id, g2.id""") #il group by mi toglie i duplicati dei geni
                    #WHERE i.id_gene1 = g1.id AND i.id_gene2 = g2.id  mi assicuro che i geni esistano sia nella tabella geni che in quella delle interazioni
                            #AND g1.cromosoma != g2.cromosoma  # cromosoma gene di partenza deve essere diverso da quello di arrivo

        try:
            cursor.execute(query)
            for row in cursor:
                result.append((row['gene1'], row['gene2'], row['correlazione'])) #potevo anche fare un oggetto interazione in cui mettevo tutte le informazioni


        except Exception as e:
            print(f"Errore durante la query: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result


