import textwrap
from abc import ABC, abstractmethod
from datetime import datetime 
from time import sleep


class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta: Conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self._cpf
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def data_nascimento(self):
        return self._data_nascimento


class Conta:
    def __init__(self, cliente, numero):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor): # Método que saca o dinheiro após uma validação e retorna True se a operação for bem-sucedida e False caso contrário
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("Operação falhou! Saldo insuficiente.")
        
        
        elif float(valor) > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso!")
            return True
        
        else:
            print("Operação falhou! O valor informado é inválido.")

        return False
            

    def depositar(self, valor): # Método que deposita o dinheiro após uma validação e retorna True se a operação for bem-sucedida e False caso contrário

        if float(valor) > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso!")
            return True
        
        else:
            print("Operação falhou! O valor informado é inválido.")

        return False


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3):
        super().__init__(cliente, numero)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([
            transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__
        ])

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        else:
            return super().sacar(valor)

        return False
    
    def __str__(self):
        return (
            f"Agência:\t{self.agencia}\n"
            f"C/C:\t\t{self.numero}\n"
            f"Titular:\t{self.cliente.nome}\n"
        )


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now()
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self._valor)

        if sucesso_transacao: # Adiciona o depósito ao histórico se a operação for bem-sucedida
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = float(valor)

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self._valor)

        if sucesso_transacao: # Adiciona o saque ao histórico se a operação for bem-sucedida
            conta.historico.adicionar_transacao(self)


def menu():
    sleep(1)
    menu = """
    ================== MENU ==================
    [1] Depositar        [4] Criar conta
    [2] Sacar            [5] Listar contas
    [3] Ver extrato      [6] Novo usuário
    [x] Sair
    ==========================================
    >>> """

    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf, clientes):
    for cliente in clientes:
        if cpf == cliente.cpf:
            return cliente
        

def ler_valor(mensagem):
    while True:
        try:
            valor = float(input(mensagem))
            if valor <= 0:
                print("Valor deve ser maior que zero.\n")
                sleep(0.3)
                continue
            return valor
        except ValueError:
            print("Digite um número válido.\n")
            sleep(0.3)


def obter_cliente(clientes):
    cpf = input("Informe o CPF >>> ")
    cliente = filtrar_cliente(cpf,clientes)

    if not cliente:
        print("ERRO: CPF não encontrado.")
        return None
    
    return cliente


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        return None
    
    print("\nContas disponíveis:")

    for i, conta in enumerate(cliente.contas, start=1):
        print(f"[{i}] Agência: {conta.agencia} | Conta: {conta.numero}")

    try:
        escolha = int(input("\nEscolha a conta >> "))
    except ValueError:
        print("Entrada inválida.")
        return None

    if 1 <= escolha <= len(cliente.contas):
        return cliente.contas[escolha - 1]
    
    print("Opção inválida!")
    return None


def depositar(clientes):
    cliente = obter_cliente(clientes)
    if not cliente:
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        print("ERRO! Cliente não possui conta.")
        return

    valor = ler_valor("Informe o valor do depósito >>> R$")
    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cliente = obter_cliente(clientes)
    if not cliente:
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        print("ERRO! Cliente não possui conta.")
        return

    valor = ler_valor("Informe o valor do saque >>> R$")
    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cliente = obter_cliente(clientes)
    if not cliente:
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        print("ERRO! Cliente não possui conta.")
        return
    
    transacoes = conta.historico.transacoes

    if not transacoes:
        print("Não foram realizadas movimentações.")
        return
    
    else:
        extrato = ""
        for transacao in transacoes:
            data_formatada = transacao['data'].strftime("%d-%m-%Y %H:%M:%S")
            extrato += (
            f"\n{data_formatada} - "
            f"{transacao['tipo'].replace('Deposito', 'Depósito')}: "
            f"R$ {transacao['valor']:.2f}"
        )

    print("\n===============- EXTRATO -================")
    print(extrato)
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("\n==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o cpf >>> ")

    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print("Inválido! Já existe cadastro com esse CPF.")
        return

    nome = input("Informe o nome completo >>> ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa) >>> ")
    endereco = input("Informe o endereço >>> ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("=== Usuário criado com sucesso! ===")


def criar_conta(clientes, contas, numero_conta):
    cpf = input("Informe o cpf >>> ")

    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Usuário não encontrado! Por favor, crie um usuário.")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("=== Conta criada com sucesso! ===")


def listar_contas(clientes, contas):
    cliente = obter_cliente(clientes)

    if not cliente.contas:
        print("Cliente não possui contas.")
        return

    for conta in cliente.contas:
        print("=" * 18)
        print(textwrap.dedent(str(conta)))
    print("=" * 18)

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "4":
            numero_conta = len(contas) + 1
            criar_conta(clientes, contas, numero_conta)

        elif opcao == "5":
            listar_contas(clientes, contas)

        elif opcao == "6":
            criar_cliente(clientes)

        elif opcao in "Xx":
            print("Finalizando programa. . .")
            sleep(1)
            break

        else:
            print("Opção inválida! Por favor, digite uma opção do menu.")


main()