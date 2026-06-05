from services.atendimento import SistemaAtendimento
from services.registry import SistemaCadastro


def solicitar_inteiro(mensagem: str) -> int:
    """Lê um inteiro válido do usuário."""
    while True:
        valor = input(mensagem).strip()
        if not valor.isdigit():
            print("Entrada inválida. Digite apenas números.")
            continue
        return int(valor)


def solicitar_texto(mensagem: str) -> str:
    """Lê uma string não vazia do usuário."""
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("Entrada inválida. O campo não pode ficar vazio.")


def run_menu() -> None:
    """Executa o menu principal do sistema."""
    sistema = SistemaCadastro()
    atendimento_svc = SistemaAtendimento(sistema)
    while True:
        print("\n=== Sistema de Atendimento ===")
        print("1 - Cadastrar cliente")
        print("2 - Cadastrar atendente")
        print("3 - Buscar cliente por ID")
        print("4 - Listar clientes ativos")
        print("5 - Remover cliente inativo")
        print("6 - Abrir atendimento")
        print("7 - Chamar próximo atendimento")
        print("8 - Finalizar atendimento")
        print("9 - Desfazer última finalização")
        print("10 - Tempo médio de atendimento")
        print("11 - Histórico de atendimentos por cliente")
        print("12 - Exportar relatório CSV")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            try:
                cliente_id = solicitar_inteiro("ID do cliente: ")
                nome = solicitar_texto("Nome do cliente: ")
                telefone = solicitar_texto("Telefone do cliente: ")
                prioridade_texto = input("Prioridade? (s/n): ").strip().lower()
                prioridade = prioridade_texto == "s"
                cliente = sistema.adicionar_cliente(cliente_id, nome, telefone, prioridade)
                print(f"Cliente cadastrado: {cliente}")
            except ValueError as erro:
                print(f"Erro: {erro}")

        elif opcao == "2":
            try:
                atendente_id = solicitar_inteiro("ID do atendente: ")
                nome = solicitar_texto("Nome do atendente: ")
                atendente = sistema.adicionar_atendente(atendente_id, nome)
                print(f"Atendente cadastrado: {atendente}")
            except ValueError as erro:
                print(f"Erro: {erro}")

        elif opcao == "3":
            cliente_id = solicitar_inteiro("ID do cliente para buscar: ")
            cliente = sistema.buscar_cliente_por_id(cliente_id)
            if cliente:
                print(f"Cliente encontrado: {cliente}")
            else:
                print("Cliente não encontrado.")

        elif opcao == "4":
            ativos = sistema.listar_cliente_ativos()
            if ativos:
                print("Clientes ativos:")
                for cliente in ativos:
                    prioridade = "Sim" if cliente.prioridade else "Não"
                    print(f"- ID {cliente.id}: {cliente.nome}, Tel: {cliente.telefone}, Prioridade: {prioridade}")
            else:
                print("Nenhum cliente ativo cadastrado.")

        elif opcao == "5":
            try:
                cliente_id = solicitar_inteiro("ID do cliente para remover: ")
                if sistema.remover_cliente_inativo(cliente_id):
                    print("Cliente marcado como inativo e removido da lista de ativos.")
                else:
                    print("Cliente já está inativo ou não foi encontrado.")
            except ValueError as erro:
                print(f"Erro: {erro}")

        elif opcao == "6":
            try:
                cliente_id = solicitar_inteiro("ID do cliente para abrir atendimento: ")
                atendimento_svc.abrir_atendimento(cliente_id)
                print("Cliente adicionado à fila de atendimento.")
            except ValueError as erro:
                print(f"Erro: {erro}")

        elif opcao == "7":
            try:
                atendente_id = solicitar_inteiro("ID do atendente para atender: ")
                cliente_id = atendimento_svc.chamar_proximo(atendente_id)
                cliente = sistema.buscar_cliente_por_id(cliente_id)
                print(f"Próximo atendimento: cliente {cliente_id} - {cliente.nome if cliente else 'desconhecido'}")
            except ValueError as erro:
                print(f"Erro: {erro}")

        elif opcao == "8":
            try:
                atendente_id = solicitar_inteiro("ID do atendente que finaliza: ")
                duracao = solicitar_inteiro("Duração do atendimento em minutos: ")
                atendimento = atendimento_svc.finalizar_atendimento(atendente_id, duracao)
                print(f"Atendimento finalizado: cliente {atendimento.cliente_id}, atendente {atendimento.atendente_id}, duração {atendimento.duracao_minutos} min")
            except ValueError as erro:
                print(f"Erro: {erro}")

        elif opcao == "9":
            try:
                atendimento = atendimento_svc.desfazer_ultima_finalizacao()
                print(f"Finalização desfeita: cliente {atendimento.cliente_id}, atendente {atendimento.atendente_id}")
            except ValueError as erro:
                print(f"Erro: {erro}")

        elif opcao == "10":
            media = atendimento_svc.calcular_tempo_medio()
            print(f"Tempo médio de atendimento: {media:.2f} minutos")

        elif opcao == "11":
            cliente_id = solicitar_inteiro("ID do cliente para ver histórico: ")
            historico = atendimento_svc.listar_historico_cliente(cliente_id)
            if historico:
                print(f"Histórico do cliente {cliente_id}:")
                for item in historico:
                    print(f"- {item.data}: atendente {item.atendente_id}, {item.duracao_minutos} min")
            else:
                print("Nenhum atendimento registrado para esse cliente.")
                
        elif opcao == "12":
            try:
                filename = solicitar_texto("Nome do arquivo CSV para exportar: ")
                atendimento_svc.exportar_relatorio_csv(filename)
                print(f"Relatório exportado para {filename}")
            except ValueError as erro:
                print(f"Erro: {erro}")

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")
