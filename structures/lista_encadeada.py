from typing import Optional, List
from models.client import Cliente


class Node:
    """Nó simples para lista encadeada."""

    def __init__(self, cliente: Cliente, proximo: "Optional[Node]" = None):
        self.cliente = cliente
        self.proximo = proximo


class ListaEncadeada:
    """Lista encadeada de clientes ativos."""

    def __init__(self):
        self.cabeca: Optional[Node] = None

    def inserir(self, cliente: Cliente) -> None:
        """Insere cliente no início da lista encadeada."""
        self.cabeca = Node(cliente, self.cabeca)

    def buscar_por_id(self, cliente_id: int) -> Optional[Cliente]:
        """Busca cliente por id caminhando na lista."""
        atual = self.cabeca
        while atual is not None:
            if atual.cliente.id == cliente_id:
                return atual.cliente
            atual = atual.proximo
        return None

    def remover_por_id(self, cliente_id: int) -> bool:
        """Remove cliente da lista se existir e retorna True."""
        atual = self.cabeca
        anterior = None
        while atual is not None:
            if atual.cliente.id == cliente_id:
                if anterior is None:
                    self.cabeca = atual.proximo
                else:
                    anterior.proximo = atual.proximo
                return True
            anterior = atual
            atual = atual.proximo
        return False

    def listar(self) -> List[Cliente]:
        """Retorna todos os clientes presentes na lista."""
        resultado: List[Cliente] = []
        atual = self.cabeca
        while atual is not None:
            resultado.append(atual.cliente)
            atual = atual.proximo
        return resultado
