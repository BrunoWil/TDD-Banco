import requests

# Script auxiliar para visualizar o relatório da API em formato de tabela no terminal

def main():
    url = "http://127.0.0.1:8000/simulacao/relatorio"
    print(f"Consultando API: {url} ...")
    
    try:
        resp = requests.get(url)
        if resp.status_code != 200:
            print(f"Erro na API: {resp.status_code} - {resp.text}")
            return
            
        data = resp.json()
        detalhes = data['detalhes']
        
        # Definição do cabeçalho com a nova coluna 'Esperado'
        # Cenário | Tradicional | TDD | Esperado | Status
        print("\n" + "="*120)
        print(f"{'Cenário':<45} | {'Tradicional':<15} | {'TDD':<15} | {'Esperado':<15} | {'Status':<10}")
        print("="*120)
        
        for row in detalhes:
            nome = row['name'][:45]
            trad = str(row['saldo_trad'])
            tdd = str(row['saldo_tdd'])
            esp = str(row['esperado'])
            status = row['status']
            
            print(f"{nome:<45} | {trad:<15} | {tdd:<15} | {esp:<15} | {status:<10}")
            
        print("="*120)
        print(f"Resumo: {data['erros']} discrepâncias encontradas em {data['total']} casos de teste.")
        
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar à API.")
        print("Certifique-se de que o servidor está rodando: 'uvicorn api:app --reload'")

if __name__ == "__main__":
    main()