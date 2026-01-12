from dataclasses import dataclass
@dataclass

class Gene:
    id: str
    funzione: str
    essenziale:str
    cromosoma: int

    def __str__(self):
        return f"{self.id}, {self.funzione}, {self.essenziale}, {self.cromosoma}"
    def __repr__(self):
        return f"{self.id}, {self.funzione}, {self.essenziale}, {self.cromosoma}"



