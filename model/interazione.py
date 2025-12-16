from dataclasses import dataclass
@dataclass
class Interazione:
    id_gene1: str
    id_gene2: str
    tipo: str
    correlazione : float

    def __str__(self):
        return f"{self.id_gene1, self.id_gene2, self.tipo, self.correlazione}"

    def __repr__(self):
        return f"{self.id_gene1, self.id_gene2, self.tipo, self.correlazione}"