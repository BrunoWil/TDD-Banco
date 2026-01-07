from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from tdd import main_tdd # Importa a implementação TDD da nova pasta
import services # Camada de serviços

app = FastAPI()

# Configuração de CORS para permitir que o frontend acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/simulacao/tradicional")
def simular_tradicional(req: main_tdd.SimulacaoRequest):
    """
    Executa operações usando a classe ContaCorrente original do main.py.
    Esperado: Erros de precisão (float) e falha no limite de saques.
    """
    return services.run_traditional_simulation(req)

@app.post("/simulacao/tdd")
def simular_tdd(req: main_tdd.SimulacaoRequest):
    """
    Executa operações usando a classe ContaTDD.
    Esperado: Precisão exata e respeito às regras de negócio.
    """
    return services.run_tdd_simulation(req)

@app.get("/simulacao/relatorio")
def gerar_relatorio():
    return services.generate_report()

@app.get("/", response_class=HTMLResponse)
def read_root():
    """Serve o arquivo index.html se existir."""
    try:
        with open("templates/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Arquivo index.html não encontrado.</h1>"

@app.get("/index.html", response_class=HTMLResponse)
def read_index():
    """Serve o arquivo index.html explicitamente para corrigir navegação."""
    return read_root()

@app.get("/mass_tests.html", response_class=HTMLResponse)
def read_mass_tests():
    """Serve o arquivo mass_tests.html se existir."""
    try:
        with open("templates/mass_tests.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Arquivo mass_tests.html não encontrado.</h1>"
