from dataclasses import dataclass


@dataclass
class Atendente:
    """Representa um atendente do sistema."""
    id: int
    nome: str

    def to_dict(self) -> dict:
        """Converte o atendente para um dicionário serializável."""
        return {"id": self.id, "nome": self.nome}

    @classmethod
    def from_dict(cls, data: dict) -> "Atendente":
        """Cria um atendente a partir de um dicionário."""
        return cls(id=int(data["id"]), nome=data["nome"])
