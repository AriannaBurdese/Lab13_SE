from dataclasses import dataclass
@dataclass
class Cromosoma:
    numero: int

    def __str__(self):
        return f"{self.numero}"

    def __repr__(self):
        return f"{self.numero}"
