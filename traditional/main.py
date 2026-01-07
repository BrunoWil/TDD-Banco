from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime
import textwrap


class Conta:
    def __init__(self,numero,cliente,saldo=0,agencia='0001'): 
        self._saldo = saldo
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()
    @classmethod
    def nova_conta(cls, numero, cliente):
        # print(f"""Conta criada com sucesso! 
        #         Número: {cls.numero}, 
        #         Agência: {cls.agencia},
        #         Cliente: {cls.cliente}""")
        return cls(numero, cliente)
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
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("Operação falhou! Saldo insuficiente!")
            return False
        
        if valor > 0:
            self._saldo -= valor
            print(f"Saque de {valor} realizado com sucesso!")
            return True
        
        excedeu_limite = valor > self.limite_saque if hasattr(self, 'limite_saque') else False
        if excedeu_saldo or excedeu_limite:
            print("Saldo insuficiente ou valor de saque excede o limite.")
            return
        return False
    
    def depositar(self, valor):
        if valor <= 0:
            print("Valor de depósito inválido.")
            return False
        if valor:
            self._saldo += valor
            print(f"Depósito de {valor} realizado com sucesso!")
            return True
        return False

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    @abstractmethod
    def registrar(self, conta):
        pass

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, Transacao):
        print(f"Realizando transação: \n {conta}")
        # Aqui você pode implementar a lógica para realizar uma transação na conta
        Transacao.registrar(conta)
    
    def adcionar_conta(self, conta):
        print(f"Realizando adcinar Conta: {conta}")
        self.contas.append(conta)
        
class PessoaFisica(Cliente):
    def __init__(self, nome,data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saque=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque

    def sacar(self, valor):
        # BUG (Tradicional): 'transacao' é um dict, logo isinstance retorna sempre False. O contador fica sempre em 0.
        numero_saques = len(
            [t for t in self.historico.transacoes if isinstance(t, Saque)]
        )

        if numero_saques >= self.limite_saque:
            print("Operação falhou! Limite de saques diários excedido!")
            return False
        if valor > self.limite:
            print("Operação falhou! Valor de saque excede o limite!")
            return False
        return super().sacar(valor)
    
    def __str__(self):
        return f"""\
            Agência: \t{self.agencia}
            Conta Corrente: \t{self.numero}
            Titular: \t{self.cliente.nome}
        """

   
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        # Armazene o objeto original para manter o tipo (Saque/Deposito)
        self._transacoes.append(transacao)
        
    def gerar_relatorio(self):
        for transacao in self._transacoes:
            yield {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Idealmente a transação deveria ter sua própria data
            }

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor(self):
        return self._valor
    def registrar(self, conta):
        if conta.depositar(self._valor):
            conta.historico.adicionar_transacao(self)
            print(f"Depósito de {self._valor} registrado com sucesso!")
            return True
        print("Falha ao registrar depósito.")
        return False

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor(self):
        return self._valor
    def registrar(self, conta):
        if conta.sacar(self._valor):
            conta.historico.adicionar_transacao(self)
            print(f"Saque de {self._valor} registrado com sucesso!")
            return True
        print("Falha ao registrar saque.")
        return False
