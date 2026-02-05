# Confiabilidade em Sistemas Financeiros com TDD

Este projeto compõe a parte prática do Trabalho de Conclusão de Curso (TCC) intitulado **"Confiabilidade em Sistemas Financeiros: Prevenção de Erros Críticos em Software Bancário com Test-Driven Development"**.

O objetivo é demonstrar empiricamente como a metodologia TDD (Test-Driven Development) previne erros críticos em sistemas bancários, como falhas de precisão numérica (ponto flutuante), erros de lógica de negócio e inconsistências de estado, comparando uma implementação "Tradicional" com uma implementação guiada por testes.

## Estrutura do Projeto

*   **`tdd/`**: Implementação do sistema bancário utilizando TDD, com uso de `Decimal` para precisão monetária e validações robustas (Guard Assertions).
*   **`traditional/`**: Implementação de controle simulando práticas comuns (uso de `float`), suscetível a erros de arredondamento.
*   **`services.py`**: Módulo de serviço que executa as simulações comparativas entre os dois métodos.
*   **`TDD.tex`**: Documento LaTeX com a fundamentação teórica e resultados.

## Pré-requisitos

*   **Python 3.13** ou superior.
*   **uv**: Gerenciador de pacotes e projetos Python de alta performance (Astral). **Obrigatório**.

## Instalação

O projeto utiliza o **uv** para gerenciar o ambiente virtual e instalar as ferramentas (**FastAPI**, **Uvicorn**, **Locust**, **Pytest**).

1.  **Instale o uv** (caso não tenha):

    **Windows (PowerShell):**
    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

    **Via Pip (Alternativa):**
    ```bash
    pip install uv
    ```

2.  **Clone o repositório** e navegue até a pasta do projeto:

    ```bash
    cd "TDD Banco"
    ```

3.  **Instale as dependências**:

    ```bash
    # Cria o ambiente virtual e instala tudo definido no pyproject.toml
    uv sync
    ```

## Execução

### Rodar a API (Uvicorn)

Para iniciar o servidor da aplicação e acessar as simulações:

```bash
uv run uvicorn api:app --reload
```

O servidor estará disponível em `/`.

### Rodar os Testes

Para executar a suíte de testes automatizados e verificar as correções aplicadas pelo TDD:

```bash
pytest
```

### Tecnologias

*   **FastAPI**: Framework web para expor os serviços de simulação.
*   **Uvicorn**: Servidor ASGI.
*   **Locust**: Ferramenta para testes de carga.
*   **Pytest**: Framework de testes unitários.