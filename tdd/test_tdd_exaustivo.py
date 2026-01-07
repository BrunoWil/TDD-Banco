import pytest
from decimal import Decimal
from tdd.main_tdd import PessoaFisica, ContaTDD

# ==============================================================================
# Suíte de Testes TDD (Consolidada)
# Baseada nos conceitos do documento TDD.tex.
# Substitui e expande os testes demonstrativos de test_tdd.py.
# ==============================================================================

# ==========================================
# Configuração e Fixtures
# ==========================================

@pytest.fixture
def cliente_padrao():
    return PessoaFisica("Tester TDD", "01/01/2000", "123.456.789-00", "Rua Teste, 123")

@pytest.fixture
def conta_zerada(cliente_padrao):
    """Retorna uma conta com saldo 0 e limites padrão."""
    return ContaTDD(1, cliente_padrao, saldo=0, limite=500, limite_saque=3)

@pytest.fixture
def conta_com_saldo(cliente_padrao):
    """Retorna uma conta com saldo 1000 e limites padrão."""
    return ContaTDD(2, cliente_padrao, saldo=1000, limite=500, limite_saque=3)

# ==========================================
# Grupo 1: Inicialização e Tipagem (5 Testes)
# ==========================================

def test_01_instancia_conta_saldo_inicial_zero(conta_zerada):
    """Verifica se a conta inicia com saldo zero Decimal."""
    assert conta_zerada.saldo == Decimal('0.00')
    assert isinstance(conta_zerada.saldo, Decimal)

def test_02_instancia_conta_saldo_inicial_float_converte_para_decimal(cliente_padrao):
    """Verifica se passar float no construtor converte corretamente para Decimal."""
    conta = ContaTDD(3, cliente_padrao, saldo=100.50)
    assert conta.saldo == Decimal('100.50')
    assert isinstance(conta.saldo, Decimal)

def test_03_instancia_conta_limites_padrao(conta_zerada):
    """Verifica se os limites padrão são respeitados."""
    assert conta_zerada.limite == Decimal('500')
    assert conta_zerada.limite_saque == 3

def test_04_instancia_conta_limites_customizados(cliente_padrao):
    """Verifica a criação de conta com limites personalizados."""
    conta = ContaTDD(4, cliente_padrao, limite=1000, limite_saque=5)
    assert conta.limite == Decimal('1000')
    assert conta.limite_saque == 5

def test_05_atributos_cliente_corretos(conta_zerada):
    """Verifica se o cliente foi associado corretamente."""
    assert conta_zerada.cliente.nome == "Tester TDD"

# ==========================================
# Grupo 2: Depósitos (6 Testes)
# ==========================================

def test_06_deposito_valor_positivo_incrementa_saldo(conta_zerada):
    """Verifica depósito de valor válido."""
    resultado = conta_zerada.depositar(100)
    assert resultado is True
    assert conta_zerada.saldo == Decimal('100.00')

def test_07_deposito_valor_string_converte_decimal(conta_zerada):
    """Verifica se depósito aceita string e converte."""
    conta_zerada.depositar("50.50")
    assert conta_zerada.saldo == Decimal('50.50')

def test_08_deposito_valor_zero_retorna_false(conta_zerada):
    """Verifica rejeição de depósito zero."""
    resultado = conta_zerada.depositar(0)
    assert resultado is False
    assert conta_zerada.saldo == Decimal('0.00')

def test_09_deposito_valor_negativo_retorna_false(conta_zerada):
    """Verifica rejeição de depósito negativo."""
    resultado = conta_zerada.depositar(-50)
    assert resultado is False
    assert conta_zerada.saldo == Decimal('0.00')

def test_10_deposito_multiplos_incrementam_corretamente(conta_zerada):
    """Verifica múltiplos depósitos sequenciais."""
    conta_zerada.depositar(10)
    conta_zerada.depositar(20)
    conta_zerada.depositar(30)
    assert conta_zerada.saldo == Decimal('60.00')

def test_11_deposito_precisao_centavos(conta_zerada):
    """Verifica se centavos são tratados corretamente."""
    conta_zerada.depositar(0.01)
    assert conta_zerada.saldo == Decimal('0.01')

# ==========================================
# Grupo 3: Saques - Validações Básicas (6 Testes)
# ==========================================

def test_12_saque_valor_positivo_saldo_suficiente(conta_com_saldo):
    """Verifica saque com saldo suficiente."""
    resultado = conta_com_saldo.sacar(100)
    assert resultado is True
    assert conta_com_saldo.saldo == Decimal('900.00')

def test_13_saque_valor_igual_saldo_zera_conta(conta_com_saldo):
    """Verifica saque de todo o saldo."""
    conta_com_saldo.limite = Decimal('2000')  # Aumenta limite para permitir saque total
    conta_com_saldo.sacar(1000)
    assert conta_com_saldo.saldo == Decimal('0.00')

def test_14_saque_valor_maior_que_saldo_retorna_false(conta_com_saldo):
    """Verifica Guard Assertion para saldo insuficiente."""
    resultado = conta_com_saldo.sacar(1001)
    assert resultado is False
    assert conta_com_saldo.saldo == Decimal('1000.00') # Saldo inalterado

def test_15_saque_valor_zero_retorna_false(conta_com_saldo):
    """Verifica rejeição de saque zero."""
    assert conta_com_saldo.sacar(0) is False

def test_16_saque_valor_negativo_retorna_false(conta_com_saldo):
    """Verifica rejeição de saque negativo."""
    assert conta_com_saldo.sacar(-100) is False

def test_17_saque_respeita_limite_por_transacao(conta_com_saldo):
    """Verifica se o saque respeita o limite de valor por transação (500)."""
    # Tenta sacar 600 (tem saldo, mas excede limite de 500)
    resultado = conta_com_saldo.sacar(600)
    assert resultado is False
    assert conta_com_saldo.saldo == Decimal('1000.00')

# ==========================================
# Grupo 4: Precisão Numérica (5 Testes)
# ==========================================

def test_18_precisao_soma_ponto_flutuante(conta_zerada):
    """
    Teste Crítico: 0.1 + 0.1 + 0.1 == 0.30
    Em float isso falharia (0.30000000000000004).
    """
    conta_zerada.depositar(0.1)
    conta_zerada.depositar(0.1)
    conta_zerada.depositar(0.1)
    assert conta_zerada.saldo == Decimal('0.30')

def test_19_precisao_subtracao_ponto_flutuante(conta_zerada):
    """
    Teste Crítico: 1.10 - 0.40 == 0.70
    Em float isso falharia (0.7000000000000001).
    """
    conta_zerada.depositar(1.10)
    conta_zerada.sacar(0.40)
    assert conta_zerada.saldo == Decimal('0.70')

def test_20_precisao_multiplicacao_implícita(conta_zerada):
    """Verifica acumulação de muitos valores pequenos."""
    for _ in range(100):
        conta_zerada.depositar(0.01)
    assert conta_zerada.saldo == Decimal('1.00')

def test_21_arredondamento_duas_casas(conta_zerada):
    """Verifica se o sistema arredonda entradas com mais de 2 casas."""
    # 10.555 -> 10.56 (ROUND_HALF_UP)
    conta_zerada.depositar(10.555)
    assert conta_zerada.saldo == Decimal('10.56')

def test_22_arredondamento_saque(conta_com_saldo):
    """Verifica arredondamento no saque."""
    conta_com_saldo.sacar(10.555)
    # 1000 - 10.56 = 989.44
    assert conta_com_saldo.saldo == Decimal('989.44')

# ==========================================
# Grupo 5: Regras de Negócio e Limites (5 Testes)
# ==========================================

def test_23_limite_saques_diarios_contagem_inicial(conta_com_saldo):
    """Verifica se a contagem de saques começa válida."""
    # Como a classe ContaTDD não adiciona ao histórico automaticamente (responsabilidade da API),
    # verificamos se ela permite o primeiro saque.
    assert conta_com_saldo.sacar(10) is True

def test_24_limite_saques_diarios_bloqueio_quarto_saque(conta_com_saldo):
    """
    Simula 3 saques no histórico e verifica se o 4º é bloqueado.
    Nota: Injetamos no histórico manualmente pois a classe ContaTDD 
    foi desenhada para ser orquestrada pela API.
    """
    # Simula estado onde 3 saques já ocorreram
    conta_com_saldo.historico.transacoes.append({'tipo': 'Saque', 'valor': 10, 'data': '...'})
    conta_com_saldo.historico.transacoes.append({'tipo': 'Saque', 'valor': 10, 'data': '...'})
    conta_com_saldo.historico.transacoes.append({'tipo': 'Saque', 'valor': 10, 'data': '...'})
    
    # Tenta o 4º saque
    resultado = conta_com_saldo.sacar(10)
    assert resultado is False

def test_25_limite_saques_nao_afeta_depositos(conta_com_saldo):
    """Verifica se atingir o limite de saques não bloqueia depósitos."""
    conta_com_saldo.historico.transacoes.append({'tipo': 'Saque', 'valor': 10, 'data': '...'})
    conta_com_saldo.historico.transacoes.append({'tipo': 'Saque', 'valor': 10, 'data': '...'})
    conta_com_saldo.historico.transacoes.append({'tipo': 'Saque', 'valor': 10, 'data': '...'})
    
    assert conta_com_saldo.depositar(100) is True

def test_26_limite_saques_customizado(cliente_padrao):
    """Verifica se conta com limite de saques diferente (ex: 5) funciona."""
    conta = ContaTDD(5, cliente_padrao, saldo=1000, limite_saque=5)
    
    # Simula 3 saques (padrão seria bloqueado, mas aqui deve passar)
    conta.historico.transacoes.append({'tipo': 'Saque', 'valor': 10, 'data': '...'})
    conta.historico.transacoes.append({'tipo': 'Saque', 'valor': 10, 'data': '...'})
    conta.historico.transacoes.append({'tipo': 'Saque', 'valor': 10, 'data': '...'})
    
    assert conta.sacar(10) is True # 4º saque permitido

def test_27_saque_falho_nao_incrementa_historico_na_logica(conta_com_saldo):
    """
    Verifica se um saque falho (por saldo) não conta como realizado.
    (Teste de lógica: o estado não deve mudar).
    """
    saldo_antes = conta_com_saldo.saldo
    conta_com_saldo.sacar(2000) # Falha
    assert conta_com_saldo.saldo == saldo_antes

# ==========================================
# Grupo 6: Casos de Borda e Tipos (5 Testes)
# ==========================================

def test_28_saldo_tipo_final_eh_sempre_decimal(conta_zerada):
    """Garante que após várias operações o tipo se mantém Decimal."""
    conta_zerada.depositar(10.5)
    conta_zerada.sacar(5)
    assert isinstance(conta_zerada.saldo, Decimal)

def test_29_deposito_grande_valor(conta_zerada):
    """Verifica comportamento com valores muito altos."""
    valor_alto = 1_000_000_000.00
    conta_zerada.depositar(valor_alto)
    assert conta_zerada.saldo == Decimal('1000000000.00')

def test_30_saque_grande_valor_com_saldo(conta_zerada):
    """Verifica saque de valor alto se houver saldo."""
    conta_zerada.depositar(2000000)
    # Aumenta limite para teste
    conta_zerada.limite = Decimal('2000000')
    assert conta_zerada.sacar(1000000) is True
    assert conta_zerada.saldo == Decimal('1000000.00')

def test_31_saque_limite_exato(conta_com_saldo):
    """Verifica saque no valor exato do limite por transação."""
    assert conta_com_saldo.sacar(500) is True

def test_32_saque_1_centavo_acima_limite(conta_com_saldo):
    """Verifica saque de 500.01 (deve falhar se limite é 500)."""
    assert conta_com_saldo.sacar(500.01) is False