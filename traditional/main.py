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
        # ERRO DE PRECISÃO: Uso de float para dinheiro
        self._saldo = 0.0
        self._limite = limite
        self._limite_saque = limite_saque
        self._saques_realizados = 0
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    def depositar(self, valor):
        # ERRO DE PRECISÃO: Conversão para float
        valor = float(valor)
        
        # ERRO DE LÓGICA: Não valida valor negativo ou zero
        # Deveria ter: if valor <= 0: return False
        
        self._saldo += valor
        self._historico.adicionar_transacao(f"Deposito de {valor}")
        return True

    def sacar(self, valor):
        valor = float(valor)
        
        # ERRO DE ESTADO: Incrementa contador antes de saber se o saque é válido
        # Se falhar por limite, o cliente perdeu uma tentativa injustamente.
        self._saques_realizados += 1
        
        # Validação apenas do limite por operação
        if valor > self._limite:
            return False
            
        # ERRO DE LÓGICA: Permite saldo negativo (Cheque especial infinito)
        # Falta verificar: if valor > self._saldo: ...
        
        # ERRO DE LÓGICA: Ignora o limite de quantidade de saques diários
        # Falta verificar: if self._saques_realizados > self._limite_saque: ...
        
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