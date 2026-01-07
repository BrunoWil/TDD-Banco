from abc import ABC, abstractmethod
from datetime import datetime
from pydantic import BaseModel
from typing import List, Literal
from decimal import Decimal, ROUND_HALF_UP

# --- Implementação TDD (Corrigida) ---

class HistoricoTDD:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
            'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

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
        if conta.depositar(self._valor):
            conta.historico.adicionar_transacao(self)
            return True
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
            return True
        return False

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero, cliente, saldo=0, agencia='0001'):
        self._saldo = Decimal(str(saldo))
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = HistoricoTDD()

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

class ContaTDD(Conta):
    """
    Versão da conta refatorada com TDD.
    Corrige:
    1. Precisão numérica (usa Decimal).
    2. Lógica de limite de saques (verifica dicionário corretamente).
    3. Validações de estado (Guard Assertions).
    """
    def __init__(self, numero, cliente, saldo=0, limite=500, limite_saque=3):
        # Correção: Sanitização de saldo inicial negativo
        if saldo < 0:
            saldo = 0
        super().__init__(numero, cliente, saldo)
        self.limite = Decimal(str(limite))
        self.limite_saque = limite_saque

    def sacar(self, valor):
        valor = Decimal(str(valor)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        # Validação básica
        if valor <= 0:
            return False
        
        # Aqui verificamos a chave 'tipo' no dicionário do histórico.
        numero_saque = len([t for t in self.historico.transacoes if t['tipo'] == 'Saque'])
        
        if numero_saque >= self.limite_saque:
            return False # Limite excedido
            
        if valor > self.limite:
            return False # Valor acima do limite por saque
            
        if valor > self._saldo:
            return False # Saldo insuficiente
            
        # CORREÇÃO PRECISÃO: Operação com Decimal
        self._saldo -= valor
        self._saldo = self._saldo.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return True

    def depositar(self, valor):
        valor = Decimal(str(valor)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if valor <= 0:
            return False
        self._saldo += valor
        self._saldo = self._saldo.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return True

# --- Modelos de Requisição ---
class Operacao(BaseModel):
    tipo: Literal["saque", "deposito"]
    valor: float

class SimulacaoRequest(BaseModel):
    saldo_inicial: float
    limite: float = 500.0
    limite_saque: int = 3
    operacoes: List[Operacao]

# --- Endpoints ---
