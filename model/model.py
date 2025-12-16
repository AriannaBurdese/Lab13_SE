import networkx as nx

from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.DiGraph()
        self._id_map = {}

    def build_graph(self):
        self.G.clear()
        lista_nodi = DAO.get_nodes()



