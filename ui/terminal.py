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
    while True:
        print("\n=== Sistema de Atendimento ===")
        print("1 - Cadastrar cliente")
        print("2 - Cadastrar atendente")
        print("3 - Buscar cliente por ID")
        print("4 - Listar clientes ativos")
        print("5 - Remover cliente inativo")
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

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")
