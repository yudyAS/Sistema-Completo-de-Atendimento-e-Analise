import shutil

from services.atendimento import SistemaAtendimento
from services.registry import SistemaCadastro
from storage.persistence import DATA_DIR


def setup_function() -> None:
    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def teardown_function() -> None:
    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)


def test_fluxo_de_atendimento() -> None:
    cadastro = SistemaCadastro()
    cadastro.adicionar_cliente(1, "Ana", "(11) 90000-0000", True)
    cadastro.adicionar_cliente(2, "Bruno", "(11) 91111-1111", False)
    cadastro.adicionar_atendente(1, "Paula")

    atendimento = SistemaAtendimento(cadastro)
    atendimento.abrir_atendimento(1)
    atendimento.abrir_atendimento(2)

    cliente_chamado = atendimento.chamar_proximo(1)
    assert cliente_chamado == 1

    registro = atendimento.finalizar_atendimento(1, 15)
    assert registro.cliente_id == 1
    assert registro.duracao_minutos == 15

    atendimento_desfeito = atendimento.desfazer_ultima_finalizacao()
    assert atendimento_desfeito.cliente_id == 1
    assert not atendimento.historico


def test_calcula_tempo_medio() -> None:
    cadastro = SistemaCadastro()
    cadastro.adicionar_cliente(10, "Carla", "(11) 92222-2222", False)
    cadastro.adicionar_atendente(5, "Lucas")

    atendimento = SistemaAtendimento(cadastro)
    atendimento.abrir_atendimento(10)
    atendimento.chamar_proximo(5)
    atendimento.finalizar_atendimento(5, 20)
    assert atendimento.calcular_tempo_medio() == 20.0
