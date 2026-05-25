from dataclasses import dataclass


@dataclass
class Cliente:
    """Representa um cliente do sistema."""
    id: int
    nome: str
    telefone: str
    prioridade: bool
    ativo: bool = True

    def to_dict(self) -> dict:
        """Converte o cliente para um dicionário serializável."""
        return {
            "id": self.id,
            "nome": self.nome,
            "telefone": self.telefone,
            "prioridade": self.prioridade,
            "ativo": self.ativo,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Cliente":
        """Cria um cliente a partir de um dicionário."""
        return cls(
            id=int(data["id"]),
            nome=data["nome"],
            telefone=data["telefone"],
            prioridade=bool(data["prioridade"]),
            ativo=bool(data.get("ativo", True)),
        )
