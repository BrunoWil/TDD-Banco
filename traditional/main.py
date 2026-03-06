from abc import ABC, abstractmethod

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class ContaCorrente:
    def __init__(self, numero, cliente, limite=500, limite_saque=3):
        self._numero = numero
        self._cliente = cliente
        self._saldo = 0.0
        self._limite = limite
        self._limite_saque = limite_saque
        self._saques_realizados = 0
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    def depositar(self, valor):
        valor = float(valor)      
        self._saldo += valor
        self._historico.adicionar_transacao(f"Deposito de {valor}")
        return True

    def sacar(self, valor):
        valor = float(valor)
        self._saques_realizados += 1
    
        if valor > self._limite:
            return False
        
        self._saldo -= valor
        self._historico.adicionar_transacao(f"Saque de {valor}")
        return True

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor
    def registrar(self, conta):
        return conta.depositar(self.valor)

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor
    def registrar(self, conta):
        return conta.sacar(self.valor)