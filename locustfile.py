from locust import HttpUser, task, between

class BancoUser(HttpUser):
    # Tempo de espera entre as tarefas (simula comportamento humano ou latência)
    wait_time = between(0.5, 2)

    @task(1)
    def teste_precisao_tdd(self):
        """
        Testa o endpoint TDD com operações de ponto flutuante.
        Verifica se o sistema aguenta cálculos de precisão sob carga.
        """
        payload = {
            "saldo_inicial": 0.0,
            "operacoes": [
                {"tipo": "deposito", "valor": 0.1},
                {"tipo": "deposito", "valor": 0.1},
                {"tipo": "deposito", "valor": 0.1}
            ]
        }
        self.client.post("/simulacao/tdd", json=payload, name="/simulacao/tdd (Precisão)")

    @task(2)
    def teste_tentativa_saldo_negativo(self):
        """
        Cenário: Esgotar o saldo até zero e tentar sacar mais.
        Objetivo: Verificar se o sistema bloqueia saldo negativo antes do limite de saques.
        Saldo Inicial: 20.00
        Operações: 3 saques de 10.00.
        1. 20 -> 10 (Sucesso)
        2. 10 -> 0 (Sucesso)
        3. 0 -> -10 (Deve falhar por Saldo Insuficiente)
        """
        payload = {
            "saldo_inicial": 20.0,
            "operacoes": [
                {"tipo": "saque", "valor": 10},
                {"tipo": "saque", "valor": 10},
                {"tipo": "saque", "valor": 10}
            ]
        }
        self.client.post("/simulacao/tdd", json=payload, name="/simulacao/tdd (Saldo Zero/Negativo)")

    @task(2)
    def teste_limite_saques_tdd(self):
        """
        Testa a regra de negócio de limite de saques.
        Peso 2 (executa 2x mais que o teste de precisão).
        """
        payload = {
            "saldo_inicial": 1000.0,
            "operacoes": [
                {"tipo": "saque", "valor": 10},
                {"tipo": "saque", "valor": 10},
                {"tipo": "saque", "valor": 10},
                {"tipo": "saque", "valor": 10} # 4º saque deve ser bloqueado
            ]
        }
        self.client.post("/simulacao/tdd", json=payload, name="/simulacao/tdd (Regras de Negócio)")

    @task(1)
    def teste_acumulacao_massiva(self):
        """
        Cenário: Acumulação de Saldo (Carga Alta).
        Objetivo: Testar precisão e performance com 50 depósitos consecutivos.
        """
        # Gera 50 operações de depósito de R$ 1000.00
        ops = [{"tipo": "deposito", "valor": 1000.0} for _ in range(50)]
        
        payload = {
            "saldo_inicial": 0.0,
            "operacoes": ops
        }
        self.client.post("/simulacao/tdd", json=payload, name="/simulacao/tdd (Acumulação Massiva)")

    @task(1)
    def teste_comparativo_tradicional(self):
        """
        Testa o endpoint Tradicional para fins de comparação de performance e estabilidade.
        """
        payload = {
            "saldo_inicial": 0.0,
            "operacoes": [
                {"tipo": "deposito", "valor": 0.1},
                {"tipo": "deposito", "valor": 0.1},
                {"tipo": "deposito", "valor": 0.1}
            ]
        }
        self.client.post("/simulacao/tradicional", json=payload, name="/simulacao/tradicional (Comparação)")
