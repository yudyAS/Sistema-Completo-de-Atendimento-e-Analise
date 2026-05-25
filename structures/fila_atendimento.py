from collections import deque
from typing import Deque, List, Optional


class FilaAtendimento:
    """Gerencia as filas comum e de prioridade."""

    def __init__(self):
        self.prioridade: Deque[int] = deque()
        self.normal: Deque[int] = deque()

    def adicionar(self, cliente_id: int, prioridade: bool) -> None:
        """Coloca um cliente na fila correta mantendo ordem de chegada."""
        if prioridade:
            self.prioridade.append(cliente_id)
        else:
            self.normal.append(cliente_id)

    def proximo(self) -> Optional[int]:
        """Retira o próximo cliente da fila, dando preferência à prioridade."""
        if self.prioridade:
            return self.prioridade.popleft()
        if self.normal:
            return self.normal.popleft()
        return None

    def esta_vazia(self) -> bool:
        """Verifica se as duas filas estão vazias."""
        return not self.prioridade and not self.normal

    def listar_ordem(self) -> List[int]:
        """Retorna os IDs na ordem atual de atendimento."""
        return list(self.prioridade) + list(self.normal)
