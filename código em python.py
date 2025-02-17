def main():
    # Variáveis iniciais
    saldo = 0  # Armazena o saldo da conta
    extrato = []  # Lista para armazenar as operações (depósitos e saques)
    numero_saques = 0  # Contador de saques realizados no dia
    LIMITE_SAQUES = 3  # Limite de saques diários
    LIMITE_POR_SAQUE = 500  # Limite máximo por saque

    # Menu do sistema
    menu = """
    === Sistema Bancário ===
    [D] Depósito
    [S] Saque
    [E] Extrato
    [Q] Sair
    => """

    while True:
        # Exibe o menu e solicita a escolha do usuário
        opcao = input(menu).strip().upper()

        # Opção Depósito
        if opcao == "D":
            valor_input = input("Digite o valor do depósito: R$ ").strip()

            # Substitui vírgula por ponto, caso o usuário digite vírgula
            valor_input = valor_input.replace(",", ".")

            try:
                # Converte o valor para float
                valor = float(valor_input)

                # Verifica se o valor é positivo
                if valor > 0:
                    saldo += valor
                    extrato.append(f"Depósito: R$ {valor:.2f}")
                    print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
                else:
                    print("Valor inválido! O valor do depósito deve ser positivo.")
            except ValueError:
                # Caso o usuário digite um valor não numérico
                print("Valor inválido! Digite um número válido.")

        # Opção Saque
        elif opcao == "S":
            if numero_saques >= LIMITE_SAQUES:
                print("Limite diário de saques atingido!")
            else:
                valor_input = input("Digite o valor do saque: R$ ").strip()

                # Substitui vírgula por ponto, caso o usuário digite vírgula
                valor_input = valor_input.replace(",", ".")

                try:
                    # Converte o valor para float
                    valor = float(valor_input)

                    # Verifica se o valor é válido (positivo e dentro do limite)
                    if valor > 0 and valor <= LIMITE_POR_SAQUE:
                        if saldo >= valor:
                            saldo -= valor
                            extrato.append(f"Saque: R$ {valor:.2f}")
                            numero_saques += 1
                            print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
                        else:
                            print("Saldo insuficiente para realizar o saque.")
                    else:
                        print(f"Valor inválido! O valor do saque deve ser positivo e não pode exceder R$ {LIMITE_POR_SAQUE:.2f}.")
                except ValueError:
                    # Caso o usuário digite um valor não numérico
                    print("Valor inválido! Digite um número válido.")

        # Opção Extrato
        elif opcao == "E":
            print("\n=== Extrato ===")
            if not extrato:
                print("Nenhuma operação realizada.")
            else:
                # Exibe todas as operações registradas
                for operacao in extrato:
                    print(operacao)
            # Exibe o saldo atual
            print(f"\nSaldo atual: R$ {saldo:.2f}")

        # Opção Sair
        elif opcao == "Q":
            print("Saindo do sistema...")
            break

        # Opção inválida
        else:
            print("Opção inválida! Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    main()
