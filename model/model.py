import networkx as nx

from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.DiGraph()
        #mi creo delle liste vuote che dopo vado a riempire
        self._nodes = [] #lista vuota di nodi
        self._edges = [] #lista vuota di archi

        self.id_map = {} #mi creo una mappa vuota
        self.soluzione_best = [] #mi servirà per la ricorsione

        #elementi usati nel dao
        self._lista_cromosomi = []
        self._lista_geni = []
        self._lista_geni_connessi = []

        self.load_geni()
        self.load_cromosomi()
        self.load_geni_connessi()

    def load_cromosomi(self):
        self._lista_cromosomi= DAO.get_cromosomi()

    def load_geni(self):
        self._lista_geni = DAO.get_geni()
        self.id_map = {} #mi serve per collegare il gene al suo cromosoma, dizionario con chiave id gene e valore cromosoma
        for g in self._lista_geni:
            self.id_map[g.id] = g.cromosoma

    def load_geni_connessi(self): #mi carico le connessioni (lista di 3, id gene1, id gene2, correlazione)
        self._lista_geni_connessi = DAO.get_geni_connessi()


    def build_graph(self):
        self.G.clear()
        #di nuovo liste vuote
        self._nodes = []
        self._edges = []
        #vado a riempirmi e crearmi i miei nodi
        for cromosoma in self._lista_cromosomi:
            self._nodes.append(cromosoma)
        self.G.add_nodes_from(self._nodes) #add_nodes_from è un metodo per creare nodi del grafo
        #creazione archi, archi tra i cromosomi, non i geni. I collegamenti tra i geni definivano il peso dell'arco
        edges = {} #dizionario vuoto,. chiave coppia di cromosomi, valore peso
        for g1, g2 ,correlazione in self._lista_geni_connessi:
            #devo calcolare peso di ogni arco
            #uso dizionario id_map con chiave id gene e valore il mio cromosoma
            if (self.id_map[g1], self.id_map[g2]) not in edges: #mi assicuro che la coppia di cromosomi non esista gia nel dizionario
                edges[(self.id_map[g1], self.id_map[g2])] = float(correlazione) #vado a porre come valore il mio peso
            else:
                edges[(self.id_map[g1], self.id_map[g2])] += float(correlazione) #altrimenti sommo e accresco la mia correlazione, il mio valore del peso
        for k,v in edges.items(): #k sono le chiavi, v valori
            self._edges.append((k[0],k[1], v)) #k[0] cromosoma di partenza, [k1] crom di arrivo, v peso
            self.G.add_weighted_edges_from(self._edges) #mi creo tutti gli edges pesati

    def ricerca_cammino(self, t): #t = soglia
        self.soluzione_best.clear()

        for n in self.get_nodes(): #prendo tutti i nodi che ho, il mio punto di partenza
                                   #devo valutare tutte le possibili soluzioni tanti possibili nodi di partenza, con ogni soluzione parte da un nodo diverso
                                   #ciclo for ogni volta parte da un nodo diverso, albero: punti iniziali dei miei rami
            partial = [] #lista parziale di nodi vuota
            partial_edges = [] #lista parziale di edges vuota
            partial.append(n)
            self.ricorsione(partial, partial_edges, t)
        print("final", len(self.soluzione_best), [i[2]["weight"] for i in self.soluzione_best])
    def ricorsione(self, partial_nodes, partial_edges, t):
        n_last = partial_nodes[-1]#vado a prendere ultimo nodo
        neigh = self._get_admissible_neighbors(n_last, partial_edges,t) #ottengo tutti i possibili nodi vicini

        #stop
        if len(neigh) == 0: #ho visitato tutti i vicini
            #faccio verifiche per assicurarmi che sia la soluzione migliore
            weight_path = self.compute_weight_path(partial_edges)
            weight_path_best = self.compute_weight_path(self.soluzione_best)
            if weight_path > weight_path_best:
                self.soluzione_best = partial_edges[:]
            #dopo che ho trovato soluzione migliore, faccio return
            return

        for n in neigh:
            print("...")
            partial_nodes.append(n)
            partial_edges.append((n_last, n, self.G.get_edge_data(n_last, n)))
            self.ricorsione(partial_nodes, partial_edges, t)
            #back
            partial_nodes.pop()
            partial_edges.pop()

    def _get_admissible_neighbors(self, node,  partial_edges, soglia):
        result = [] #lista vuota
        for u,v, data in self.G.out_edges(node, data = True): #u = nodo di partenza, v= nodo di arrivo, data = peso
            if data["weight"] > soglia: #data["weight"] è dizionario
                #controllo solo l'arco diretto
                if (u,v) not in [(x[0], x[1]) for x in partial_edges]: #controllo che l'edge non sia gia nella mia partial edges
                    result.append(v)
        return result

    def compute_weight_path(self, mylist):
        weight = 0
        for e in mylist:
            weight += e[2]['weight']
        return weight

    def count_edges(self, t):
        count_bigger = 0
        count_smaller = 0
        for x in self.get_edges():
            if x[2]['weight'] > t:
                count_bigger += 1
            elif x[2]['weight'] < t:
                count_smaller += 1
        return count_bigger, count_smaller

    def get_nodes(self):
        return self.G.nodes()
    def get_edges(self):
        return self.G.edges(data = True)

    def get_num_of_nodes(self):
        return self.G.number_of_nodes()
    def get_num_of_edges(self):
        return self.G.number_of_edges()
    def get_min_weight(self):
        return min([x[2]["weight"] for x in self.get_edges()])
    def get_max_weight(self):
        return max([x[2]["weight"] for x in self.get_edges()])



















