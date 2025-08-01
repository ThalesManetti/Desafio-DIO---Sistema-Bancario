# 💳 Sistema Bancário em Python

Este repositório contém a evolução de um sistema bancário desenvolvido em Python. 
O projeto foi dividido em **três versões progressivas**, com o objetivo de aplicar boas práticas de desenvolvimento, refatoração e conceitos fundamentais da programação, culminando em uma arquitetura orientada a objetos.

---

## 📈 Evolução do Projeto

### ✅ Versão 1 — Implementação Procedural

A primeira versão foi implementada de forma totalmente **procedural**, utilizando apenas estruturas básicas da linguagem.

**Funcionalidades:**

- Operações bancárias: depósito, saque, extrato
- Limitação de número de saques diários
- Limite por valor de saque
- Armazenamento de extrato em lista
- Tratamento de entrada via `input()` e validação de dados com `try/except`

**Técnicas e estruturas utilizadas:**

- Controle de fluxo com `if`, `while`, `try/except`
- Listas para registro de transações
- Boas práticas de identação, mensagens claras e tratamento de erros

**Pontos fortes:**

- Código funcional e bem comentado
- Mensagens de erro amigáveis
- Clareza no fluxo de execução

**Limitações:**

- Baixa escalabilidade e reutilização
- Alto acoplamento entre lógica e fluxo de entrada
- Nenhuma abstração de usuário ou conta

---

### 👥 Versão 2 — Suporte a Múltiplos Usuários

A segunda versão reestrutura o sistema para suportar **múltiplos usuários** e **múltiplas contas** associadas a esses usuários. O código se torna mais modular, mas ainda procedural.

**Principais melhorias:**

- Cadastro de usuários com CPF e validação com expressão regular (`re`)
- Criação de contas vinculadas a clientes
- Autenticação de usuários pelo CPF
- Separação do código em funções específicas com responsabilidade única
- Introdução de conceitos de filtragem e validação externa

**Boas práticas aplicadas:**

- Modularização: funções como `criar_cliente()`, `autenticar_cliente()`, `criar_conta()`
- Validação de entrada com regex
- Menor repetição de código, maior reutilização

**Limitações persistentes:**

- Acoplamento ainda alto entre dados e operações
- A lógica de negócio permanece acoplada ao input/output
- Ausência de encapsulamento (nenhuma classe ainda é usada)

---

### 🧠 Versão 3 — Arquitetura Orientada a Objetos (POO)

A terceira versão transforma o sistema com base nos **princípios da Programação Orientada a Objetos**, promovendo maior extensibilidade, organização e coesão.

**Componentes principais:**

- `PessoaFisica`: representa o indivíduo com nome, CPF e data de nascimento
- `Cliente`: encapsula um cliente e suas contas
- `Conta` e `ContaCorrente`: abstração de conta bancária com herança
- `Historico`: armazena transações realizadas
- `Transacao`, `Saque`, `Deposito`: classes para aplicar polimorfismo e encapsular ações bancárias

**Melhorias significativas:**

- Cada classe possui uma única responsabilidade (SRP - Single Responsibility Principle)
- Abstração de operações por meio da hierarquia de `Transacao`
- Registro de extrato baseado em objetos e não apenas em strings
- Composição entre objetos: cliente → conta → histórico → transações
- Facilita futura integração com banco de dados, testes unitários ou interface gráfica

**Boas práticas aplicadas:**

- Herança e polimorfismo (`ContaCorrente` herda de `Conta`, `Saque` e `Deposito` herdam de `Transacao`)
- Composição ao invés de acoplamento rígido (ex: `Conta` tem um `Historico`)
- Validação de CPF com expressões regulares
- Código extensível e desacoplado

**Limitações remanescentes (oportunidades de melhoria):**

- Falta de controle de datas nas transações
- Regras de negócio (ex: limites) ainda parcialmente fora de encapsulamento ideal
- Persistência em memória (sem armazenamento em arquivo ou banco)
- Interface via terminal pode ser substituída por API ou GUI futuramente

---

## 🧪 Tecnologias Utilizadas

- Python 3.10+
- Módulo `re` para expressões regulares
- Conceitos de POO: classes, herança, encapsulamento, composição, polimorfismo
- Controle de fluxo, tratamento de exceções, listas

---

## 🧭 Conclusão

Este projeto demonstra a **evolução natural de um sistema real** partindo de uma abordagem funcional/procedural para uma arquitetura orientada a objetos. 
Cada versão introduz conceitos que facilitam manutenções futuras, aumentam a legibilidade e melhoram a qualidade do código.

É uma base sólida para expandir o sistema, seja por meio de:

- Adição de testes automatizados
- Persistência com SQLite ou PostgreSQL
- Interface gráfica com Tkinter ou PyQt
- API REST com FastAPI ou Flask

---

## 🧠 Autor

Desenvolvido por Thales G. Manetti

