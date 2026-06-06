from services.atendimento import SistemaAtendimento
from services.registry import SistemaCadastro


def test_listar_atendimentos_por_data() -> None:
    cadastro = SistemaCadastro()
    atendimento = SistemaAtendimento(cadastro)

    # Garantir que há atendimentos de 2026-06-01 (existem no data/atendimentos.json)
    resultados = atendimento.listar_atendimentos_por_data("2026-06-01")
    assert isinstance(resultados, list)
    assert all(r.data.startswith("2026-06-01") for r in resultados)


def test_top_clientes_atendidos() -> None:
    cadastro = SistemaCadastro()
    atendimento = SistemaAtendimento(cadastro)

    top = atendimento.top_clientes_atendidos(limite=3)
    assert isinstance(top, list)
    # Cada item deve ser tupla (cliente_id, nome, qtd)
    if top:
        cid, nome, qtd = top[0]
        assert isinstance(cid, int)
        assert isinstance(nome, str)
        assert isinstance(qtd, int)


def test_verificar_alertas_fila() -> None:
    cadastro = SistemaCadastro()
    atendimento = SistemaAtendimento(cadastro)

    alertas = atendimento.verificar_alertas_fila(limite_minutos=1)
    assert isinstance(alertas, list)

