import json
from pathlib import Path
from typing import List

from models.atendente import Atendente
from models.client import Cliente
from models.atendimento import Atendimento

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


def _load_json(file_name: str) -> List[dict]:
    """Carrega uma lista de dicionários de um arquivo JSON."""
    caminho = DATA_DIR / file_name
    if not caminho.exists():
        return []
    with caminho.open("r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def _save_json(file_name: str, records: List[dict]) -> None:
    """Salva uma lista de dicionários em um arquivo JSON."""
    caminho = DATA_DIR / file_name
    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(records, arquivo, indent=2, ensure_ascii=False)


def load_clients() -> List[Cliente]:
    """Lê a lista de clientes do armazenamento."""
    return [Cliente.from_dict(item) for item in _load_json("clientes.json")]


def save_clients(clients: List[Cliente]) -> None:
    """Salva a lista de clientes no armazenamento."""
    _save_json("clientes.json", [cliente.to_dict() for cliente in clients])


def load_atendentes() -> List[Atendente]:
    """Lê a lista de atendentes do armazenamento."""
    return [Atendente.from_dict(item) for item in _load_json("atendentes.json")]


def save_atendentes(atendentes: List[Atendente]) -> None:
    """Salva a lista de atendentes no armazenamento."""
    _save_json("atendentes.json", [atendente.to_dict() for atendente in atendentes])


def load_atendimentos() -> List[Atendimento]:
    """Lê o histórico de atendimentos do armazenamento."""
    return [Atendimento.from_dict(item) for item in _load_json("atendimentos.json")]


def save_atendimentos(atendimentos: List[Atendimento]) -> None:
    """Salva o histórico de atendimentos no armazenamento."""
    _save_json("atendimentos.json", [atendimento.to_dict() for atendimento in atendimentos])
