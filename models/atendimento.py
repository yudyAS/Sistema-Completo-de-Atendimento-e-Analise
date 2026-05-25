from dataclasses import dataclass


@dataclass
class Atendimento:
    """Representa um atendimento finalizado."""
    cliente_id: int
    atendente_id: int
    data: str
    duracao_minutos: int

    def to_dict(self) -> dict:
        """Converte o atendimento para um dicionário serializável."""
        return {
            "cliente_id": self.cliente_id,
            "atendente_id": self.atendente_id,
            "data": self.data,
            "duracao_minutos": self.duracao_minutos,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Atendimento":
        """Cria um atendimento a partir de um dicionário."""
        return cls(
            cliente_id=int(data["cliente_id"]),
            atendente_id=int(data["atendente_id"]),
            data=data["data"],
            duracao_minutos=int(data["duracao_minutos"]),
        )
