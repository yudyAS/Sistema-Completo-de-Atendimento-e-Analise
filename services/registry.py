from typing import List, Optional

from models.atendente import Atendente
from models.client import Cliente
from storage.persistence import (
    load_atendentes,
    load_clients,
    save_atendentes,
    save_clients,
)
from structures.lista_encadeada import ListaEncadeada


class SistemaCadastro:
    """Responsável por cadastro, busca e persistência de clientes e atendentes."""

    def __init__(self):
        self.clientes_temp: List[Cliente] = []
        self.clientes_ordenados: List[Cliente] = []
        self.clientes_ativos = ListaEncadeada()
        self.atendentes: List[Atendente] = []
        self.carregar_dados()

    def carregar_dados(self) -> None:
        """Carrega dados salvos em arquivo e inicializa estruturas.

        O vetor ordenado é usado para busca binária por id. A lista encadeada
        mantém clientes ativos de forma separada.
        """
        self.clientes_temp = load_clients()
        self.clientes_ordenados = list(self.clientes_temp)
        self._ordenar_clientes_por_id()
        self.clientes_ativos = ListaEncadeada()
        for cliente in self.clientes_ordenados:
            if cliente.ativo:
                self.clientes_ativos.inserir(cliente)

        self.atendentes = load_atendentes()

    def salvar_dados(self) -> None:
        """Salva clientes e atendentes em arquivo."""
        save_clients(self.clientes_ordenados)
        save_atendentes(self.atendentes)

    def adicionar_cliente(
        self,
        cliente_id: int,
        nome: str,
        telefone: str,
        prioridade: bool,
    ) -> Cliente:
        """Adiciona um cliente novo e mantém o vetor ordenado por id."""
        if self.buscar_cliente_por_id(cliente_id) is not None:
            raise ValueError(f"ID {cliente_id} já existe")

        cliente = Cliente(id=cliente_id, nome=nome, telefone=telefone, prioridade=prioridade)
        self.clientes_temp.append(cliente)
        self.clientes_ordenados.append(cliente)
        self._ordenar_clientes_por_id()
        self.clientes_ativos.inserir(cliente)
        self.salvar_dados()
        return cliente

    def adicionar_atendente(self, atendente_id: int, nome: str) -> Atendente:
        """Adiciona um atendente ao sistema."""
        if any(a.id == atendente_id for a in self.atendentes):
            raise ValueError(f"ID {atendente_id} já existe")
        atendente = Atendente(id=atendente_id, nome=nome)
        self.atendentes.append(atendente)
        self.salvar_dados()
        return atendente

    def buscar_cliente_por_id(self, cliente_id: int) -> Optional[Cliente]:
        """Busca cliente no vetor ordenado usando busca binária."""
        esquerda = 0
        direita = len(self.clientes_ordenados) - 1
        while esquerda <= direita:
            meio = (esquerda + direita) // 2
            atual = self.clientes_ordenados[meio]
            if atual.id == cliente_id:
                return atual
            if atual.id < cliente_id:
                esquerda = meio + 1
            else:
                direita = meio - 1
        return None

    def remover_cliente_inativo(self, cliente_id: int) -> bool:
        """Marca cliente como inativo e remove da lista encadeada de ativos."""
        cliente = self.buscar_cliente_por_id(cliente_id)
        if cliente is None:
            raise ValueError(f"Cliente {cliente_id} não encontrado")
        if not cliente.ativo:
            return False

        cliente.ativo = False
        removido = self.clientes_ativos.remover_por_id(cliente_id)
        self.salvar_dados()
        return removido

    def listar_cliente_ativos(self) -> List[Cliente]:
        """Retorna a lista de clientes ativos armazenada na lista encadeada."""
        return self.clientes_ativos.listar()

    def _ordenar_clientes_por_id(self) -> None:
        """Ordena o vetor de clientes por id usando insertion sort.

        Isto garante o vetor ordenado para busca binária rápida.
        """
        for i in range(1, len(self.clientes_ordenados)):
            chave = self.clientes_ordenados[i]
            j = i - 1
            while j >= 0 and self.clientes_ordenados[j].id > chave.id:
                self.clientes_ordenados[j + 1] = self.clientes_ordenados[j]
                j -= 1
            self.clientes_ordenados[j + 1] = chave
