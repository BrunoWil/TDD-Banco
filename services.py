from traditional import main
from tdd import main_tdd

# Lista de casos de teste para execução em massa
TEST_CASES = [
    {'id': 't01', 'name': '01. Inicialização: Saldo Zero', 'bal': 0, 'lim': 500, 'limQ': 3, 'ops': [], 'expected': 0,
        'desc': "Setup/Fixture: Garante que o objeto Account é instanciado corretamente com o estado inicial esperado (Zero) antes de qualquer operação."},
    {'id': 't01_neg', 'name': '01b. Inicialização: Saldo Negativo', 'bal': -100, 'lim': 500, 'limQ': 3, 'ops': [], 'expected': 0,
        'desc': "Setup/Fixture: Tenta inicializar com saldo negativo. TDD deve sanitizar para 0, Tradicional aceita o erro."},
    {'id': 't02', 'name': '02. Inicialização: Saldo Float (100.50)', 'bal': 100.50, 'lim': 500, 'limQ': 3, 'ops': [
    ], 'expected': 100.50, 'desc': "Setup/Fixture: Verifica se o construtor aceita e converte corretamente tipos primitivos (float) para a representação interna segura."},
    {'id': 't03', 'name': '03. Inicialização: Limites Padrão', 'bal': 0, 'lim': 500, 'limQ': 3, 'ops': [
    ], 'expected': 0, 'desc': "Setup: Validação de valores default definidos nas regras de negócio."},
    {'id': 't04', 'name': '04. Inicialização: Limites Custom (1000/5)', 'bal': 0, 'lim': 1000, 'limQ': 5, 'ops': [
    ], 'expected': 0, 'desc': "Setup: Garante flexibilidade da classe para diferentes perfis de conta (injeção de dependência via construtor)."},
    {'id': 't05', 'name': '05. Atributos Cliente (Visual)', 'bal': 0, 'lim': 500, 'limQ': 3, 'ops': [
    ], 'expected': 0, 'desc': "Verificação de integridade de dados não-monetários."},
    {'id': 't06', 'name': '06. Depósito: Valor Positivo (100)', 'bal': 0, 'lim': 500, 'limQ': 3, 'ops': [
        {'tipo': 'deposito', 'valor': 100}], 'expected': 100, 'desc': "State Verification: Verifica se o método deposit() altera o estado do saldo corretamente. No TDD, começamos com a implementação mais simples (Green)."},
    {'id': 't07', 'name': '07. Depósito: String/Float (50.50)', 'bal': 0, 'lim': 500, 'limQ': 3, 'ops': [
        {'tipo': 'deposito', 'valor': 50.50}], 'expected': 50.50, 'desc': "Robustez de Tipos: Garante que o sistema aceita diferentes formatos numéricos sem quebrar."},
    {'id': 't08', 'name': '08. Depósito: Valor Zero', 'bal': 0, 'lim': 500, 'limQ': 3, 'ops': [
        {'tipo': 'deposito', 'valor': 0}], 'expected': 0, 'desc': "Guard Assertion: Regra de negócio que impede movimentações nulas."},
    {'id': 't09', 'name': '09. Depósito: Valor Negativo', 'bal': 0, 'lim': 500, 'limQ': 3, 'ops': [
        {'tipo': 'deposito', 'valor': -50}], 'expected': 0, 'desc': "Guard Assertion: Validação crítica para impedir injeção de valores negativos (que virariam saques disfarçados)."},
    {'id': 't10', 'name': '10. Depósito: Múltiplos (10, 20, 30)', 'bal': 0, 'lim': 500, 'limQ': 3, 'ops': [{'tipo': 'deposito', 'valor': 10}, {'tipo': 'deposito', 'valor': 20}, {
        'tipo': 'deposito', 'valor': 30}], 'expected': 60, 'desc': "Acumulação de Estado: Verifica se múltiplas operações sequenciais mantêm a consistência do saldo."},
    {'id': 't11', 'name': '11. Depósito: Centavos (0.01)', 'bal': 0, 'lim': 500, 'limQ': 3, 'ops': [
        {'tipo': 'deposito', 'valor': 0.01}], 'expected': 0.01, 'desc': "Precisão Básica: Verifica se o sistema consegue lidar com a menor unidade monetária possível."},
    {'id': 't12', 'name': '12. Saque: Saldo Suficiente (100)', 'bal': 1000, 'lim': 500, 'limQ': 3, 'ops': [
        {'tipo': 'saque', 'valor': 100}], 'expected': 900, 'desc': "Ciclo 1 (Lógica Básica): O teste define o 'Caminho Feliz' do saque. A implementação inicial (Green) apenas subtrai o valor."},
    {'id': 't13', 'name': '13. Saque: Total (Zerar Conta)', 'bal': 1000, 'lim': 2000, 'limQ': 3, 'ops': [
        {'tipo': 'saque', 'valor': 1000}], 'expected': 0, 'desc': "Teste de Limite: Verifica o comportamento exato quando Saldo == Saque."},
    {'id': 't14', 'name': '14. Saque: Insuficiente (Guard Assertion)', 'bal': 1000, 'lim': 2000, 'limQ': 3, 'ops': [
        {'tipo': 'saque', 'valor': 1001}], 'expected': 1000, 'desc': "Ciclo 2 (Guard Assertion): Este teste força a falha (Red) quando o saldo é insuficiente. A correção (Green) exige adicionar um 'if' para lançar exceção."},
    {'id': 't15', 'name': '15. Saque: Valor Zero', 'bal': 1000, 'lim': 500, 'limQ': 3, 'ops': [
        {'tipo': 'saque', 'valor': 0}], 'expected': 1000, 'desc': "Validação de Entrada: Impede operações nulas desnecessárias."},
    {'id': 't16', 'name': '16. Saque: Valor Negativo', 'bal': 1000, 'lim': 500, 'limQ': 3, 'ops': [
        {'tipo': 'saque', 'valor': -100}], 'expected': 1000, 'desc': "Segurança: Impede que um saque negativo se torne um depósito indevido."},
    {'id': 't17', 'name': '17. Saque: Acima Limite Transação (600)', 'bal': 1000, 'lim': 500, 'limQ': 3, 'ops': [
        {'tipo': 'saque', 'valor': 600}], 'expected': 1000, 'desc': "Regra de Negócio: Validação de limite por operação, independente do saldo disponível."},
    {'id': 't18', 'name': '18. Precisão: Soma (0.1+0.1+0.1)', 'bal': 0, 'lim': 500, 'limQ': 3, 'ops': [{'tipo': 'deposito', 'valor': 0.1}, {'tipo': 'deposito', 'valor': 0.1}, {
        'tipo': 'deposito', 'valor': 0.1}], 'expected': 0.30, 'desc': "Ciclo 3 (Precisão - Refactor): Expõe o erro clássico de ponto flutuante (0.30000000000000004). Exige refatoração para Decimal."},
    {'id': 't19', 'name': '19. Precisão: Subtração (1.10 - 0.40)', 'bal': 1.10, 'lim': 500, 'limQ': 3, 'ops': [
        {'tipo': 'saque', 'valor': 0.40}], 'expected': 0.70, 'desc': "Ciclo 3 (Precisão - Refactor): Verifica erro de subtração em float. Essencial para garantir integridade de saldo."},
    {'id': 't20', 'name': '20. Precisão: Multiplicação (100x 0.01)', 'bal': 0, 'lim': 500, 'limQ': 3, 'ops': [
        {'tipo': 'deposito', 'valor': 0.01}] * 100, 'expected': 1.00, 'desc': "Teste de Carga/Acumulação: Verifica se pequenos erros de precisão se acumulam ao longo de muitas transações."},
    {'id': 't21', 'name': '21. Arredondamento Entrada (10.555)', 'bal': 0, 'lim': 500, 'limQ': 3, 'ops': [
        {'tipo': 'deposito', 'valor': 10.555}], 'expected': 10.56, 'desc': "Política de Arredondamento: Define como o sistema lida com frações de centavos (ROUND_HALF_UP)."},
    {'id': 't22', 'name': '22. Arredondamento Saque (10.555)', 'bal': 1000, 'lim': 500, 'limQ': 3, 'ops': [
        {'tipo': 'saque', 'valor': 10.555}], 'expected': 989.44, 'desc': "Consistência: Garante que a política de arredondamento é aplicada tanto em entradas quanto em saídas."},
    {'id': 't23', 'name': '23. Limite Saques: Contagem Inicial', 'bal': 1000, 'lim': 500, 'limQ': 3, 'ops': [
        {'tipo': 'saque', 'valor': 10}], 'expected': 990, 'desc': "Controle de Estado: Verifica se o contador de saques é incrementado corretamente."},
    {'id': 't24', 'name': '24. Limite Saques: Bloqueio 4º Saque', 'bal': 1000, 'lim': 500, 'limQ': 3, 'ops': [{'tipo': 'saque', 'valor': 10}, {'tipo': 'saque', 'valor': 10}, {
        'tipo': 'saque', 'valor': 10}, {'tipo': 'saque', 'valor': 10}], 'expected': 970, 'desc': "Regra de Negócio (Stateful): Verifica se o sistema bloqueia operações após atingir o limite diário."},
    {'id': 't25', 'name': '25. Limite Saques: Depósito Permitido', 'bal': 1000, 'lim': 500, 'limQ': 3, 'ops': [{'tipo': 'saque', 'valor': 10}, {'tipo': 'saque', 'valor': 10}, {
        'tipo': 'saque', 'valor': 10}, {'tipo': 'deposito', 'valor': 100}], 'expected': 1070, 'desc': "Isolamento de Regras: Garante que o bloqueio de saques não afeta outras operações (depósitos)."},
    {'id': 't26', 'name': '26. Limite Saques: Customizado (5)', 'bal': 1000, 'lim': 500, 'limQ': 5, 'ops': [{'tipo': 'saque', 'valor': 10}, {'tipo': 'saque', 'valor': 10}, {
        'tipo': 'saque', 'valor': 10}, {'tipo': 'saque', 'valor': 10}], 'expected': 960, 'desc': "Configuração Dinâmica: Verifica se o limite de saques respeita a configuração da instância."},
    {'id': 't27', 'name': '27. Lógica: Falha não incrementa', 'bal': 1000, 'lim': 500, 'limQ': 3, 'ops': [{'tipo': 'saque', 'valor': 2000}, {
        'tipo': 'saque', 'valor': 10}], 'expected': 990, 'desc': "Atomicidade/Rollback: Uma operação falha (ex: saldo insuficiente) NÃO deve incrementar o contador de saques realizados."},
    {'id': 't28', 'name': '28. Tipos: Decimal Preservado', 'bal': 0, 'lim': 500, 'limQ': 3, 'ops': [{'tipo': 'deposito', 'valor': 10.5}, {
        'tipo': 'saque', 'valor': 5}], 'expected': 5.5, 'desc': "Integridade de Tipos: Garante que operações mistas não degradam o tipo Decimal para float."},
    {'id': 't29', 'name': '29. Borda: Depósito Bilhão', 'bal': 0, 'lim': 500, 'limQ': 3, 'ops': [
        {'tipo': 'deposito', 'valor': 1000000000}], 'expected': 1000000000, 'desc': "Teste de Borda (Overflow): Verifica comportamento com valores muito grandes."},
    {'id': 't30', 'name': '30. Borda: Saque Milhão', 'bal': 0, 'lim': 2000000, 'limQ': 3, 'ops': [{'tipo': 'deposito', 'valor': 2000000}, {
        'tipo': 'saque', 'valor': 1000000}], 'expected': 1000000, 'desc': "Teste de Carga: Operações de alto valor."},
    {'id': 't31', 'name': '31. Borda: Limite Exato (500)', 'bal': 1000, 'lim': 500, 'limQ': 3, 'ops': [
        {'tipo': 'saque', 'valor': 500}], 'expected': 500, 'desc': "Teste de Limite (Boundary): Verifica se a condição é > ou >=."},
    {'id': 't32', 'name': '32. Borda: Acima Limite (500.01)', 'bal': 1000, 'lim': 500, 'limQ': 3, 'ops': [
        {'tipo': 'saque', 'valor': 500.01}], 'expected': 1000, 'desc': "Teste de Limite (Boundary): Verifica se 1 centavo acima do limite é bloqueado."}
]


def run_traditional_simulation(req: main_tdd.SimulacaoRequest):
    cliente = main.PessoaFisica("Tradicional", "01/01/1990", "111", "Rua A")
    conta = main.ContaCorrente(
        1, cliente, limite=req.limite, limite_saque=req.limite_saque)
    conta._saldo = req.saldo_inicial  # Força float

    log = []
    for op in req.operacoes:
        sucesso = False
        if op.tipo == "deposito":
            transacao = main.Deposito(op.valor)
            sucesso = transacao.registrar(conta)
        elif op.tipo == "saque":
            transacao = main.Saque(op.valor)
            sucesso = transacao.registrar(conta)

        log.append({"op": op.tipo, "valor": op.valor,
                   "sucesso": sucesso, "saldo": conta.saldo})

    return {
        "metodo": "Tradicional (Float)",
        "saldo_final": conta.saldo,
        "tipo_dado": str(type(conta.saldo)),
        "historico": log
    }


def run_tdd_simulation(req: main_tdd.SimulacaoRequest):
    cliente = main_tdd.PessoaFisica("TDD", "01/01/1990", "222", "Rua B")
    conta = main_tdd.ContaTDD(1, cliente, saldo=req.saldo_inicial,
                              limite=req.limite, limite_saque=req.limite_saque)

    log = []
    for op in req.operacoes:
        sucesso = False
        if op.tipo == "deposito":
            sucesso = conta.depositar(op.valor)
            if sucesso and not hasattr(conta, 'auto_historico'):
                conta.historico.adicionar_transacao(
                    main_tdd.Deposito(op.valor))
        elif op.tipo == "saque":
            sucesso = conta.sacar(op.valor)
            if sucesso and not hasattr(conta, 'auto_historico'):
                conta.historico.adicionar_transacao(main_tdd.Saque(op.valor))

        log.append({"op": op.tipo, "valor": op.valor,
                   "sucesso": sucesso, "saldo": float(conta.saldo)})

    return {
        "metodo": "TDD (Decimal)",
        "saldo_final": float(conta.saldo),
        "tipo_dado": "<class 'decimal.Decimal'>",
        "historico": log
    }


def generate_report():
    results = []
    discrepancies = 0

    for case in TEST_CASES:
        ops = [main_tdd.Operacao(tipo=op['tipo'], valor=op['valor'])
               for op in case['ops']]
        req = main_tdd.SimulacaoRequest(
            saldo_inicial=case['bal'],
            limite=case['lim'],
            limite_saque=case['limQ'],
            operacoes=ops
        )

        # Executa Tradicional
        res_trad = run_traditional_simulation(req)

        # Executa TDD
        res_tdd = run_tdd_simulation(req)

        saldo_trad = res_trad['saldo_final']
        saldo_tdd = res_tdd['saldo_final']

        status = "OK"
        msg_erro = ""

        if saldo_trad != saldo_tdd:
            status = "ERRO (Valor)"
            discrepancies += 1
            msg_erro = f"Divergência: Tradicional {saldo_trad} vs TDD {saldo_tdd}"
        else:
            trad_success = sum(
                1 for h in res_trad['historico'] if h['sucesso'])
            tdd_success = sum(1 for h in res_tdd['historico'] if h['sucesso'])
            if trad_success != tdd_success:
                status = "ERRO (Lógica)"
                discrepancies += 1
                msg_erro = f"Lógica: Tradicional permitiu {trad_success} ops, TDD {tdd_success}"

        results.append({
            "name": case['name'],
            "desc": case['desc'],
            "saldo_trad": saldo_trad,
            "saldo_tdd": saldo_tdd,
            "esperado": case['expected'],
            "status": status,
            "msg_erro": msg_erro,
            "tipo_trad": res_trad['tipo_dado'],
            "tipo_tdd": res_tdd['tipo_dado']
        })

    return {
        "total": len(TEST_CASES),
        "erros": discrepancies,
        "detalhes": results
    }


def get_all_test_cases():
    return TEST_CASES
