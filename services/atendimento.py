import csv
from collections import Counter
from datetime import datetime
from typing import Dict, List, Optional

from models.atendimento import Atendimento
from services.registry import SistemaCadastro
from storage.persistence import load_atendimentos, save_atendimentos
from structures.fila_atendimento import FilaAtendimento
from structures.pilha import Pilha


class SistemaAtendimento:
    """Regras de negócio para abertura, chamada e finalização de atendimentos."""

    def __init__(self, cadastro: SistemaCadastro):
        self.cadastro = cadastro
        self.fila = FilaAtendimento()
        self.atendimentos_abertos: Dict[int, int] = {}
        self.historico: List[Atendimento] = load_atendimentos()
        self.undo_pilha: Pilha[Atendimento] = Pilha()

    def abrir_atendimento(self, cliente_id: int) -> None:
        """
        Coloca o cliente na fila de atendimento apropriada.

        Complexidade: O(n) no pior caso devido à verificação se o cliente
        já está na fila (lista de IDs retornada por `listar_ordem()`),
        onde n é o número de clientes na fila.
        """
        cliente = self.cadastro.buscar_cliente_por_id(cliente_id)
        if cliente is None:
            raise ValueError(f"Cliente {cliente_id} não encontrado")
        if not cliente.ativo:
            raise ValueError("Não é possível abrir atendimento para cliente inativo.")
        if cliente_id in self.fila.listar_ordem() or cliente_id in self.atendimentos_abertos.values():
            raise ValueError("Cliente já está em atendimento ou na fila.")

        self.fila.adicionar(cliente_id, cliente.prioridade)

    def chamar_proximo(self, atendente_id: int) -> int:
        """
        Seleciona o próximo cliente para o atendente e marca atendimento aberto.

        Complexidade: O(1) para remoção da fila (deque.popleft).
        Verificações adicionais são O(k) onde k é número de atendentes.
        """
        if not any(atendente.id == atendente_id for atendente in self.cadastro.atendentes):
            raise ValueError(f"Atendente {atendente_id} não encontrado")
        if atendente_id in self.atendimentos_abertos:
            raise ValueError("Atendente já possui um atendimento aberto.")
        if self.fila.esta_vazia():
            raise ValueError("Não há clientes na fila.")

        cliente_id = self.fila.proximo()
        if cliente_id is None:
            raise ValueError("Não há clientes na fila.")
        self.atendimentos_abertos[atendente_id] = cliente_id
        return cliente_id

    def finalizar_atendimento(self, atendente_id: int, duracao_minutos: int, data: Optional[str] = None) -> Atendimento:
        """
        Finaliza atendimento aberto e salva no histórico.

        Complexidade: O(1) para remover atendimento aberto e empilhar o registro.
        Salvamento em arquivo é O(m) onde m é o tamanho do histórico.
        """
        if atendente_id not in self.atendimentos_abertos:
            raise ValueError("Atendente não possui atendimento aberto.")
        cliente_id = self.atendimentos_abertos.pop(atendente_id)
        if data is None:
            data = datetime.now().strftime("%Y-%m-%d %H:%M")
        atendimento = Atendimento(
            cliente_id=cliente_id,
            atendente_id=atendente_id,
            data=data,
            duracao_minutos=duracao_minutos,
        )
        self.historico.append(atendimento)
        self.undo_pilha.push(atendimento)
        save_atendimentos(self.historico)
        return atendimento

    def desfazer_ultima_finalizacao(self) -> Atendimento:
        """
        Desfaz a última finalização de atendimento usando pilha.

        Complexidade: O(m) no pior caso para localizar e remover o registro
        do histórico (onde m é o tamanho do histórico), embora o pop da pilha
        seja O(1).
        """
        atendimento = self.undo_pilha.pop()
        if atendimento is None:
            raise ValueError("Não há finalização para desfazer.")

        for i in range(len(self.historico) - 1, -1, -1):
            if self.historico[i] == atendimento:
                self.historico.pop(i)
                save_atendimentos(self.historico)
                cliente = self.cadastro.buscar_cliente_por_id(atendimento.cliente_id)
                if cliente is not None and cliente.ativo:
                    self.fila.adicionar(cliente.id, cliente.prioridade)
                return atendimento

        raise ValueError("Registro de atendimento não encontrado no histórico.")

    def calcular_tempo_medio(self) -> float:
        """
        Calcula tempo médio em minutos de todos os atendimentos do histórico.

        Complexidade: O(m) onde m é a quantidade de atendimentos no histórico.
        """
        if not self.historico:
            return 0.0
        total = sum(item.duracao_minutos for item in self.historico)
        return total / len(self.historico)

    def listar_historico_cliente(self, cliente_id: int) -> List[Atendimento]:
        """
        Retorna histórico de atendimentos de um cliente específico.

        Complexidade: O(m) onde m é o tamanho do histórico.
        """
        return [item for item in self.historico if item.cliente_id == cliente_id]

    def listar_atendimentos_por_data(self, data: str) -> List[Atendimento]:
        """
        Retorna atendimentos de uma data específica (formato YYYY-MM-DD).

        Complexidade: O(m) onde m é o número de atendimentos no histórico.
        """
        prefix = data
        return [a for a in self.historico if a.data.startswith(prefix)]

    def top_clientes_atendidos(self, limite: int = 5) -> List[tuple]:
        """
        Retorna os clientes mais atendidos, em ordem decrescente.

        Complexidade: O(m + k log k) onde m é número de atendimentos e
        k é número de clientes distintos no histórico.
        """
        contagem = Counter(a.cliente_id for a in self.historico)
        top = contagem.most_common(limite)
        resultado = []
        for cliente_id, qtd in top:
            cliente = self.cadastro.buscar_cliente_por_id(cliente_id)
            nome = cliente.nome if cliente else "<desconhecido>"
            resultado.append((cliente_id, nome, qtd))
        return resultado

    def verificar_alertas_fila(self, limite_minutos: int = 30) -> List[str]:
        """
        Verifica alertas básicos sobre a fila e tempo de atendimento.

        Complexidade: O(m) onde m é o número de atendimentos considerados.
        """
        alertas: List[str] = []
        # Alerta simples baseado na média dos últimos 10 atendimentos
        recentes = self.historico[-10:]
        if recentes:
            media_recentes = sum(a.duracao_minutos for a in recentes) / len(recentes)
            if media_recentes > limite_minutos:
                alertas.append(f"ALERTA: tempo médio recente ({media_recentes:.1f} min) > {limite_minutos} min")

        # Alerta por tamanho da fila
        tamanho_fila = len(self.fila.listar_ordem())
        if tamanho_fila > 10:
            alertas.append(f"ALERTA: fila com {tamanho_fila} clientes (alto volume)")

        return alertas

    def exportar_relatorio_csv(self, caminho: str) -> None:
        """Gera arquivo CSV com o histórico de atendimentos."""
        with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(["cliente_id", "atendente_id", "data", "duracao_minutos"])
            for item in self.historico:
                writer.writerow([item.cliente_id, item.atendente_id, item.data, item.duracao_minutos])
