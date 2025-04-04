import re  # Importando o módulo de expressões regulares


def main():
    """
    Função principal do sistema bancário.
    """
    usuarios = []  # Lista para armazenar os usuários
    contas = []  # Lista para armazenar as contas
    numero_conta = 1  # Conta corrente é sequencial começando em 1

    menu = """
    === Sistema Bancário ===
    [NU] Novo usuário
    [NC] Nova Conta
    [A] Acessar conta
    [Q] Sair
    => """

    while True:
        opcao = input(menu).strip().upper()

        if opcao == "NU":
            criar_usuario(usuarios)

        elif opcao == "NC":
            numero_conta, cont = criar_conta(numero_conta, contas, usuarios)
            if cont is False:
                print("Não foi possível criar a conta")

        elif opcao == "A":
            usuario_logado, conta_corrente = autenticar_usuario(usuarios, contas)
            if usuario_logado:
                menu_operacoes(usuario_logado, conta_corrente ,contas, usuarios)

        elif opcao == "Q":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida! Por favor, escolha uma opção válida.")


def menu_operacoes(usuario_logado, conta_corrente, contas, usuarios):
    """
    Exibe o menu de operações bancárias após a autenticação.

    Args:
        usuario_logado (dict): O usuário autenticado.
        conta_corrente (int): conta do usuario autenticado.
    """
    saldo = 0
    extrato = []
    numero_saques = 0
    LIMITE_SAQUES = 3
    LIMITE_POR_SAQUE = 500
    
    
    menu_interno = """
    === Operações Bancárias ===
    [D] Depósito
    [S] Saque
    [E] Extrato
    [L] Logout
    => """
    
    while True:
        opcao = input(menu_interno).strip().upper()

        if opcao == "D":
            valor_input = input("Digite o valor do depósito: R$ ").strip()
            valor_input = valor_input.replace(",", ".")

            try:
                valor = float(valor_input)
                saldo, extrato = depositar(saldo, valor, extrato)
            except ValueError:
                print("Valor inválido! Digite um número válido.")

        elif opcao == "S":
            valor_input = input("Digite o valor do saque: R$ ").strip()
            valor_input = valor_input.replace(",", ".")
            try:
                valor = float(valor_input)
                saldo, extrato = sacar(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=LIMITE_POR_SAQUE,
                    quantidade_saque=numero_saques,
                    limite_saques=LIMITE_SAQUES,
                )
                if (f"Saque: R$ {valor:.2f}") in extrato:
                    numero_saques += 1

            except ValueError:
                print("Valor inválido! Digite um número válido.")

        elif opcao == "E":
            exibir_extrato(saldo, extrato=extrato, usuario=usuario_logado, conta_corrente=conta_corrente)

        elif opcao == "L":
            print("Logout efetuado com sucesso!")
            break

        else:
            print("Opção inválida! Por favor, escolha uma opção válida.")

def depositar(saldo, valor, extrato, /):
    """
    Realiza um depósito na conta.

    Args:
        saldo (float): Saldo atual da conta.
        valor (float): Valor a ser depositado.
        extrato (list): Lista de transações.
    Returns:
        tuple: O novo saldo e o extrato atualizado.
    """
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Valor inválido! O valor do depósito deve ser positivo.")
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, quantidade_saque, limite_saques):
    """
    Realiza um saque na conta.

    Args:
        saldo (float): Saldo atual da conta.
        valor (float): Valor a ser sacado.
        extrato (list): Lista de transações.
        limite (float): Limite máximo por saque.
        quantidade_saque (int): Quantidade de saques já realizados no dia.
        limite_saques (int): Limite máximo de saques diários.

    Returns:
        tuple: O novo saldo e o extrato atualizado.
    """
    if quantidade_saque >= limite_saques:
        print("Limite diário de saques atingido!")
        return saldo, extrato

    if valor > limite:
        print(f"Valor inválido! O valor do saque não pode exceder R$ {limite:.2f}.")
        return saldo, extrato

    if valor > saldo:
        print("Saldo insuficiente para realizar o saque.")
        return saldo, extrato

    if valor <= 0:
        print("Valor invalido! Digite um valor positivo")
        return saldo, extrato

    saldo -= valor
    extrato.append(f"Saque: R$ {valor:.2f}")
    print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato, usuario, conta_corrente):
    """
    Exibe o extrato da conta.

    Args:
        saldo (float): Saldo atual da conta.
        extrato (list): Lista de transações.
        usuario (dict): dicionario com os dados do usuario.
        conta_corrente (dict): dicionario com os dados da conta corrente.
    """
    print("\n=== Extrato ===")
    print(f"Usuário: {usuario['nome']}")
    print(f"Conta Corrente: {conta_corrente['numero_conta']}")
    if not extrato:
        print("Nenhuma operação realizada.")
    else:
        for operacao in extrato:
            print(operacao)
    print(f"\nSaldo atual: R$ {saldo:.2f}")


def criar_usuario(usuarios):
    """
    Cria um novo usuário e o adiciona à lista de usuários.

    Args:
        usuarios (list): Lista de usuários.
    """
    while True:
        cpf = input("Informe o CPF (XXX.XXX.XXX-XX): ")
        if validar_cpf(cpf):
            break
        else:
            print("CPF inválido. O CPF deve estar no formato XXX.XXX.XXX-XX.")

    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Já existe usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, numero - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("Usuário criado com sucesso!")


def validar_cpf(cpf):
    """
    Valida se o CPF está no formato XXX.XXX.XXX-XX.

    Args:
        cpf (str): CPF a ser validado.

    Returns:
        bool: True se o CPF for válido, False caso contrário.
    """
    padrao = re.compile(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")
    return bool(padrao.match(cpf))


def filtrar_usuario(cpf, usuarios):
    """
    Filtra um usuário pelo CPF.

    Args:
        cpf (str): CPF do usuário (XXX.XXX.XXX-XX).
        usuarios (list): Lista de usuários.

    Returns:
        dict: Usuário encontrado ou None.
    """
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(numero_conta, contas, usuarios):
    """
    Cria uma nova conta corrente e a adiciona à lista de contas.

    Args:
        numero_conta (int): Número da conta corrente.
        contas (list): Lista de contas.
        usuarios (list): Lista de usuários.

    Returns:
        tuple: Novo número da conta e Booleano se houve sucesso na criação.
    """
    cpf = input("Informe o CPF do usuário (XXX.XXX.XXX-XX): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        conta = {
            "agencia": "0001",
            "numero_conta": numero_conta,
            "usuario": usuario,
        }
        contas.append(conta)
        print(f"Conta criada com sucesso! Agência: {conta['agencia']} | Conta: {conta['numero_conta']}")
        return numero_conta + 1, True
    else:
        print("Usuário não encontrado!")
        return numero_conta, False

def autenticar_usuario(usuarios, contas):
    """
    Autentica o usuário pelo CPF.

    Args:
        usuarios (list): Lista de usuários.
        contas (list): Lista de contas.
    Returns:
        tuple: Usuário autenticado, ou None, conta corrente do usuario
    """
    cpf = input("Informe seu CPF para acessar a conta (XXX.XXX.XXX-XX): ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        usuario_tem_conta = False
        for conta in contas:
            if conta["usuario"] == usuario:
                usuario_tem_conta = True
                break
        if usuario_tem_conta:
            conta_corrente = [conta for conta in contas if conta["usuario"] == usuario][0]
            print("Usuário autenticado com sucesso!")
            return usuario, conta_corrente
        else:
            print("Usuário não possui conta cadastrada!")
            return None, None
    else:
        print("Usuário não encontrado!")
        return None, None
    
    

if __name__ == "__main__":
    main()
