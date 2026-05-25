from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class Pilha(Generic[T]):
    """Pilha simples para desfazer a última ação."""

    def __init__(self):
        self.itens: List[T] = []

    def push(self, item: T) -> None:
        """Empilha um item na pilha."""
        self.itens.append(item)

    def pop(self) -> Optional[T]:
        """Desempilha e retorna o item do topo."""
        if self.esta_vazia():
            return None
        return self.itens.pop()

    def topo(self) -> Optional[T]:
        """Retorna o item do topo sem remover."""
        if self.esta_vazia():
            return None
        return self.itens[-1]

    def esta_vazia(self) -> bool:
        """Verifica se a pilha está vazia."""
        return len(self.itens) == 0
