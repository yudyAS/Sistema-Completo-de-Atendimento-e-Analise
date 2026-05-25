import os
import shutil

from services.registry import SistemaCadastro
from storage.persistence import DATA_DIR


def setup_function() -> None:
    """Prepara ambiente de teste removendo arquivos de dados temporários."""
    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def teardown_function() -> None:
    """Limpa os dados após cada teste."""
    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)


def test_adicionar_e_buscar_cliente() -> None:
    sistema = SistemaCadastro()
    sistema.adicionar_cliente(1, "Ana", "(11) 90000-0000", True)
    sistema.adicionar_cliente(2, "Bruno", "(11) 91111-1111", False)

    cliente = sistema.buscar_cliente_por_id(2)
    assert cliente is not None
    assert cliente.nome == "Bruno"
    assert cliente.prioridade is False

    cliente_nao_existe = sistema.buscar_cliente_por_id(3)
    assert cliente_nao_existe is None


def test_remover_cliente_inativo() -> None:
    sistema = SistemaCadastro()
    sistema.adicionar_cliente(10, "Carlos", "(11) 92222-2222", False)
    sucesso = sistema.remover_cliente_inativo(10)
    assert sucesso is True
    cliente = sistema.buscar_cliente_por_id(10)
    assert cliente is not None
    assert cliente.ativo is False
