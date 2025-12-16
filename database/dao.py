from database.DB_connect import DBConnect
from model.cromosoma import Cromosoma
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
    def get_nodes() -> list[Cromosoma] | None:
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None
        cursor = cnx.cursor(dictionary=True)
        query = ("""SELECT cromosoma
                    FROM gene g 
                    WHERE g.cromosoma != 0""")
        try:
            cursor.execute(query)
            for row in cursor:
                cromosoma = Cromosoma(**row)
                result.append(cromosoma)

        except Exception as e:
            print(f"Errore durante la query: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_geni_connessi() -> list[Interazione] | None:
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None
        cursor = cnx.cursor(dictionary=True)
        query = ("""SELECT g1.id AS gene1, g2.id AS gene2, correlazione c
                    "FROM  gene g1, gene g2,  interazione i
                    WHERE i.id_gene1 = g1.id AND i.id_gene2 = g2.id AND g1.cromosoma != g2.cromosoma AND g1.cromosoma > 0 AND g2.cromosoma > 0
                    GROUP BY g1.id, g2.id""")
        try:
            cursor.execute(query)
            for row in cursor:
                interazione = Interazione(**row)
                result.append(interazione)

        except Exception as e:
            print(f"Errore durante la query: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result


