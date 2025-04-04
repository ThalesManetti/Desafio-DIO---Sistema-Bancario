import re  # Importando o módulo de expressões regulares
from datetime import datetime

# Definição das classes conforme o diagrama UML

class PessoaFisica:
    def __init__(self, nome, cpf, data_nascimento):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento


class Cliente:
    def __init__(self, endereco, pessoa_fisica):
        self.endereco = endereco
        self.contas = []
        self.cpf = pessoa_fisica.cpf
        self.nome = pessoa_fisica.nome
        self.data_nascimento = pessoa_fisica.data_nascimento
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)


class Historico:
    def __init__(self):
        self.transacoes = []
    
    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)


class Conta:
    def __init__(self, numero, cliente, agencia="0001"):
        self.saldo = 0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()
    
    def saldo(self):
        return self.saldo
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    def sacar(self, valor):
        if valor > 0 and self.saldo >= valor:
            self.saldo -= valor
            return True
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            return True
        return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500.0, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques


class Transacao:
    @staticmethod
    def registrar(conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor
    
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)
            return True
        return False


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor
    
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)
            return True
        return False


def main():
    clientes = []  # Lista para armazenar os clientes
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
            (clientes)

        elif opcao == "NC":
            numero_conta = criar_conta(numero_conta, clientes)

        elif opcao == "A":
            cliente_autenticado, conta_corrente = autenticar_cliente(clientes)
            if cliente_autenticado and conta_corrente:
                menu_operacoes(cliente_autenticado, conta_corrente)

        elif opcao == "Q":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida! Por favor, escolha uma opção válida.")


def menu_operacoes(cliente, conta):
    """
    Exibe o menu de operações bancárias após a autenticação.

    Args:
        cliente (Cliente): O cliente autenticado.
        conta (ContaCorrente): A conta do cliente autenticado.
    """
    numero_saques = 0
    
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
                deposito = Deposito(valor)
                if cliente.realizar_transacao(conta, deposito):
                    print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
                else:
                    print("Não foi possível realizar o depósito!")
            except ValueError:
                print("Valor inválido! Digite um número válido.")

        elif opcao == "S":
            valor_input = input("Digite o valor do saque: R$ ").strip()
            valor_input = valor_input.replace(",", ".")
            try:
                valor = float(valor_input)
                if numero_saques >= conta.limite_saques:
                    print("Limite diário de saques atingido!")
                elif valor > conta.limite:
                    print(f"Valor inválido! O valor do saque não pode exceder R$ {conta.limite:.2f}.")
                else:
                    saque = Saque(valor)
                    if cliente.realizar_transacao(conta, saque):
                        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
                        numero_saques += 1
                    else:
                        print("Não foi possível realizar o saque!")
            except ValueError:
                print("Valor inválido! Digite um número válido.")

        elif opcao == "E":
            exibir_extrato(conta)

        elif opcao == "L":
            print("Logout efetuado com sucesso!")
            break

        else:
            print("Opção inválida! Por favor, escolha uma opção válida.")


def exibir_extrato(conta):
    """
    Exibe o extrato da conta.

    Args:
        conta (ContaCorrente): A conta a ser exibida.
    """
    print("\n=== Extrato ===")
    print(f"Usuário: {conta.cliente.nome}")
    print(f"Conta Corrente: {conta.numero}")
    
    transacoes = conta.historico.transacoes
    
    if not transacoes:
        print("Nenhuma operação realizada.")
    else:
        for transacao in transacoes:
            if isinstance(transacao, Saque):
                print(f"Saque: R$ {transacao.valor:.2f}")
            elif isinstance(transacao, Deposito):
                print(f"Depósito: R$ {transacao.valor:.2f}")
    
    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")


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


def filtrar_cliente(cpf, clientes):
    """
    Filtra um cliente pelo CPF.

    Args:
        cpf (str): CPF do cliente (XXX.XXX.XXX-XX).
        clientes (list): Lista de clientes.

    Returns:
        Cliente: Cliente encontrado ou None.
    """
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def criar_cliente(clientes):
    """
    Cria um novo cliente e o adiciona à lista de clientes.

    Args:
        clientes (list): Lista de clientes.
    """
    while True:
        cpf = input("Informe o CPF (XXX.XXX.XXX-XX): ")
        if validar_cpf(cpf):
            break
        else:
            print("CPF inválido. O CPF deve estar no formato XXX.XXX.XXX-XX.")

    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Já existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, numero - bairro - cidade/sigla estado): ")

    pessoa = PessoaFisica(nome, cpf, data_nascimento)
    cliente = Cliente(endereco, pessoa)
    clientes.append(cliente)

    print("Cliente criado com sucesso!")


def criar_conta(numero_conta, clientes):
    """
    Cria uma nova conta corrente e a adiciona ao cliente.

    Args:
        numero_conta (int): Número da conta corrente.
        clientes (list): Lista de clientes.

    Returns:
        int: Novo número da conta.
    """
    cpf = input("Informe o CPF do cliente (XXX.XXX.XXX-XX): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        conta = ContaCorrente.nova_conta(cliente, numero_conta)
        cliente.adicionar_conta(conta)
        print(f"Conta criada com sucesso! Agência: {conta.agencia} | Conta: {conta.numero}")
        return numero_conta + 1
    else:
        print("Cliente não encontrado!")
        return numero_conta


def autenticar_cliente(clientes):
    """
    Autentica o cliente pelo CPF.

    Args:
        clientes (list): Lista de clientes.
    Returns:
        tuple: Cliente autenticado e conta corrente, ou (None, None).
    """
    cpf = input("Informe seu CPF para acessar a conta (XXX.XXX.XXX-XX): ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if cliente:
        if cliente.contas:
            # Por simplicidade, vamos pegar a primeira conta do cliente
            conta = cliente.contas[0]
            print("Cliente autenticado com sucesso!")
            return cliente, conta
        else:
            print("Cliente não possui conta cadastrada!")
            return None, None
    else:
        print("Cliente não encontrado!")
        return None, None


if __name__ == "__main__":
    main()
